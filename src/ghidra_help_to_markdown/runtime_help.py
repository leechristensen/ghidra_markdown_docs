"""Read Ghidra's help model from a running Ghidra JVM.

Bypasses the source-tree-walking pipeline. Works against an installed
Ghidra (no source needed): the help system is loaded at runtime through
``ghidra.base.help.GhidraHelpService.install()``, which discovers every
``<Module>_HelpSet.hs`` on the classpath, parses each one, and merges
the cross-module ``combinedMap``. We then walk the merged TOC and read
each topic's HTML content via ``URL.openStream()`` from the module jar.

This is the runtime equivalent of what Ghidra's Swing UI does when you
press F1 — same API surface, same resolution rules (theme-aware icons,
``GHelpSet.getCombinedMap()`` for cross-module IDs, etc.). The
maintainer's note in issue #8747 called this "the easiest path."
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Optional

from . import ghidra_session

_log = logging.getLogger(__name__)

# jar:file:/.../<Module>.jar!/help/topics/<Topic>/<file>.htm[#anchor]
_JAR_URL_RE = re.compile(
    r"^jar:file:(?P<jar>[^!]+)!/help/(?P<inner>[^#]+)(?:#(?P<anchor>.*))?$"
)
# file:/.../help/topics/...
_FILE_URL_RE = re.compile(r"^file:(?P<path>[^#]+)(?:#(?P<anchor>.*))?$")


@dataclass
class RuntimeTopic:
    """One help topic as exposed by the runtime help service."""

    help_id: str  # e.g. "Tool_Configure_Tool"
    url: str  # full jar:file:.../!/help/topics/... URL
    inner_path: str  # "topics/Tool/Configure_Tool.html" (the part after help/)
    anchor: Optional[str] = None  # fragment if present
    module: Optional[str] = None  # "Tool", "FunctionID", ...
    topic_dir: Optional[str] = None  # "Tool" (the directory under help/topics/)
    filename: Optional[str] = None  # "Configure_Tool.html"


@dataclass
class RuntimeTOCEntry:
    """One node in the merged TOC. Mirrors the existing toc_parser.TOCEntry shape."""

    id: str
    text: str
    target_id: Optional[str] = None  # help-id target (may be None for grouping nodes)
    target_url: Optional[str] = None  # resolved URL from combinedMap
    inner_path: Optional[str] = None  # "topics/Tool/X.html"
    anchor: Optional[str] = None
    is_external: bool = False  # target starts with "external:"
    children: list["RuntimeTOCEntry"] = field(default_factory=list)


class RuntimeHelp:
    """Wrapper over Ghidra's in-JVM help service."""

    def __init__(self, install_dir: Path) -> None:
        ghidra_session.start(install_dir)
        self._install_dir = install_dir

        self._GhidraHelpService = ghidra_session.jclass("ghidra.base.help.GhidraHelpService")
        self._Help = ghidra_session.jclass("help.Help")
        self._URL = ghidra_session.jclass("java.net.URL")

        self._GhidraHelpService.install()
        svc = self._Help.getHelpService()
        if not bool(svc.helpExists()):
            raise RuntimeError(
                f"Ghidra help did not load from install at {install_dir}. "
                "The install may be missing built help; try ghidraRun once to ensure built."
            )
        self._service = svc
        self._helpset = svc.getMasterHelpSet()
        self._cmap = self._helpset.getCombinedMap()

    # ------------------------------------------------------------------
    # TOC enumeration

    def walk_toc(self) -> list[RuntimeTOCEntry]:
        """Return the merged TOC as a list of top-level entries with children."""
        toc_view = self._helpset.getNavigatorView("TOC")
        tree = toc_view.getDataAsTree()
        top: list[RuntimeTOCEntry] = []
        children = tree.children()
        while children.hasMoreElements():
            node = children.nextElement()
            entry = self._node_to_entry(node)
            if entry is not None:
                top.append(entry)
        return top

    def _node_to_entry(self, node: Any) -> Optional[RuntimeTOCEntry]:  # noqa: ANN401
        obj = node.getUserObject()
        if obj is None:
            # Synthetic root or malformed node; still walk children
            entry = RuntimeTOCEntry(id="", text="")
        else:
            text = str(obj.getDisplayText() or "")
            toc_id = str(obj.getTocID() or "")
            target_id_obj = obj.getID()
            target_id = str(target_id_obj.getIDString()) if target_id_obj is not None else None
            target_url: Optional[str] = None
            inner: Optional[str] = None
            anchor: Optional[str] = None
            is_external = False

            if target_id:
                if target_id.startswith("external:"):
                    is_external = True
                    target_url = target_id  # keep "external:..." form for caller
                else:
                    url_obj = self._cmap.getURLFromID(target_id_obj)
                    if url_obj is not None:
                        target_url = str(url_obj)
                        inner, anchor = parse_help_url(target_url)

            entry = RuntimeTOCEntry(
                id=toc_id,
                text=text,
                target_id=target_id,
                target_url=target_url,
                inner_path=inner,
                anchor=anchor,
                is_external=is_external,
            )

        enum = node.children()
        while enum.hasMoreElements():
            child = enum.nextElement()
            child_entry = self._node_to_entry(child)
            if child_entry is not None:
                entry.children.append(child_entry)
        return entry

    # ------------------------------------------------------------------
    # Topic enumeration

    def iter_topics(self) -> Iterable[RuntimeTopic]:
        """Yield every help topic across all loaded HelpSets.

        The master HelpSet's combined-map ``getAllIDs()`` only enumerates IDs
        from the *master* helpset's own map (not merged ones), so a 12.0.4
        install reports 1577 IDs instead of the actual 2716 across all 50+
        merged HelpSets. We iterate every helpset's local map and look each ID
        up through the master combined map so cross-module references resolve.
        """
        seen: set[str] = set()
        helpsets = self._collect_helpsets()
        for hs in helpsets:
            local = hs.getLocalMap()
            ids = local.getAllIDs()
            while ids.hasMoreElements():
                id_obj = ids.nextElement()
                help_id = str(id_obj.id)
                if help_id in seen:
                    continue
                seen.add(help_id)
                url_obj = self._cmap.getURLFromID(id_obj)
                if url_obj is None:
                    # Fall back to the local map's URL if combined lookup fails
                    url_obj = local.getURLFromID(id_obj)
                if url_obj is None:
                    continue
                url = str(url_obj)
                inner, anchor = parse_help_url(url)
                if inner is None:
                    continue
                module = _module_from_url(url)
                topic_dir, filename = _topic_from_inner(inner)
                yield RuntimeTopic(
                    help_id=help_id,
                    url=url,
                    inner_path=inner,
                    anchor=anchor,
                    module=module,
                    topic_dir=topic_dir,
                    filename=filename,
                )

    def _collect_helpsets(self) -> list[Any]:
        """Master HelpSet + every recursively-merged HelpSet, flattened."""
        result: list[Any] = [self._helpset]

        def visit(hs: Any) -> None:  # noqa: ANN401
            enum = hs.getHelpSets()
            while enum.hasMoreElements():
                sub = enum.nextElement()
                result.append(sub)
                visit(sub)

        visit(self._helpset)
        return result

    # ------------------------------------------------------------------
    # Content access

    def read_url(self, url: str) -> bytes:
        """Read the bytes at a help URL (typically jar:file:.../!/help/topics/...)."""
        url_obj = self._URL(url.split("#", 1)[0])  # strip fragment if any
        stream = url_obj.openStream()
        try:
            # Use Java 9+ InputStream.readAllBytes() — avoids the JPype buffer-copy
            # quirks that bytearray + read(byte[]) has at the Python <-> Java boundary.
            raw = stream.readAllBytes()
            return bytes(raw)
        finally:
            stream.close()

    def read_text(self, url: str, encodings: tuple[str, ...] = ("utf-8", "windows-1252", "iso-8859-1")) -> str:
        """Read a help URL as text, trying the same encoding ladder as the file-based path."""
        raw = self.read_url(url)
        for enc in encodings:
            try:
                return raw.decode(enc)
            except UnicodeDecodeError:
                continue
        return raw.decode("utf-8", errors="ignore")


