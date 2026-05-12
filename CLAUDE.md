# CLAUDE.md

## Project Overview

This is a Python CLI tool that converts Ghidra's HTML help documentation to Markdown format with cross-references and navigation.

## Tech Stack

- Python 3.13+
- BeautifulSoup4 + lxml for HTML parsing
- pyghidra (JPype bridge to a headless Ghidra JVM) for icon resolution and runtime help loading
- uv for dependency management
- Ruff for linting/formatting

Runtime mode requires Ghidra ≥ 12.0 (PyPI pyghidra 3.x constraint). Source-tree mode works against any Ghidra checkout.

## Project Structure

```
src/ghidra_help_to_markdown/
  main.py              # Entry point, orchestrates conversion; auto-detects install vs source tree
  ghidra_session.py    # Idempotent pyghidra startup + HeadlessThemeManager init
  runtime_help.py      # Reads merged TOC + topic URLs from a running Ghidra JVM
  toc_parser.py        # Source-tree TOC_Source.xml parser
  html_converter.py    # HTML to Markdown body conversion (handles tables, lists,
                       #   dl/dt/dd pandoc-style, callouts, clickable images, <u>)
  link_resolver.py     # help/topics/... -> relative Markdown paths
  icon_resolver.py     # HelpBuildUtils.locateImageReference + ResourceManager fallback
  generate_full_index.py  # Generates index-full.md with all headers
  validator.py         # Standalone link/anchor/render checker
```

## Commands

```bash
# Install dependencies
uv sync

# Run against an installed Ghidra (runtime mode; auto-detects via ghidraRun)
uv run ghidra-help-to-markdown /path/to/installed/ghidra ./docs

# Run against a source-tree checkout, with a 12.x install for icon resolution
uv run ghidra-help-to-markdown /path/to/ghidra-source ./docs \
  --ghidra-install /path/to/installed/ghidra

# Validate output for broken links
uv run ghidra-docs-validator ./docs/Ghidra_12.0.4_PUBLIC

# Lint and format
uv run ruff check src/
uv run ruff format src/
```

Output is auto-suffixed with the Ghidra version: `./docs/Ghidra_<version>/`.

## Key Concepts

1. **Two operating modes**: installed Ghidra (reads help from module jars via pyghidra) or source-tree checkout (walks `src/main/help/help/topics/`). Detection is on `ghidraRun` existence.
2. **Help-via-runtime**: in install mode we call `GhidraHelpService.install()` to merge every `<Module>_HelpSet.hs`, then iterate the combined map + every merged HelpSet's local map for the full cross-module topic list. HTML is read via `URL.openStream()` on `jar:file:...` URLs.
3. **HTML Conversion**: transforms HTML help files to Markdown preserving structure. Pandoc-style definition lists, clickable images, `<u>` HTML pass-through.
4. **Link Resolution**: converts `help/topics/...` paths to relative Markdown paths; slugifies anchors to match GFM heading slugs.
5. **Icon Resolution**: pyghidra-backed via `HelpBuildUtils.locateImageReference`. Programmatic refs (`Icons.X`, `icon.X`), filesystem-relative refs, and jar-root images (via `ResourceManager.getResource` fallback) all route through it.
6. **Validation**: checks converted docs for broken internal links and missing images; the conversion run itself prints a summary at the end.

## Code Style

- Line length: 120 characters
- Type annotations required (ANN rules enabled)
- Import sorting via Ruff
- Double quotes for strings

## Testing Changes

After making changes, verify by:
1. Running `uv run ruff check src/` to check for lint errors
2. Running the converter on a Ghidra installation
3. Running the validator on the output: `uv run ghidra-docs-validator ./docs`
