# Ghidra Help to Markdown Converter

Converts Ghidra's HTML help documentation to Markdown with best-effort cross-references and navigation.

Vibe coded and several things are probably broken, but does a pretty decent job!

## Quick Start

Point it at an installed Ghidra:

```bash
uv sync
uv run ghidra-help-to-markdown /path/to/ghidra ./docs
```

Or at a source-tree checkout (handy for tagged releases and dev builds):

```bash
git clone --depth 1 --branch Ghidra_12.0.4_build https://github.com/NationalSecurityAgency/ghidra
uv run ghidra-help-to-markdown ./ghidra ./docs --ghidra-install /path/to/installed/ghidra
```

Either way, output lands at `./docs/Ghidra_<version>/` — the version is
read from `Ghidra/application.properties` and appended automatically so
multiple builds can coexist:

```
docs/
  Ghidra_12.0.4_PUBLIC/
  Ghidra_11.3_DEV/
  ...
```

## Modes

The converter detects what you point it at and picks one of two modes:

- **Installed Ghidra (runtime mode)**: directory contains `ghidraRun`.
  Boots a headless Ghidra JVM via [`pyghidra`](https://pypi.org/project/pyghidra/)
  and reads help straight out of the module jars. No filesystem extraction.
  Cross-module link resolution and icon lookup go through Ghidra's own
  `GhidraHelpService` and `HelpBuildUtils` — same code the Swing help
  viewer uses.

- **Source tree mode**: directory has `**/src/main/help/help/topics/`.
  Walks the help files on disk. Pass `--ghidra-install <path>` to a
  built/installed Ghidra to resolve programmatic icon refs
  (`Icons.ADD_ICON`, `icon.bsim.connected`); without it those refs fall
  back to text placeholders.

## Options

```
--ghidra-install PATH   Path to an installed/extracted Ghidra. Required
                        for programmatic icon resolution. Optional in
                        runtime mode (ghidra_root itself is used).
--module NAME           Convert only the named topic (e.g. DecompilePlugin).
--no-images             Skip image copying.
--verbose, -v           Show detailed progress.
```

## Compatibility

| Ghidra | Runtime mode | Source-tree mode |
|---|---|---|
| 12.0+ | ✅ | ✅ |
| 11.0 – 11.4 | ❌ (PyPI pyghidra requires Ghidra ≥12.0) | ✅ (clone source tag, point `--ghidra-install` at a 12.x install for icons) |

Tested end-to-end on 11.0, 11.3, 12.0.4, 12.1_DEV, and 12.2_DEV.

## Project Structure

```
src/ghidra_help_to_markdown/
  main.py              # Entry point, orchestrates the pipeline
  ghidra_session.py    # Lazy pyghidra session (idempotent start, theme init)
  runtime_help.py      # Reads merged help model from running Ghidra JVM
  toc_parser.py        # Parses TOC_Source.xml into a TOC tree (source mode)
  html_converter.py    # HTML to Markdown body conversion
  link_resolver.py     # help/topics/... -> relative Markdown paths
  icon_resolver.py     # Resolves icon refs via HelpBuildUtils + classpath
  generate_full_index.py  # Expands index.md with each page's headers
  validator.py         # Standalone link/anchor/render checker
```

## Conversion Pipeline

In runtime mode:

1. **JVM bootstrap** — start pyghidra, init `HeadlessThemeManager`, call
   `GhidraHelpService.install()` to merge every `<Module>_HelpSet.hs`.
2. **TOC walk** — traverse the merged TOC tree from `getMasterHelpSet()`.
3. **Topic enumeration** — iterate every loaded HelpSet's local map for
   the full cross-module topic list (~2700 topics on a real install).
4. **HTML fetch** — read each topic's bytes via `URL.openStream()` on its
   `jar:file:.../!/help/topics/...` URL.
5. **HTML to Markdown** — `html_converter.py` handles headings, tables,
   lists, code fences, definition lists (pandoc style), callouts
   (note/tip/warning), keyboard shortcuts, clickable images.
6. **Link resolution** — rewrite `help/topics/X/Y.htm#anchor` to relative
   `X/Y.md#slug` paths, slugifying anchors to match GFM heading slugs.
7. **Icon resolution** — programmatic refs (`Icons.X`, `icon.X`) and
   jar-root images (`<img src="images/icon_link.gif">`) go through
   `HelpBuildUtils.locateImageReference` and `ResourceManager.getResource`,
   with extracted bytes cached and copied to `docs/.../icons/`.
8. **Image extraction** — pull `help/topics/<topic>/images/*` and
   `help/shared/*` out of the module jars into the matching output paths.
9. **External docs** — convert `WhatsNew`, `ChangeHistory`, `README_PDB`,
   `InstallationGuide` (the Ghidra-source format varies: HTML on 11.x,
   Markdown on 12.x — both handled).
10. **Index + nav** — generate master `index.md`, per-module `index.md`s,
    breadcrumbs and prev/next links, plus `index-full.md` with every
    page's headers.

In source-tree mode, steps 1–4 are replaced by direct filesystem walking
of `**/src/main/help/help/topics/`; everything else is identical.

## Output

```
docs/Ghidra_<version>/
  index.md              # Master TOC
  index-full.md         # Full TOC expanded with every page's headers
  icons/                # Resolved icons (jar-extracted + theme-resolved)
  images/               # Logo + master-index images
  shared/               # Shared images (note.png, etc.)
  docs/                 # External docs (WhatsNew, ChangeHistory, README_PDB)
  Misc/Tips.md          # Tip-of-the-Day (generated from tips.txt)
  <Topic>/
    index.md            # Topic index
    *.md                # Converted help pages
    images/             # Topic-specific images
```

## Validation

```bash
# Quick built-in checker (run automatically as the last conversion step)
uv run ghidra-docs-validator ./docs/Ghidra_12.0.4_PUBLIC

# Render + link/anchor check via mkdocs. Wraps `mkdocs build --strict`
# and fails on any warning (broken anchor, unknown nav file, missing
# fragment). Run this after every converter change or doc edit.
./scripts/check_links.sh
```

The built-in validator catches broken internal links, malformed tables,
unmatched bold/backtick markers, missing image files, and same-line
anchor+heading rendering bugs. `mkdocs build --strict` additionally
validates every `[text](path.md#anchor)` reference against the rendered
heading slugs and any `<a name>` markup in the target file (configured
via `validation:` in `mkdocs.yml`).
