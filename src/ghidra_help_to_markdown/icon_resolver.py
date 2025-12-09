"""
Icon resolver for Ghidra help documentation.

Resolves programmatic icon references (like Icons.ADD_ICON or icon.bsim.connected)
to actual image file paths by parsing:
1. Icons.java - Maps field names (ADD_ICON) to icon IDs (icon.add)
2. *.theme.properties - Maps icon IDs to filenames (Plus2.png)
3. */src/main/resources/images/ - Actual icon files
"""

import re
from pathlib import Path
from typing import Optional


class IconResolver:
    """Resolve Ghidra icon references to actual image files."""

    # Fallback mappings for composite icons that can't be resolved directly
    # These icons are defined as EMPTY_ICON{...} with transformations
    COMPOSITE_ICON_FALLBACKS = {
        "icon.undo": "edit-undo.png",
        "icon.redo": "edit-redo.png",
    }

    def __init__(self, ghidra_root: Path) -> None:
        """
        Initialize the icon resolver.

        Args:
            ghidra_root: Path to the Ghidra repository root
        """
        self.ghidra_root = ghidra_root
        self.icons_field_to_id: dict[str, str] = {}  # ADD_ICON → icon.add
        self.id_to_filename: dict[str, str] = {}  # icon.add → Plus2.png
        self.filename_to_path: dict[str, list[Path]] = {}  # Plus2.png → [full paths]
        self._load_mappings()

    def _load_mappings(self) -> None:
        """Load all icon mappings from the Ghidra codebase."""
        self._parse_icons_java()
        self._parse_theme_properties()
        self._find_icon_files()

    def _parse_icons_java(self) -> None:
        """Parse Icons.java to extract field name → icon.id mappings."""
        icons_java = self.ghidra_root / "Ghidra/Framework/Gui/src/main/java/resources/Icons.java"
        if not icons_java.exists():
            return

        content = icons_java.read_text(encoding="utf-8")

        # Match: public static final Icon ADD_ICON = new GIcon("icon.add");
        pattern = re.compile(r'public\s+static\s+final\s+Icon\s+(\w+)\s*=\s*new\s+GIcon\s*\(\s*"([^"]+)"\s*\)')

        for match in pattern.finditer(content):
            field_name = match.group(1)  # ADD_ICON
            icon_id = match.group(2)  # icon.add
            self.icons_field_to_id[field_name] = icon_id

    def _parse_theme_properties(self) -> None:
        """Parse all theme.properties files to extract icon.id → filename mappings."""
        # Find all theme properties files
        for props_file in self.ghidra_root.glob("Ghidra/**/data/*.theme.properties"):
            self._parse_properties_file(props_file)

    def _parse_properties_file(self, props_file: Path) -> None:
        """Parse a single theme.properties file."""
        try:
            content = props_file.read_text(encoding="utf-8")
        except Exception:
            return

        # Skip section headers and comments, parse icon.* = value lines
        for line in content.split("\n"):
            line = line.strip()

            # Skip comments and section headers
            if not line or line.startswith("//") or line.startswith("["):
                continue

            # Parse: icon.add = Plus2.png
            if line.startswith("icon.") and "=" in line:
                parts = line.split("=", 1)
                if len(parts) == 2:
                    icon_id = parts[0].strip()
                    value = parts[1].strip()

                    # Handle transformations like: icon.arrow.down.right = viewmagfit.png[rotate(90)]
                    # Extract just the filename
                    if "[" in value:
                        value = value.split("[")[0].strip()

                    # Handle icon aliases like: icon.base.delete = icon.delete
                    # We'll resolve these later
                    self.id_to_filename[icon_id] = value

        # Resolve icon aliases (icon.base.delete = icon.delete)
        self._resolve_icon_aliases()

    def _resolve_icon_aliases(self) -> None:
        """Resolve icon aliases that point to other icons."""
        max_iterations = 10  # Prevent infinite loops
        for _ in range(max_iterations):
            changed = False
            for icon_id, value in list(self.id_to_filename.items()):
                # If value is another icon reference, resolve it
                if value.startswith("icon."):
                    if value in self.id_to_filename:
                        resolved = self.id_to_filename[value]
                        if not resolved.startswith("icon."):
                            self.id_to_filename[icon_id] = resolved
                            changed = True
            if not changed:
                break

    def _find_icon_files(self) -> None:
        """Build an index of filename → actual file paths (list for duplicates)."""
        # Search all resources/images directories
        for img_dir in self.ghidra_root.glob("Ghidra/**/src/main/resources/images"):
            for img_file in img_dir.glob("**/*"):
                if img_file.is_file():
                    # Store all paths per filename to handle duplicates
                    if img_file.name not in self.filename_to_path:
                        self.filename_to_path[img_file.name] = []
                    self.filename_to_path[img_file.name].append(img_file)

    def resolve(self, src: str) -> Optional[Path]:
        """
        Resolve an icon reference to an actual file path.

        Args:
            src: Icon reference like "Icons.ADD_ICON" or "icon.bsim.connected"

        Returns:
            Path to the actual icon file, or None if not found
        """
        icon_id = None

        # Handle Icons.FIELD_NAME format
        if src.startswith("Icons."):
            field_name = src[6:]  # Remove "Icons." prefix
            icon_id = self.icons_field_to_id.get(field_name)
        # Handle icon.id format directly
        elif src.startswith("icon."):
            icon_id = src

        if not icon_id:
            return None

        # Look up the filename for this icon ID
        filename = self.id_to_filename.get(icon_id)
        if not filename:
            return None

        # Check for composite icon fallbacks before skipping EMPTY_ICON definitions
        if icon_id in self.COMPOSITE_ICON_FALLBACKS:
            fallback_filename = self.COMPOSITE_ICON_FALLBACKS[icon_id]
            paths = self.filename_to_path.get(fallback_filename)
            if paths:
                return paths[0]

        # Handle complex icon definitions (EMPTY_ICON {...} {...})
        # Just skip these for now
        if filename.startswith("EMPTY_ICON") or "{" in filename:
            return None

        # Look up the actual file path (return first match)
        paths = self.filename_to_path.get(filename)
        return paths[0] if paths else None

    def resolve_by_filename(self, filename: str, source_path: Optional[Path] = None) -> Optional[Path]:
        """
        Resolve an icon by filename, preferring icons from the same module.

        Args:
            filename: Icon filename (e.g., "editbytes.gif")
            source_path: Optional source help file path for module-aware resolution

        Returns:
            Path to the icon file, or None if not found
        """
        paths = self.filename_to_path.get(filename)
        if not paths:
            return None

        if len(paths) == 1:
            return paths[0]

        # Multiple paths - try to match module from source path
        if source_path:
            # Extract module path: Ghidra/Features/{Module}/src/main/help/...
            # Looking for:         Ghidra/Features/{Module}/src/main/resources/images/
            source_str = str(source_path).replace("\\", "/")
            if "/src/main/help/" in source_str:
                module_prefix = source_str.split("/src/main/help/")[0]
                for path in paths:
                    path_str = str(path).replace("\\", "/")
                    if module_prefix in path_str:
                        return path

        # Fall back to first available
        return paths[0]

    def get_stats(self) -> dict:
        """Get statistics about loaded icon mappings."""
        return {
            "icons_field_to_id": len(self.icons_field_to_id),
            "id_to_filename": len(self.id_to_filename),
            "filename_to_path": len(self.filename_to_path),
        }


if __name__ == "__main__":
    # Test the icon resolver
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m ghidra_help_to_markdown.icon_resolver <ghidra_root>")
        sys.exit(1)

    ghidra_root = Path(sys.argv[1])
    resolver = IconResolver(ghidra_root)

    print("Icon Resolver Statistics:")
    stats = resolver.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # Test some common icons
    test_icons = [
        "Icons.ADD_ICON",
        "Icons.DELETE_ICON",
        "Icons.CONFIGURE_FILTER_ICON",
        "Icons.INFO_ICON",
        "icon.bsim.connected",
        "icon.bsim.disconnected",
        "icon.bsim.query.dialog.provider",
        "icon.undo",
        "icon.redo",
    ]

    print("\nTest resolutions:")
    for icon in test_icons:
        resolved = resolver.resolve(icon)
        if resolved:
            print(f"  {icon} -> {resolved.name}")
        else:
            print(f"  {icon} -> NOT FOUND")
