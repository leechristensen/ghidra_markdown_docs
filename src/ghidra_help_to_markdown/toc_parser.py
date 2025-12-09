"""
TOC Parser for Ghidra's help system.

Parses TOC_Source.xml files and builds a unified table of contents tree.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from xml.etree import ElementTree as ET


@dataclass
class TOCEntry:
    """Represents a single entry in the table of contents."""

    id: str
    text: str
    target: Optional[str] = None  # HTML file path (help/topics/...)
    anchor: Optional[str] = None  # #section anchor
    sortgroup: str = ""
    children: list["TOCEntry"] = field(default_factory=list)
    module_path: Optional[Path] = None  # Source module location

    def __post_init__(self) -> None:
        # Extract anchor from target if present
        if self.target and "#" in self.target:
            self.target, self.anchor = self.target.split("#", 1)
        # Use text as sortgroup if not specified
        if not self.sortgroup:
            self.sortgroup = self.text


@dataclass
class TOCTree:
    """The complete table of contents tree."""

    entries: list[TOCEntry] = field(default_factory=list)
    definitions: dict[str, TOCEntry] = field(default_factory=dict)  # id -> entry mapping


def find_toc_files(ghidra_root: Path) -> list[Path]:
    """Find all TOC_Source.xml files in the Ghidra source tree."""
    pattern = "**/src/main/help/help/TOC_Source.xml"
    return sorted(ghidra_root.glob(pattern))


def get_module_name(toc_path: Path) -> str:
    """Extract module name from TOC file path."""
    # Path is like: .../Ghidra/Features/Decompiler/src/main/help/help/TOC_Source.xml
    # We want to get the module name (e.g., "Decompiler")
    parts = toc_path.parts
    try:
        src_idx = parts.index("src")
        if src_idx >= 1:
            return parts[src_idx - 1]
    except ValueError:
        pass
    return toc_path.parent.parent.parent.parent.name


def parse_tocdef(element: ET.Element, module_path: Path) -> TOCEntry:
    """Parse a tocdef element into a TOCEntry."""
    entry = TOCEntry(
        id=element.get("id", ""),
        text=element.get("text", ""),
        target=element.get("target"),
        sortgroup=element.get("sortgroup", ""),
        module_path=module_path,
    )

    # Parse children (both tocdef and tocref)
    for child in element:
        if child.tag == "tocdef":
            entry.children.append(parse_tocdef(child, module_path))
        # tocref children will be resolved later

    return entry


def parse_toc_file(toc_path: Path) -> tuple[list[TOCEntry], dict[str, TOCEntry], list[tuple[str, list[TOCEntry]]]]:
    """
    Parse a single TOC_Source.xml file.

    Returns:
        - List of top-level entries (for files that define new content)
        - Dict of all tocdef definitions (id -> entry)
        - List of tocref insertions (parent_id, children_to_insert)
    """
    tree = ET.parse(toc_path)
    root = tree.getroot()

    module_path = toc_path.parent  # help/ directory

    entries: list[TOCEntry] = []
    definitions: dict[str, TOCEntry] = {}
    insertions: list[tuple[str, list[TOCEntry]]] = []

    def collect_definitions(entry: TOCEntry) -> None:
        """Recursively collect all definitions."""
        if entry.id:
            definitions[entry.id] = entry
        for child in entry.children:
            collect_definitions(child)

    def process_element(element: ET.Element) -> list[TOCEntry]:
        """Process an element and its children."""
        result = []

        for child in element:
            if child.tag == "tocdef":
                entry = parse_tocdef(child, module_path)
                collect_definitions(entry)
                result.append(entry)
            elif child.tag == "tocref":
                # This references a tocdef from another module
                ref_id = child.get("id", "")
                # Get children of this tocref
                children = process_element(child)
                if children:
                    insertions.append((ref_id, children))

        return result

    entries = process_element(root)

    return entries, definitions, insertions


def sort_entries(entries: list[TOCEntry]) -> list[TOCEntry]:
    """Sort entries by sortgroup."""
    sorted_entries = sorted(entries, key=lambda e: e.sortgroup)
    for entry in sorted_entries:
        entry.children = sort_entries(entry.children)
    return sorted_entries


def build_toc_tree(ghidra_root: Path) -> TOCTree:
    """
    Build a complete TOC tree from all TOC_Source.xml files.

    The Base module defines the root structure, and other modules
    insert their content using tocref.
    """
    toc_files = find_toc_files(ghidra_root)

    all_definitions: dict[str, TOCEntry] = {}
    all_insertions: list[tuple[str, list[TOCEntry]]] = []
    root_entries: list[TOCEntry] = []

    # First pass: parse all files
    for toc_path in toc_files:
        module_name = get_module_name(toc_path)
        print(f"Parsing TOC: {module_name}")

        entries, definitions, insertions = parse_toc_file(toc_path)

        all_definitions.update(definitions)
        all_insertions.extend(insertions)

        # Check if this is the base module (has Root reference)
        # Files that reference "Root" are adding to the top level
        for parent_id, children in insertions:
            if parent_id == "Root":
                root_entries.extend(children)

    # Second pass: resolve all tocref insertions
    for parent_id, children in all_insertions:
        if parent_id == "Root":
            continue  # Already handled

        if parent_id in all_definitions:
            parent = all_definitions[parent_id]
            parent.children.extend(children)
            # Also add new definitions
            for child in children:

                def add_to_defs(entry: TOCEntry) -> None:
                    if entry.id:
                        all_definitions[entry.id] = entry
                    for c in entry.children:
                        add_to_defs(c)

                add_to_defs(child)

    # Sort all entries
    root_entries = sort_entries(root_entries)

    return TOCTree(entries=root_entries, definitions=all_definitions)


def flatten_toc(tree: TOCTree) -> list[TOCEntry]:
    """Flatten the TOC tree into a list for sequential navigation."""
    result: list[TOCEntry] = []

    def visit(entry: TOCEntry) -> None:
        result.append(entry)
        for child in entry.children:
            visit(child)

    for entry in tree.entries:
        visit(entry)

    return result


def get_unique_html_files(tree: TOCTree) -> dict[str, list[TOCEntry]]:
    """
    Get all unique HTML files referenced in the TOC.

    Returns a dict mapping HTML file paths to the TOC entries that reference them.
    """
    files: dict[str, list[TOCEntry]] = {}

    def visit(entry: TOCEntry) -> None:
        if entry.target:
            # Normalize the path
            target = entry.target.replace("\\", "/")
            if target not in files:
                files[target] = []
            files[target].append(entry)

        for child in entry.children:
            visit(child)

    for entry in tree.entries:
        visit(entry)

    return files


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m ghidra_help_to_markdown.toc_parser <ghidra_root>")
        sys.exit(1)

    ghidra_root = Path(sys.argv[1])

    print(f"Building TOC tree from {ghidra_root}")
    tree = build_toc_tree(ghidra_root)

    print(f"\nFound {len(tree.definitions)} TOC definitions")
    print(f"Root entries: {len(tree.entries)}")

    html_files = get_unique_html_files(tree)
    print(f"Unique HTML files: {len(html_files)}")

    # Print the tree structure
    def print_tree(entries: list[TOCEntry], indent: int = 0) -> None:
        for entry in entries:
            prefix = "  " * indent
            target_info = f" -> {entry.target}" if entry.target else ""
            print(f"{prefix}- {entry.text}{target_info}")
            print_tree(entry.children, indent + 1)

    print("\nTOC Structure:")
    print_tree(tree.entries)