# ----------------------------------------------------------------------
# URL parsing helpers (module-level for testability)


def parse_help_url(url: str) -> tuple[Optional[str], Optional[str]]:
    """Return (inner_path, anchor) given a Ghidra help URL.

    inner_path is the part after ``/help/`` so ``help/topics/X/Y.html`` ->
    ``topics/X/Y.html``. Returns (None, None) if the URL doesn't match.
    """
    m = _JAR_URL_RE.match(url)
    if m:
        return m.group("inner"), m.group("anchor")
    m = _FILE_URL_RE.match(url)
    if m:
        # For file: URLs find /help/ marker
        p = m.group("path")
        idx = p.find("/help/")
        if idx >= 0:
            return p[idx + len("/help/"):], m.group("anchor")
    return None, None


def _module_from_url(url: str) -> Optional[str]:
    """Extract the module name from a jar URL.

    ``jar:file:.../Features/Base/lib/Base.jar!/help/topics/...`` -> "Base".
    """
    m = re.search(r"/([A-Za-z0-9_-]+)\.jar!/", url)
    if m:
        return m.group(1)
    return None


def _topic_from_inner(inner: str) -> tuple[Optional[str], Optional[str]]:
    """Given ``topics/Tool/Configure_Tool.html`` return ("Tool", "Configure_Tool.html")."""
    parts = inner.split("/")
    if len(parts) >= 3 and parts[0] == "topics":
        return parts[1], parts[-1]
    return None, None
