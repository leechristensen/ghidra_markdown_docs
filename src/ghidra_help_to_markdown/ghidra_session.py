"""Lazy pyghidra session wrapper.

Exposes Ghidra's Java help classes to the rest of the Python pipeline via
JPype. The session starts on first use and is process-global — pyghidra
cannot be restarted within a single Python process, so callers must accept
that the install dir is fixed for the lifetime of the process.

A note on Ghidra's help model: ``HelpModuleCollection.fromFiles`` and
``fromHelpLocations`` only accept ONE source-input help directory per
collection (the maintainer's docstring on ``HelpModuleCollection`` notes
this is "a bit conceptually muddled" — it reflects Ghidra's per-module
build, not multi-module input). For cross-module operations we either
build a collection per module, or skip the collection abstraction and
call the lower-level utilities (``HelpBuildUtils``, ``GhidraTOCFile``)
directly.
"""

from __future__ import annotations

import threading
from pathlib import Path
from typing import Any, Optional  # noqa: F401  - Any is used in return type annotations below

_lock = threading.Lock()
_started = False
_install_dir: Optional[Path] = None


def start(install_dir: Path) -> None:
    """Start pyghidra against the given Ghidra install. Idempotent per process.

    Also boots Ghidra's HeadlessThemeManager so that icon/theme lookups work
    (without it, ``Gui.hasIcon("icon.X")`` returns False and ``Icons.X_ICON``
    resolves to a placeholder rather than the real image).

    Raises ValueError if called twice with different install_dir values
    (pyghidra cannot be restarted with a different install in the same process).
    """
    global _started, _install_dir
    with _lock:
        if _started:
            if _install_dir != install_dir:
                raise ValueError(
                    f"pyghidra already started against {_install_dir}; "
                    f"cannot re-start against {install_dir}"
                )
            return
        import pyghidra  # type: ignore[import-untyped]

        pyghidra.start(install_dir=str(install_dir))
        _install_dir = install_dir
        _started = True

        # Boot the theme manager. Ghidra's GHelpBuilder does this in its
        # ApplicationConfiguration.initializeApplication override (see
        # GHelpBuilder.java:80). Without it, theme-driven icon refs fail silently.
        from jpype import JClass  # type: ignore[import-untyped]

        JClass("generic.theme.HeadlessThemeManager").initialize()


def is_started() -> bool:
    return _started


def jclass(name: str) -> Any:  # noqa: ANN401 - JPype types have no Python stub
    """Look up a Java class by FQN. Requires start() to have been called."""
    if not _started:
        raise RuntimeError("pyghidra session not started; call ghidra_session.start() first")
    from jpype import JClass  # type: ignore[import-untyped]

    return JClass(name)


def java_file(path: Path) -> Any:  # noqa: ANN401
    """Wrap a pathlib.Path as a java.io.File."""
    return jclass("java.io.File")(str(path))


def java_path(path: Path) -> Any:  # noqa: ANN401
    """Wrap a pathlib.Path as a java.nio.file.Path."""
    return jclass("java.nio.file.Paths").get(str(path))
