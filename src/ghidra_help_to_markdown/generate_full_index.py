#!/usr/bin/env python3
"""Generate index-full.md with links to all document headers.

This script reads the generated index.md and expands it to include
links to every header within each linked document.
"""

import re
from pathlib import Path
from typing import Optional

from .html_converter import slugify


def extract_headers(md_path: Path) -> list[tuple[int, str, str]]:
    """Extract all headers from a markdown file.

    Args:
        md_path: Path to the markdown file

    Returns:
        List of (level, text, slug) tuples for each header
    """
    headers = []
    if not md_path.exists():
        return headers

    content = md_path.read_text(encoding="utf-8")
    for line in content.splitlines():
        # Match markdown headers (# ## ### etc)
        match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if match:
            hashes = match.group(1)
            text = match.group(2).strip()
            level = len(hashes)
            slug = slugify(text)
            headers.append((level, text, slug))

    return headers


def parse_index_entry(line: str) -> Optional[dict]:
    """Parse a single index.md line into structured data.

    Args:
        line: A line from index.md

    Returns:
        Dict with indent, text, path, anchor or None if not a link line
    """
    # Match list items with markdown links: "- [Text](path.md)" or "  - [Text](path.md#anchor)"
    match = re.match(r"^(\s*)-\s+\[([^\]]+)\]\(([^)]+)\)\s*$", line)
    if not match:
        return None

    indent = len(match.group(1))
    text = match.group(2)
    full_path = match.group(3)

    # Split path and anchor
    if "#" in full_path:
        path, anchor = full_path.split("#", 1)
    else:
        path = full_path
        anchor = None

    return {
        "indent": indent,
        "text": text,
        "path": path,
        "anchor": anchor,
        "full_path": full_path,
    }


def generate_full_index(docs_dir: Path) -> str:
    """Generate the full index content with all document headers.

    Args:
        docs_dir: Path to the docs directory containing index.md

    Returns:
        The generated index-full.md content
    """
    index_path = docs_dir / "index.md"
    if not index_path.exists():
        raise FileNotFoundError(f"index.md not found at {index_path}")

    content = index_path.read_text(encoding="utf-8")
    lines = content.splitlines()

    output_lines = []
    processed_files: set[str] = set()  # Track which files we've expanded

    for line in lines:
        entry = parse_index_entry(line)

        if entry is None:
            # Not a link line, keep as-is
            output_lines.append(line)
            continue

        # Check if this links to a markdown file (not an anchor-only link)
        path = entry["path"]
        if not path or not path.endswith(".md"):
            output_lines.append(line)
            continue

        # Skip docs/ folder links (external docs like WhatsNew.md)
        if path.startswith("docs/"):
            output_lines.append(line)
            continue

        # Check if we've already expanded this file
        if path in processed_files:
            # Skip duplicate file references - they were already expanded
            continue

        # Add the original entry
        output_lines.append(line)
        processed_files.add(path)

        # Get headers from the linked file
        md_file = docs_dir / path
        headers = extract_headers(md_file)

        if not headers:
            continue

        # Add each header as a sub-item
        base_indent = entry["indent"] + 2  # Indent under the document entry
        for level, text, slug in headers:
            # Create indentation: base + extra for nested headers
            header_indent = base_indent + (level - 1) * 2
            indent_str = " " * header_indent

            # Build the link
            link_path = f"{path}#{slug}"
            header_line = f"{indent_str}- [{text}]({link_path})"
            output_lines.append(header_line)

    return "\n".join(output_lines) + "\n"


def main() -> None:
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate index-full.md with links to all document headers")
    parser.add_argument("docs_dir", nargs="?", default="./docs", help="Path to the docs directory (default: ./docs)")
    args = parser.parse_args()

    docs_dir = Path(args.docs_dir)
    if not docs_dir.exists():
        print(f"Error: docs directory not found at {docs_dir}")
        return 1

    try:
        content = generate_full_index(docs_dir)
        output_path = docs_dir / "index-full.md"
        output_path.write_text(content, encoding="utf-8")
        print(f"Generated {output_path}")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
