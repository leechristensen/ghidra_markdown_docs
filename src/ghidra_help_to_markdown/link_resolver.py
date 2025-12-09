"""
Link Resolver for Ghidra help to Markdown conversion.

Maps HTML paths to Markdown paths and resolves cross-references.
"""

import re
from pathlib import Path
from typing import Optional

from .html_converter import slugify


class LinkResolver:
    """Resolves and transforms links in converted Markdown content."""

    def __init__(self) -> None:
        # Map from help/topics/... paths to output markdown paths
        self.html_to_md_map: dict[str, str] = {}
        # Map from help/topics/... paths to source file paths
        self.html_to_source: dict[str, Path] = {}

    def add_mapping(self, html_path: str, md_path: str, source_path: Optional[Path] = None) -> None:
        """Add a mapping from HTML path to Markdown path."""
        # Normalize paths
        html_path = html_path.replace("\\", "/")
        md_path = md_path.replace("\\", "/")

        self.html_to_md_map[html_path] = md_path
        if source_path:
            self.html_to_source[html_path] = source_path

    def resolve_link(self, href: str, current_md_path: str) -> str:
        """
        Resolve a link from the original HTML to the new Markdown structure.

        Args:
            href: The original href value (e.g., "help/topics/Tool/Configure_Tool.htm")
            current_md_path: The current Markdown file path (for relative resolution)

        Returns:
            The resolved href for the Markdown file
        """
        if not href:
            return href

        # Handle external URLs
        if href.startswith(("http://", "https://", "mailto:", "ftp://")):
            return href

        # Handle anchor-only links - slugify for markdown compatibility
        if href.startswith("#"):
            slug = slugify(href[1:])
            return "#" + slug if slug else href

        # Normalize the href
        href = href.replace("\\", "/")

        # Split off anchor if present - slugify for markdown compatibility
        anchor = ""
        if "#" in href:
            href, anchor_text = href.split("#", 1)
            slug = slugify(anchor_text)
            anchor = "#" + slug if slug else ""

        # Handle help/topics/ paths
        if href.startswith("help/topics/"):
            return self._resolve_help_path(href, anchor, current_md_path)

        # Handle help/shared/ paths (images)
        if href.startswith("help/shared/"):
            # These are shared images, keep the path structure
            return href + anchor

        # Handle docs/ paths (like docs/WhatsNew.html, docs/README_PDB.html)
        if href.startswith("docs/"):
            # External docs - convert to relative path from current location
            # PDB.md is in Pdb/, docs are in docs/, so need ../docs/
            doc_name = href[5:]  # Remove "docs/" prefix
            if doc_name.endswith(".html"):
                doc_name = doc_name[:-5] + ".md"
            elif doc_name.endswith(".htm"):
                doc_name = doc_name[:-4] + ".md"
            # Calculate relative path to docs/ folder
            current_dir = Path(current_md_path).parent
            depth = len(current_dir.parts) if current_dir.parts and current_dir.parts[0] != "." else 0
            relative_prefix = "../" * depth if depth > 0 else ""
            return f"{relative_prefix}docs/{doc_name}" + anchor

        # Handle relative paths
        return self._resolve_relative_path(href, anchor, current_md_path)

    def _resolve_help_path(self, href: str, anchor: str, current_md_path: str) -> str:
        """Resolve a help/topics/... path."""
        # Check if we have a mapping for this file
        if href in self.html_to_md_map:
            md_path = self.html_to_md_map[href]
            # Make it relative to current file
            return self._make_relative(md_path, current_md_path) + anchor

        # Try with different extensions
        for ext in [".htm", ".html", ""]:
            test_path = href
            if not href.endswith((".htm", ".html")):
                test_path = href + ext

            if test_path in self.html_to_md_map:
                md_path = self.html_to_md_map[test_path]
                return self._make_relative(md_path, current_md_path) + anchor

        # No mapping found, convert path structure
        # help/topics/PluginName/File.htm -> PluginName/File.md
        if href.startswith("help/topics/"):
            path = href[len("help/topics/") :]
            # Change extension (but not for images)
            image_extensions = (".png", ".gif", ".jpg", ".jpeg", ".bmp", ".svg", ".ico")
            if path.endswith(".htm"):
                path = path[:-4] + ".md"
            elif path.endswith(".html"):
                path = path[:-5] + ".md"
            elif not path.lower().endswith(image_extensions):
                # Only add .md if not an image file
                path = path + ".md"
            return self._make_relative(path, current_md_path) + anchor

        return href + anchor

    def _resolve_relative_path(self, href: str, anchor: str, current_md_path: str) -> str:
        """Resolve a relative path."""
        # Handle images/ subdirectory
        if href.startswith("images/"):
            return href + anchor

        # Handle relative paths that eventually reach help/topics/
        # e.g., ../../../help/topics/FrontEndPlugin/File.htm
        if "help/topics/" in href:
            # Extract the path after help/topics/
            idx = href.find("help/topics/")
            help_path = "help/topics/" + href[idx + len("help/topics/") :]
            return self._resolve_help_path(help_path, anchor, current_md_path)

        # Handle docs/ paths (like ../docs/README_PDB.html)
        if "docs/" in href and "README_PDB" in href:
            # Special case for README_PDB which is in docs/ folder
            return "../docs/README_PDB.md" + anchor

        # Convert extension if needed
        if href.endswith(".htm"):
            href = href[:-4] + ".md"
        elif href.endswith(".html"):
            href = href[:-5] + ".md"

        return href + anchor

    def _make_relative(self, target_path: str, current_path: str) -> str:
        """Make target_path relative to current_path."""
        # Get directory of current file
        current_dir = Path(current_path).parent

        # Get target path
        target = Path(target_path)

        try:
            # Calculate relative path
            relative = Path(target).relative_to(current_dir)
            return str(relative).replace("\\", "/")
        except ValueError:
            # Paths don't share a common base, use ../ navigation
            current_parts = current_dir.parts
            target_parts = target.parts

            # Find common prefix
            common_len = 0
            for i, (c, t) in enumerate(zip(current_parts, target_parts)):
                if c == t:
                    common_len = i + 1
                else:
                    break

            # Build relative path
            up_count = len(current_parts) - common_len
            down_parts = target_parts[common_len:]

            relative_parts = [".."] * up_count + list(down_parts)
            return "/".join(relative_parts)

    def transform_markdown_links(self, markdown: str, current_md_path: str) -> str:
        """Transform all links in a Markdown document."""
        # Pattern for markdown links: [text](url)
        link_pattern = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")

        def replace_link(match: re.Match[str]) -> str:
            text = match.group(1)
            href = match.group(2)
            new_href = self.resolve_link(href, current_md_path)
            return f"[{text}]({new_href})"

        markdown = link_pattern.sub(replace_link, markdown)

        # Pattern for image links: ![alt](src)
        img_pattern = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")

        def replace_img(match: re.Match[str]) -> str:
            alt = match.group(1)
            src = match.group(2)
            new_src = self.resolve_image_link(src, current_md_path)
            return f"![{alt}]({new_src})"

        markdown = img_pattern.sub(replace_img, markdown)

        return markdown

    def resolve_image_link(self, src: str, current_md_path: str) -> str:
        """Resolve an image link."""
        if not src:
            return src

        # Handle external URLs
        if src.startswith(("http://", "https://")):
            return src

        src = src.replace("\\", "/")

        # Handle help/shared/ images
        if src.startswith("help/shared/"):
            # Convert to relative path from current location
            # These will be copied to a shared/ folder in output
            filename = Path(src).name
            return f"../shared/{filename}"

        # Handle help/topics/*/images/ paths
        if src.startswith("help/topics/"):
            # Extract the relative path
            path = src[len("help/topics/") :]
            # The image will be in the same directory structure
            return self._make_relative(path, current_md_path)

        # Handle relative images/ paths
        if src.startswith("images/"):
            return src

        return src


