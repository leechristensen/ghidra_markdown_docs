"""Icon resolver backed by Ghidra's own help utilities.

Replaces the old heuristic resolver (which parsed ``Icons.java`` and
``*.theme.properties`` from the source tree). All resolution now goes
through ``help.HelpBuildUtils.locateImageReference`` which is the same
function Ghidra's build uses. For runtime icons that resolve to a URL
inside a jar (e.g. ``jar:file:.../Gui.jar!/images/Plus2.png``) the bytes
are extracted into a per-session cache directory so the rest of the
pipeline can treat them as ordinary files.

If pyghidra isn't started yet, callers should call
``ghidra_session.start(install_dir)`` first. The resolver itself is just
a thin Python facade over the Java APIs.
"""

from __future__ import annotations

import logging
import shutil
import tempfile
from pathlib import Path
from typing import Optional

from . import ghidra_session

_log = logging.getLogger(__name__)


class IconResolver:
    """Resolve Ghidra icon/image references to real files on disk."""

    def __init__(self, ghidra_root: Path, install_dir: Optional[Path] = None) -> None:
        """Initialize the resolver.

        Args:
            ghidra_root: Path to the Ghidra source tree being converted.
                Retained for compatibility with the previous resolver's
                signature; not used directly by the JVM-backed paths.
            install_dir: Path to an installed Ghidra (the same install
                already passed to ``ghidra_session.start``). Required so
                we can look up icons even if start() hasn't been called yet.
        """
        self.ghidra_root = ghidra_root
        self.install_dir = install_dir

        if not ghidra_session.is_started():
            if install_dir is None:
                raise RuntimeError(
                    "IconResolver requires either an already-started pyghidra "
                    "session or install_dir= to start one"
                )
            ghidra_session.start(install_dir)

        self._help_build_utils = ghidra_session.jclass("help.HelpBuildUtils")
        self._jpaths = ghidra_session.jclass("java.nio.file.Paths")

        # Per-session cache for icons extracted from jars. Lives until the
        # process exits; callers don't need to clean it up.
        self._cache_dir = Path(tempfile.mkdtemp(prefix="ghidra-icons-"))
        self._cache: dict[str, Optional[Path]] = {}

    def get_stats(self) -> dict:
        """Compatibility shim — the JVM resolver doesn't maintain table sizes."""
        return {
            "icons_field_to_id": 0,
            "id_to_filename": 0,
            "filename_to_path": 0,
        }

    def resolve(self, src: str, source_path: Optional[Path] = None) -> Optional[Path]:
        """Resolve an icon reference to an on-disk Path.

        Handles three input forms in one call (whatever ``locateImageReference``
        accepts): programmatic refs like ``Icons.ADD_ICON`` / ``icon.add``,
        relative refs like ``images/foo.png``, and absolute URLs.

        Args:
            src: The HTML ``src`` value (icon ref, relative path, or URL).
            source_path: Path to the source HTML file that contains the
                reference. Required for relative-path resolution; for
                programmatic refs, any plausible help file path works.

        Returns:
            Filesystem ``Path`` to the resolved icon, or ``None`` if the
            reference is invalid, remote, or a synthesized icon with no
            extractable image.
        """
        cache_key = f"{source_path}|{src}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        # Need *some* source path for HelpBuildUtils to anchor relative refs.
        # For pure programmatic refs the value isn't actually consulted.
        if source_path is None:
            source_path = self.ghidra_root / "Ghidra/Features/Base/src/main/help/help/topics/About/About_Ghidra.html"

        resolved = self._resolve_via_jvm(src, source_path)
        self._cache[cache_key] = resolved
        return resolved

    def resolve_by_filename(self, filename: str, source_path: Optional[Path] = None) -> Optional[Path]:
        """Compatibility wrapper for callers that have only a bare filename.

        Reconstructs the original HTML ``src`` form (``images/<filename>``) and
        delegates to :meth:`resolve`.
        """
        if not filename:
            return None
        return self.resolve(f"images/{filename}", source_path)

    def _resolve_via_jvm(self, src: str, source_path: Path) -> Optional[Path]:
        try:
            jsrc = self._jpaths.get(str(source_path))
            location = self._help_build_utils.locateImageReference(jsrc, src)
        except Exception as exc:  # noqa: BLE001
            _log.debug("locateImageReference threw on %r: %s", src, exc)
            return None

        if location is None:
            return None
        try:
            if bool(location.isInvalidRuntimeImage()):
                return None
            if bool(location.isRemote()):
                return None
        except Exception:  # noqa: BLE001
            pass

        # Filesystem-resolved path takes priority — `images/foo.png` and
        # `help/shared/note.png` come back this way.
        resolved_path = location.getResolvedPath()
        if resolved_path is not None:
            fs_path = Path(str(resolved_path))
            if fs_path.exists():
                return fs_path

        # Runtime icons resolve to a jar: URI. Extract once into the cache.
        uri = location.getResolvedUri()
        if uri is not None:
            uri_str = str(uri)
            if uri_str.startswith("jar:") or uri_str.startswith("file:"):
                extracted = self._extract_uri(uri_str, src)
                if extracted is not None:
                    return extracted

        # Fallback: classpath lookup. Ghidra's runtime resolves jar-root
        # resources like "images/icon_link.gif" via ResourceManager when the
        # filesystem-relative resolve(sourceFile, ref) fails. Mirror that here
        # so HTML refs to shared (non-topic-local) images survive conversion.
        # Programmatic refs (Icons.X / icon.X) are already handled above, skip
        # them here so we don't double-process.
        if not src.startswith(("Icons.", "icon.")):
            try:
                resource_manager = ghidra_session.jclass("resources.ResourceManager")
                cp_url = resource_manager.getResource(src)
                if cp_url is not None:
                    return self._extract_uri(str(cp_url), src)
            except Exception as exc:  # noqa: BLE001
                _log.debug("ResourceManager.getResource failed on %r: %s", src, exc)

        return None

    def _extract_uri(self, uri_str: str, src: str) -> Optional[Path]:
        """Copy the content at ``uri_str`` into the per-session cache."""
        # Derive a stable filename from the URI's tail to avoid collisions
        # between icons that share the same logical name across jars.
        name = uri_str.rsplit("/", 1)[-1].rsplit("!", 1)[-1].lstrip("/")
        if not name:
            name = "icon.png"
        cache_path = self._cache_dir / name
        if cache_path.exists():
            return cache_path

        URL = ghidra_session.jclass("java.net.URL")  # noqa: N806
        Files = ghidra_session.jclass("java.nio.file.Files")  # noqa: N806
        StandardCopyOption = ghidra_session.jclass("java.nio.file.StandardCopyOption")  # noqa: N806
        try:
            url = URL(uri_str)
            stream = url.openStream()
            try:
                Files.copy(
                    stream,
                    self._jpaths.get(str(cache_path)),
                    StandardCopyOption.REPLACE_EXISTING,
                )
            finally:
                stream.close()
        except Exception as exc:  # noqa: BLE001
            _log.debug("failed to extract %r for %r: %s", uri_str, src, exc)
            return None

        if cache_path.exists():
            return cache_path
        return None

    def cleanup_cache(self) -> None:
        """Remove the per-session icon cache. Called at program shutdown."""
        if self._cache_dir.exists():
            shutil.rmtree(self._cache_dir, ignore_errors=True)
