# Ghidra Help to Markdown Converter

Converts Ghidra's HTML help documentation to Markdown with best-effort cross-references and navigation. 

Vibe coded and several things are probably broken, but does a pretty decent job!

## Quick Start

```bash
uv sync
uv run ghidra-help-to-markdown /path/to/ghidra ./docs
```

Options:
- `--module <name>` - Convert only a specific module (e.g., `DecompilePlugin`)
- `--no-images` - Skip image copying
- `--verbose` - Show detailed output


Example for a tagged Ghidra release:
```bash
git clone https://github.com/NationalSecurityAgency/ghidra
cd ghidra
git checkout Ghidra_12.0_build

cd ..
uv run ghidra-help-to-markdown /path/to/ghidra ./docs/Ghidra_12.0
```

## Project Structure

```
src/ghidra_help_to_markdown/
  main.py              # Entry point, orchestrates conversion pipeline
  toc_parser.py        # Parses TOC_Source.xml files into unified TOC tree
  html_converter.py    # Converts HTML to Markdown (tables, lists, formatting)
  link_resolver.py     # Maps help/topics/... paths to Markdown paths
  icon_resolver.py     # Resolves programmatic icon refs (Icons.*, icon.*)
  generate_full_index.py  # Generates index-full.md with all headers
  validator.py         # Validates converted docs for broken links
```

## Conversion Pipeline

1. **TOC Parsing** - Finds all `TOC_Source.xml` files and builds a unified table of contents. The Base module defines root structure; other modules insert via `<tocref>`.

2. **Anchor Collection** - Scans all HTML files to find which anchors are actually referenced, so only needed anchors are preserved.

3. **HTML Conversion** - Converts each HTML file to Markdown: headings, tables, lists, images, links, and special patterns (notes, tips, warnings).

4. **Link Resolution** - Transforms `help/topics/...` paths to relative Markdown paths and slugifies anchors.

5. **Icon Resolution** - Maps programmatic icon references (`Icons.ADD_ICON`, `icon.bsim.connected`) to actual image files via `Icons.java` and `*.theme.properties`.

6. **Index Generation** - Creates master `index.md` with full TOC and per-module indexes.

7. **Navigation** - Adds breadcrumbs and prev/next links to each page.

## Output

```
docs/
  index.md           # Master table of contents
  icons/             # Resolved icon images
  images/            # Shared images (logo, etc.)
  <Module>/
    index.md         # Module index
    *.md             # Converted help pages
```

## Validation

```bash
uv run ghidra-docs-validator ./docs
```

Checks for broken internal links and missing images.