def build_link_resolver(html_files: dict[str, list], output_base: str = "") -> LinkResolver:
    """
    Build a LinkResolver from a mapping of HTML files.

    Args:
        html_files: Dict mapping help/topics/... paths to TOCEntry lists
        output_base: Base path for output files

    Returns:
        Configured LinkResolver
    """
    resolver = LinkResolver()

    for html_path in html_files.keys():
        # Convert help/topics/PluginName/File.htm -> PluginName/File.md
        if html_path.startswith("help/topics/"):
            md_path = html_path[len("help/topics/") :]
        else:
            md_path = html_path

        # Change extension
        if md_path.endswith(".htm"):
            md_path = md_path[:-4] + ".md"
        elif md_path.endswith(".html"):
            md_path = md_path[:-5] + ".md"
        else:
            md_path = md_path + ".md"

        if output_base:
            md_path = f"{output_base}/{md_path}"

        resolver.add_mapping(html_path, md_path)

    return resolver


if __name__ == "__main__":
    # Test the link resolver
    resolver = LinkResolver()

    # Add some test mappings
    resolver.add_mapping("help/topics/Tool/Configure_Tool.htm", "Tool/Configure_Tool.md")
    resolver.add_mapping("help/topics/Intro/Intro.htm", "Intro/Intro.md")

    # Test link resolution
    current = "Intro/Intro.md"

    test_links = [
        "help/topics/Tool/Configure_Tool.htm",
        "help/topics/Intro/Intro.htm#GettingStarted",
        "#anchor",
        "images/screenshot.png",
        "help/shared/tip.png",
        "https://example.com",
    ]

    print(f"Current file: {current}\n")
    for link in test_links:
        resolved = resolver.resolve_link(link, current)
        print(f"  {link}")
        print(f"    -> {resolved}\n")

    # Test markdown transformation
    markdown = """
# Test

See [configuring](help/topics/Tool/Configure_Tool.htm) a tool.

Check the [intro](help/topics/Intro/Intro.htm#GettingStarted) section.

![tip](help/shared/tip.png)
"""

    print("\nTransformed markdown:")
    print(resolver.transform_markdown_links(markdown, current))
