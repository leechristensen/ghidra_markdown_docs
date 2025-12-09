# AGENTS.md

## Project Overview

This is a Python CLI tool that converts Ghidra's HTML help documentation to Markdown format with cross-references and navigation.

## Tech Stack

- Python 3.13+
- BeautifulSoup4 + lxml for HTML parsing
- uv for dependency management
- Ruff for linting/formatting

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

## Commands

```bash
# Install dependencies
uv sync

# Run the converter
uv run ghidra-help-to-markdown /path/to/ghidra ./docs

# Validate output for broken links
uv run ghidra-docs-validator ./docs

# Lint and format
uv run ruff check --fix src/
uv run ruff format src/
```

## Key Concepts

1. **TOC Parsing**: Reads `TOC_Source.xml` files from Ghidra modules to build navigation structure
2. **HTML Conversion**: Transforms HTML help files to Markdown preserving structure
3. **Link Resolution**: Converts `help/topics/...` paths to relative Markdown paths
4. **Icon Resolution**: Maps programmatic icon references to actual image files
5. **Validation**: Checks converted docs for broken internal links and missing images

## Code Style

- Line length: 120 characters
- Type annotations required (ANN rules enabled)
- Import sorting via Ruff
- Double quotes for strings
- Do NOT use emojis in code, comments, or documentation

### Comments

- Keep comments minimal - code should be self-explanatory
- Only add comments for complex logic or non-obvious behavior
- Avoid redundant single-line comments that just restate what the code does
- When removing or changing code, do NOT add comments explaining what was removed or changed. Just make the change cleanly without leaving comment breadcrumbs about the old behavior