"""
HTML to Markdown converter for Ghidra help files.

Handles both simple HTML 4.01 and DocBook-generated HTML formats.
"""

import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from bs4 import BeautifulSoup, NavigableString, Tag

if TYPE_CHECKING:
    from .icon_resolver import IconResolver


@dataclass
class ImageStats:
    """Track image conversion statistics for validation."""

    html_total: int = 0  # Total <img> tags encountered in HTML
    converted_to_text: int = 0  # Images converted to text (arrows, icons, callouts)
    markdown_images: int = 0  # Images that become markdown ![alt](src)


@dataclass
class CodeBlockStats:
    """Track code block conversion statistics for validation."""

    html_pre_tags: int = 0  # Total <pre> tags encountered in HTML
    markdown_code_blocks: int = 0  # Code blocks generated (``` ... ```)


@dataclass
class TableStats:
    """Track table conversion statistics for validation."""

    html_tables: int = 0  # Total <table> tags encountered in HTML
    layout_tables: int = 0  # Tables detected as layout (image-only, single cell)
    content_tables: int = 0  # Tables with actual text content
    markdown_tables: int = 0  # Non-empty markdown tables generated
    blank_tables: int = 0  # Blank markdown tables generated (all cells empty)


def slugify(text: str) -> str:
    """Convert text to GitHub-style anchor slug.

    Examples:
        "Error Dialogs" -> "error-dialogs"
        "Ghidra Overview" -> "ghidra-overview"
        "P-code" -> "p-code"
    """
    # Lowercase
    slug = text.lower()
    # Replace spaces/underscores with hyphens
    slug = re.sub(r"[\s_]+", "-", slug)
    # Remove non-alphanumeric except hyphens
    slug = re.sub(r"[^a-z0-9-]", "", slug)
    # Collapse multiple hyphens
    slug = re.sub(r"-+", "-", slug)
    # Strip leading/trailing hyphens
    return slug.strip("-")


def escape_angle_brackets(text: str) -> str:
    """Escape angle brackets in text to prevent markdown interpreting them as HTML.

    Detects keyboard shortcut patterns like <Home>, <Ctrl><End> and wraps them
    in backticks for code formatting. Other angle brackets are escaped to HTML entities.

    Examples:
        "<Home>" -> "`<Home>`"
        "<Ctrl><Home>" -> "`<Ctrl><Home>`"
        "Press <Enter> to continue" -> "Press `<Enter>` to continue"
        "<script>" -> "&lt;script&gt;"
    """
    # Pattern for keyboard shortcuts: one or more <Key> patterns together
    # Matches: <Home>, <Ctrl><Home>, <Shift><Ctrl><End>, etc.
    keyboard_pattern = re.compile(r"(<[A-Za-z][A-Za-z0-9 ]*>)+")

    def replace_keyboard(match: re.Match[str]) -> str:
        return f"`{match.group(0)}`"

    # First, wrap keyboard shortcuts in backticks
    result = keyboard_pattern.sub(replace_keyboard, text)

    # Then escape any remaining angle brackets that aren't in backticks
    # Split by backtick-delimited sections and only escape non-code parts
    parts = result.split("`")
    for i in range(0, len(parts), 2):  # Even indices are outside backticks
        parts[i] = parts[i].replace("<", "&lt;").replace(">", "&gt;")

    return "`".join(parts)


class HTMLToMarkdownConverter:
    """Converts HTML help files to Markdown."""

    def __init__(
        self,
        used_anchors: Optional[set[str]] = None,
        icon_resolver: Optional["IconResolver"] = None,
        output_dir: Optional[Path] = None,
        source_path: Optional[Path] = None,
        output_md_path: Optional[Path] = None,
    ) -> None:
        """
        Initialize the converter.

        Args:
            used_anchors: Optional set of anchor names that are actually referenced.
                         If provided, only these anchors will be emitted in the output.
                         If None, all anchors are emitted.
            icon_resolver: Optional IconResolver for resolving programmatic icon references.
            output_dir: Optional output directory for copying resolved icons.
            source_path: Optional source HTML file path for module-aware icon resolution.
            output_md_path: Optional output markdown file path for correct relative icon paths.
        """
        self.anchors: list[str] = []  # Collect anchors found in the document
        self.used_anchors = used_anchors  # Only emit anchors in this set
        self.image_stats = ImageStats()  # Track image conversion statistics
        self.code_block_stats = CodeBlockStats()  # Track code block conversion statistics
        self.table_stats = TableStats()  # Track table conversion statistics
        self.icon_resolver = icon_resolver
        self.output_dir = output_dir
        self.source_path = source_path  # For module-aware icon resolution
        self.output_md_path = output_md_path  # For correct relative icon paths
        self._copied_icons: set[str] = set()  # Track icons already copied
        # Map from slugified HTML anchor names to GFM heading slugs
        # e.g., "tailorbsim" -> "tailoring-bsim"
        self.anchor_to_heading_slug: dict[str, str] = {}

    def _preprocess_html(self, html_content: str) -> str:
        """Preprocess HTML to fix common issues in Ghidra help files.

        Fixes:
        - Mismatched heading tags (e.g., <H3>...</H2> -> <H3>...</H3>)
        """
        # Fix mismatched heading closing tags
        # Only match within a single line to avoid corrupting valid multi-line HTML
        # Pattern: <H[1-6] ...>...</H[different number]> on the same line
        # This handles cases like <H3><A name="..."></A>Text</H2>
        for level in range(1, 7):
            for wrong_level in range(1, 7):
                if level != wrong_level:
                    # Match opening H tag and mismatched closing tag on the SAME LINE
                    # [^\n]* ensures we don't match across newlines
                    pattern = re.compile(rf"(<[Hh]{level}[^>]*>)([^\n]*?)(</[Hh]{wrong_level}>)", re.IGNORECASE)
                    html_content = pattern.sub(rf"\g<1>\g<2></h{level}>", html_content)
        return html_content

    def convert(self, html_content: str) -> str:
        """Convert HTML content to Markdown."""
        # Preprocess HTML to fix common issues in Ghidra help files
        html_content = self._preprocess_html(html_content)
        soup = BeautifulSoup(html_content, "html.parser")

        # Find the body content
        body = soup.find("body")
        if not body:
            body = soup

        # Reset state for this document
        self.anchors = []
        self.image_stats = ImageStats()
        self.code_block_stats = CodeBlockStats()
        self.table_stats = TableStats()

        # Convert the content
        markdown = self._convert_element(body)

        # Clean up the result
        markdown = self._cleanup_markdown(markdown)

        return markdown

    def convert_file(self, html_path: Path) -> str:
        """Convert an HTML file to Markdown."""
        # Store source path for module-aware icon resolution
        self.source_path = html_path

        # Try different encodings
        for encoding in ["utf-8", "windows-1252", "iso-8859-1"]:
            try:
                html_content = html_path.read_text(encoding=encoding)
                return self.convert(html_content)
            except UnicodeDecodeError:
                continue

        # Fallback: read with errors ignored
        html_content = html_path.read_text(encoding="utf-8", errors="ignore")
        return self.convert(html_content)

    def validate_image_counts(self) -> tuple[bool, str]:
        """
        Validate that image counts are consistent.

        Returns:
            (is_valid, message) tuple where:
            - is_valid: True if counts match expected, False otherwise
            - message: Description of the validation result
        """
        stats = self.image_stats
        expected_md = stats.html_total - stats.converted_to_text

        if stats.markdown_images == expected_md:
            return True, (
                f"OK: {stats.html_total} HTML images → {stats.converted_to_text} text + {stats.markdown_images} md"
            )
        else:
            diff = expected_md - stats.markdown_images
            return False, (
                f"MISMATCH: {stats.html_total} HTML images, "
                f"{stats.converted_to_text} converted to text, "
                f"expected {expected_md} markdown but got {stats.markdown_images} "
                f"(off by {diff})"
            )

    def validate_code_block_counts(self) -> tuple[bool, str]:
        """
        Validate that code block counts are consistent.

        Returns:
            (is_valid, message) tuple where:
            - is_valid: True if counts match, False otherwise
            - message: Description of the validation result
        """
        stats = self.code_block_stats

        if stats.markdown_code_blocks == stats.html_pre_tags:
            return True, (f"OK: {stats.html_pre_tags} HTML <pre> → {stats.markdown_code_blocks} md code blocks")
        else:
            diff = stats.html_pre_tags - stats.markdown_code_blocks
            return False, (
                f"MISMATCH: {stats.html_pre_tags} HTML <pre> tags, "
                f"but only {stats.markdown_code_blocks} markdown code blocks "
                f"(missing {diff})"
            )

    def validate_table_counts(self) -> tuple[bool, str]:
        """
        Validate table conversion statistics.

        Returns:
            (is_valid, message) tuple where:
            - is_valid: True if no blank content tables, False otherwise
            - message: Description of the validation result
        """
        stats = self.table_stats

        # Check if any content tables became blank (lost their content)
        if stats.blank_tables > 0 and stats.layout_tables < stats.blank_tables:
            # Some content tables may have lost their data
            return False, (
                f"WARNING: {stats.html_tables} HTML tables → "
                f"{stats.markdown_tables} with content, {stats.blank_tables} blank "
                f"(layout: {stats.layout_tables}, content: {stats.content_tables})"
            )
        else:
            return True, (
                f"OK: {stats.html_tables} HTML tables → "
                f"{stats.markdown_tables} with content, {stats.blank_tables} blank/layout"
            )

    def _convert_element(self, element: NavigableString | Tag) -> str:
        """Recursively convert an HTML element to Markdown."""
        if isinstance(element, NavigableString):
            text = str(element)
            # Preserve some whitespace but normalize excessive whitespace
            # Escape angle brackets to prevent markdown interpreting them as HTML
            # (e.g., <Ctrl>, <Shift> keyboard shortcuts in paragraph text)
            return escape_angle_brackets(text)

        if not isinstance(element, Tag):
            return ""

        tag_name = element.name.lower() if element.name else ""

        # Handle different tags
        if tag_name in ("h1", "h2", "h3", "h4", "h5", "h6"):
            return self._convert_heading(element)
        elif tag_name == "p":
            return self._convert_paragraph(element)
        elif tag_name == "a":
            return self._convert_link(element)
        elif tag_name == "img":
            return self._convert_image(element)
        elif tag_name in ("ul", "ol"):
            return self._convert_list(element)
        elif tag_name == "li":
            return self._convert_list_item(element)
        elif tag_name == "table":
            return self._convert_table(element)
        elif tag_name in ("pre", "code"):
            return self._convert_code(element)
        elif tag_name in ("b", "strong"):
            return self._convert_bold(element)
        elif tag_name in ("i", "em"):
            return self._convert_italic(element)
        elif tag_name == "blockquote":
            return self._convert_blockquote(element)
        elif tag_name == "br":
            return "\n"
        elif tag_name == "hr":
            return "\n---\n\n"
        elif tag_name in ("div", "span"):
            return self._convert_div_span(element)
        elif tag_name in ("head", "script", "style", "meta", "link"):
            return ""  # Skip these
        elif tag_name == "tt":
            return self._convert_inline_code(element)
        elif tag_name == "center":
            # Just process children, markdown doesn't have center
            return self._convert_children(element)
        elif tag_name == "tbody":
            return self._convert_children(element)
        else:
            # Default: just convert children
            return self._convert_children(element)

    def _convert_children(self, element: Tag) -> str:
        """Convert all children of an element."""
        result = []
        for child in element.children:
            result.append(self._convert_element(child))
        return "".join(result)

    def _convert_heading(self, element: Tag) -> str:
        """Convert a heading element."""
        level = int(element.name[1])
        prefix = "#" * level

        # Extract ALL anchors from HTML (headings can have multiple anchors)
        # e.g., <H2><A name="Delete_Equate"></A><A name="Remove_Equate"></A>Remove Equate</H2>
        html_anchors = self._extract_all_anchors(element)

        # Get text content and normalize whitespace (HTML headings can span multiple lines)
        text = self._get_text_content(element).strip()
        # Collapse all whitespace (including newlines) to single spaces
        text = " ".join(text.split())

        if not text:
            return ""

        # GitHub-flavored markdown automatically generates anchors from heading text
        # e.g., "## My Section" -> anchor "#my-section"
        heading_slug = slugify(text)

        # Build mapping from HTML anchor slugs to GFM heading slug
        # This allows link resolver to convert old anchor references to correct GFM anchors
        for html_anchor in html_anchors:
            if html_anchor and html_anchor != heading_slug:
                self.anchor_to_heading_slug[html_anchor] = heading_slug

        return f"\n\n{prefix} {text}\n\n"

    def _convert_paragraph(self, element: Tag) -> str:
        """Convert a paragraph element."""
        # Check for special classes
        classes = element.get("class", [])
        if isinstance(classes, str):
            classes = [classes]

        # Check if paragraph starts with a note/tip/warning icon
        # Only check immediate children to avoid matching nested content in malformed HTML
        first_img = element.find("img", recursive=False)
        if first_img:
            src = first_img.get("src", "")
            if "note.png" in src:
                text = element.get_text(separator=" ", strip=True)
                return f"\n\n> **Note:** {text}\n\n"
            elif "tip.png" in src:
                text = element.get_text(separator=" ", strip=True)
                return f"\n\n> **Tip:** {text}\n\n"
            elif "warning.png" in src:
                text = element.get_text(separator=" ", strip=True)
                return f"\n\n> **Warning:** {text}\n\n"

        content = self._convert_children(element).strip()

        if not content:
            return ""

        if "relatedtopic" in classes:
            # Check if this is the header or a link paragraph
            # The header contains "Related Topics:" text, link paragraphs contain actual links
            text = element.get_text(strip=True)
            if text == "Related Topics:" or text.lower().startswith("related topic"):
                return "\n\n**Related Topics:**\n\n"
            # Otherwise, it's a paragraph containing links - convert normally
            return f"\n\n{content}\n\n"
        elif "providedbyplugin" in classes:
            return f"\n\n*{content}*\n\n"

        return f"\n\n{content}\n\n"

    def _convert_link(self, element: Tag) -> str:
        """Convert an anchor element."""
        # Check if this is a named anchor (target for links)
        name = element.get("name")
        if name:
            # Slugify anchor for markdown compatibility (dashes, lowercase)
            slug_name = slugify(name)
            if slug_name:
                self.anchors.append(slug_name)
            # Named anchors can also contain content that needs to be converted
            # e.g., <A name="foo"><B>Title</B> Description</A>
            content = self._convert_children(element).strip()
            # Just return the content - links to anchors should point to nearby headings
            # which GFM auto-anchors based on heading text
            return content

        # Regular link
        href = element.get("href", "")
        text = self._get_text_content(element).strip()

        if not text:
            # Image link or empty
            img = element.find("img")
            if img:
                return self._convert_image(img)
            return ""

        if not href:
            return text

        # Fix malformed paths like "file.htm/#anchor" → "file.htm#anchor"
        href = href.replace("/#", "#")

        return f"[{text}]({href})"

    # Common toolbar/menu icons that are runtime-loaded (not actual files)
    RUNTIME_ICONS = {
        "menu16.gif": "[Menu]",
        "disk.png": "[Save]",
        "edit-delete.png": "[Delete]",
        "Plus.png": "[Add]",
        "go-home.png": "[Home]",
        "go-down.tango.16.png": "[Down]",
        "go-up.tango.16.png": "[Up]",
        "view-filter.png": "[Filter]",
        "notes.gif": "[Note]",
        "wrench.png": "[Settings]",
        "editbytes.gif": "[Edit]",
        "binaryData.gif": "[Binary]",
        "error.png": "[Error]",
        "warning.help.png": "[Warning]",
        "field.header.down.png": "[Expand]",
        "NextSelectionBlock16.gif": "[Next]",
        "PreviousSelectionBlock16.gif": "[Previous]",
        "locationIn.gif": "[Location In]",
        "locationOut.gif": "[Location Out]",
        "locationInOut.gif": "[Location In/Out]",
        "EmptyIcon16.gif": "",
        "Caution.png": "[Caution]",
        "information.png": "[Info]",
        "checkmark_green.gif": "[Check]",
        "reload3.png": "[Reload]",
        "software_install.png": "[Install]",
        "Package.png": "[Package]",
        "collapse_all.gif": "[Collapse All]",
        "collapse_all.png": "[Collapse All]",
        "expand_all.gif": "[Expand All]",
        "doubleArrow.png": " → ",
        "smallRightArrow.png": " → ",
        "smallLeftArrow.png": " ← ",
        "fingerPointer.png": "[Select]",
        "emblem-favorite.png": "[Favorite]",
        "decompileFunction.gif": "[Decompile]",
        "dataTypes.png": "[Data Types]",
        "conflictReplaceOrRename.png": "[Replace/Rename]",
        "conflictReplace.png": "[Replace]",
        "conflictRename.png": "[Rename]",
        "conflictKeep.png": "[Keep]",
        "closedFolderInvalid.png": "[Invalid Folder]",
        "BookShelfOpen.png": "[Library]",
        "Array.png": "[Array]",
        # Version Tracking / Diff icons
        "table_relationship.png": "[Relationship]",
        "up.png": "[Up]",
        "down.png": "[Down]",
        "DiffSelect16.png": "[Diff Select]",
        "Diff16.png": "[Diff]",
        "camera-photo.png": "[Snapshot]",
        "shape_handles.png": "[Handles]",
        "pencil_arrow16.png": "[Edit Arrow]",
        "page_white_copy.png": "[Copy]",
        "eraser_arrow16.png": "[Erase Arrow]",
        "disconnected.gif": "[Disconnected]",
        "connected.gif": "[Connected]",
        "xmag.png": "[Zoom]",
        "window.png": "[Window]",
        "user.png": "[User]",
        "shape_ungroup.png": "[Ungroup]",
        "shape_square_add.png": "[Add Shape]",
        "pencil16.png": "[Pencil]",
        "page_paste.png": "[Paste]",
        "page_edit.png": "[Edit Page]",
        "monitor.png": "[Monitor]",
        "house.png": "[Home]",
        "fullscreen_view.png": "[Fullscreen]",
        "field.header.png": "[Header]",
        "edit-redo.png": "[Redo]",
        "downArrow.png": "[Down]",
        # More misc icons
        "right.png": " → ",
        "left.png": " ← ",
        "lock.gif": "[Lock]",
        "unlock.gif": "[Unlock]",
        "magnifier.png": "[Search]",
        "font.png": "[Font]",
        "dialog-warning_red.png": "[Warning]",
        "V.png": "[V]",
        "unknown.gif": "[Unknown]",
        "U.gif": "[U]",
        "trash-empty.png": "[Delete]",
        "tag_yellow.png": "[Tag]",
        "searchm_obj.gif": "[Search]",
        "reload.png": "[Reload]",
        "registerIcon.png": "[Register]",
        "registerGroup.png": "[Register Group]",
        "preferences-system-windows.png": "[Preferences]",
        "Plus2.png": "[Add]",
        "openSmallFolder.png": "[Open Folder]",
        "openFolderInView.png": "[Open Folder]",
        "notF.gif": "[Not F]",
        "Merge.png": "[Merge]",
        "memory16.gif": "[Memory]",
        "layout_add.png": "[Add Layout]",
        "label.png": "[Label]",
        "L.gif": "[L]",
        "I.gif": "[I]",
        "F.gif": "[F]",
        "expand.gif": "[Expand]",
        "dragMoveCursor.gif": "[Move]",
        "dragCopyCursor.gif": "[Copy]",
        "dialog-cancel.png": "[Cancel]",
        "D.gif": "[D]",
        "core.png": "[Core]",
        "codeNotInView.gif": "[Not In View]",
        "codeInView.gif": "[In View]",
        "closedFolderInView.png": "[Folder In View]",
        "closedDescendantsInView.png": "[Descendants In View]",
        "B.gif": "[B]",
        "applications-system.png": "[System]",
        # Search/Pattern icons
        "edit-clear.png": "[Clear]",
        "DOSA_D.png": "[D]",
        "DOSA_O.png": "[O]",
        "DOSA_S.png": "[S]",
        "DOSA_A.png": "[A]",
        "hexData.png": "[Hex]",
        "PreviousHighlightBlock16.gif": "[Previous Highlight]",
        "NextHighlightBlock16.gif": "[Next Highlight]",
        # Symbol icons
        "table_go.png": "[Go To]",
        "table.png": "[Table]",
        "sitemap_color.png": "[Tree]",
        "openFolderGroup.png": "[Folder Group]",
        # Tool config icons
        "disk_save_as.png": "[Save As]",
        "plugin.png": "[Plugin]",
        # Version control icons
        "vcAdd.png": "[VC Add]",
        "vcCheckOut.png": "[Check Out]",
        "vcCheckIn.png": "[Check In]",
        "vcUndoCheckOut.png": "[Undo Checkout]",
        "vcMerge.png": "[VC Merge]",
        # Version Tracking icons
        "flag.png": "[Flag]",
        "start-here_16.png": "[Start]",
        "settings16.gif": "[Settings]",
        "wizard.png": "[Wizard]",
        "doubleArrowUpDown.png": "[Up/Down]",
        "list-remove.png": "[Remove]",
        "function.png": "[Function]",
        "filter_matched.png": "[Filter Matched]",
        "application_tile_horizontal.png": "[Tile]",
        "lightbulb.png": "[Idea]",
        "tag_blue.png": "[Tag]",
        "tag_blue_delete.png": "[Delete Tag]",
        "tag_blue_edit.png": "[Edit Tag]",
        "undo-apply.png": "[Undo Apply]",
        "table_gear.png": "[Table Settings]",
    }

    def _convert_image(self, element: Tag) -> str:
        """Convert an image element and track conversion statistics."""
        src = element.get("src", "")
        alt = element.get("alt", "")

        # Count every image we encounter
        self.image_stats.html_total += 1

        if not src:
            # Empty src - counts as converted to nothing
            self.image_stats.converted_to_text += 1
            return ""

        # Handle programmatic icon references (Ghidra runtime icons)
        if src.startswith("Icons.") or src.startswith("icon."):
            # Try to resolve to actual icon file
            if self.icon_resolver:
                resolved_path = self.icon_resolver.resolve(src)
                if resolved_path:
                    # Copy icon to output directory and return markdown reference
                    icon_ref = self._copy_icon_to_output(resolved_path)
                    if icon_ref:
                        self.image_stats.markdown_images += 1
                        icon_alt = alt or src.split(".")[-1].replace("_ICON", "").replace("_", " ").title()
                        return f"![{icon_alt}]({icon_ref})"

            # Fallback: return placeholder text
            self.image_stats.converted_to_text += 1
            icon_name = src.split(".")[-1].replace("_ICON", "").replace("_", " ").title()
            return f"[{icon_name}]"

        # Handle arrow images in menu paths - convert to text arrow
        if "arrow.gif" in src or "arrow.png" in src:
            self.image_stats.converted_to_text += 1
            return " → "

        # Extract filename for lookups
        filename = Path(src).name

        # Try to resolve icon by filename BEFORE checking RUNTIME_ICONS
        # This allows actual icon files to be used instead of text placeholders
        if self.icon_resolver and src.startswith("images/"):
            resolved_path = self.icon_resolver.resolve_by_filename(filename, self.source_path)
            if resolved_path and resolved_path.exists():
                icon_ref = self._copy_icon_to_output(resolved_path)
                if icon_ref:
                    self.image_stats.markdown_images += 1
                    return f"![{alt or filename}]({icon_ref})"

        # Fall back to text placeholders for icons that don't exist as files
        if filename in self.RUNTIME_ICONS:
            self.image_stats.converted_to_text += 1
            return self.RUNTIME_ICONS[filename]

        # Handle note/tip/warning icons - these will be part of callout boxes
        if src.endswith(("note.png", "tip.png", "warning.png")):
            self.image_stats.converted_to_text += 1
            return ""  # These are handled by the parent div

        # Regular image - becomes markdown
        self.image_stats.markdown_images += 1
        return f"![{alt}]({src})"

    def _copy_icon_to_output(self, icon_path: Path) -> Optional[str]:
        """
        Copy an icon file to the output icons directory.

        Args:
            icon_path: Path to the source icon file

        Returns:
            Relative path to use in markdown (e.g., "../icons/Plus2.png"),
            or None if copying failed.
            Calculates the correct relative path based on the output markdown file's depth.
        """
        if not self.output_dir:
            return None

        try:
            # Create icons directory in output root
            icons_dir = self.output_dir / "icons"
            icons_dir.mkdir(parents=True, exist_ok=True)

            dest = icons_dir / icon_path.name

            # Only copy if not already copied
            if icon_path.name not in self._copied_icons:
                shutil.copy(icon_path, dest)
                self._copied_icons.add(icon_path.name)

            # Calculate correct relative path based on output markdown file depth
            if self.output_md_path:
                # Get the directory containing the markdown file
                md_dir = self.output_md_path.parent
                # Calculate relative path from md_dir to icons_dir
                try:
                    # Use os.path.relpath for cross-platform relative path calculation
                    import os

                    rel_path = os.path.relpath(icons_dir, md_dir)
                    return f"{rel_path}/{icon_path.name}".replace("\\", "/")
                except ValueError:
                    # Fallback if paths are on different drives (Windows)
                    pass

            # Fallback: assume depth 1 (ModuleName/File.md)
            return f"../icons/{icon_path.name}"
        except Exception:
            return None

    def _convert_list(self, element: Tag) -> str:
        """Convert a list element."""
        is_ordered = element.name.lower() == "ol"
        items = []
        counter = 1

        for child in element.children:
            if isinstance(child, Tag) and child.name.lower() == "li":
                content = self._convert_children(child).strip()
                # Handle multi-line content in list items
                lines = content.split("\n")
                if is_ordered:
                    prefix = f"{counter}. "
                    counter += 1
                else:
                    prefix = "- "

                if lines:
                    # Check if first line starts with a code fence (```)
                    # Code blocks inside list items need special handling
                    if lines[0].strip().startswith("```"):
                        # Code block inside list item - put on new line and indent
                        item = prefix.rstrip()  # Just the list marker
                        item += "\n"
                        # Indent all code block lines
                        for line in lines:
                            if line.strip():
                                item += "  " + line + "\n"
                            else:
                                item += "\n"
                        item = item.rstrip()
                    else:
                        # Normal list item - first line with prefix
                        item = prefix + lines[0]
                        # Subsequent lines indented
                        for line in lines[1:]:
                            if line.strip():
                                item += "\n  " + line
                    items.append(item)

        return "\n\n" + "\n".join(items) + "\n\n"

    def _convert_list_item(self, element: Tag) -> str:
        """Convert a list item (handled by _convert_list)."""
        return self._convert_children(element)

    def _get_direct_table_rows(self, table: Tag) -> list:
        """Get only the direct rows of a table, not rows from nested tables.

        This handles both direct <tr> children and <tr> inside <tbody>/<thead>/<tfoot>,
        but excludes rows from nested <table> elements.
        """
        rows = []

        for child in table.children:
            if not isinstance(child, Tag):
                continue

            if child.name.lower() == "tr":
                rows.append(child)
            elif child.name.lower() in ("tbody", "thead", "tfoot"):
                # Get <tr> children of this section, but not from nested tables
                for subchild in child.children:
                    if isinstance(subchild, Tag) and subchild.name.lower() == "tr":
                        rows.append(subchild)

        return rows

    def _convert_table(self, element: Tag) -> str:
        """Convert a table to Markdown and track conversion statistics."""
        self.table_stats.html_tables += 1

        is_layout_table = self._is_layout_table(element)

        # Check if this layout table contains nested tables
        # If so, just convert the children directly instead of creating a markdown table
        if is_layout_table:
            nested_tables = element.find_all("table", recursive=True)
            if nested_tables:
                self.table_stats.layout_tables += 1
                # Convert children directly - nested tables will be handled separately
                return self._convert_children(element)

        rows = []
        table_has_content = False

        # Find direct rows only (not rows from nested tables)
        for row in self._get_direct_table_rows(element):
            cells = []
            is_header = False

            # Only get direct cell children, not cells from nested tables
            for cell in row.find_all(["th", "td"], recursive=False):
                # Convert cell content, including images
                content = self._convert_table_cell(cell)
                # Replace newlines and pipes in cell content
                content = content.replace("\n", " ").replace("|", "\\|")
                cells.append(content)

                # Handle colspan - add empty cells for spanned columns
                colspan = cell.get("colspan", "1")
                try:
                    colspan_num = int(colspan)
                    for _ in range(colspan_num - 1):
                        cells.append("")  # Add empty cells for colspan
                except (ValueError, TypeError):
                    pass
                if content.strip():
                    table_has_content = True
                if cell.name.lower() == "th":
                    is_header = True

            if cells:
                rows.append((cells, is_header))

        if not rows:
            return ""

        # Track table type
        if is_layout_table:
            self.table_stats.layout_tables += 1
        else:
            self.table_stats.content_tables += 1

        # Build markdown table
        result = ["\n"]

        # Determine column count
        max_cols = max(len(r[0]) for r in rows)

        for i, (cells, is_header) in enumerate(rows):
            # Pad cells if needed
            while len(cells) < max_cols:
                cells.append("")

            row_str = "| " + " | ".join(cells) + " |"
            result.append(row_str)

            # Add header separator after first row or header row
            if i == 0 or is_header:
                separator = "| " + " | ".join(["---"] * max_cols) + " |"
                result.append(separator)

        result.append("\n")

        # Track output type
        if table_has_content:
            self.table_stats.markdown_tables += 1
        else:
            self.table_stats.blank_tables += 1

        return "\n".join(result)

    def _is_layout_table(self, element: Tag) -> bool:
        """Detect if a table is used for layout rather than data.

        Layout tables typically:
        - Have width="100%" and a single cell
        - Contain only images
        - Have x-use-null-cells attribute
        - Are used for centering/positioning content
        """
        # Check for layout indicators
        width = element.get("width", "")
        has_null_cells = element.get("x-use-null-cells") is not None

        # Count only direct cells (not cells from nested tables)
        direct_rows = self._get_direct_table_rows(element)
        direct_cells = []
        for row in direct_rows:
            for cell in row.find_all(["td", "th"], recursive=False):
                direct_cells.append(cell)

        if len(direct_cells) == 1:
            cell = direct_cells[0]
            # Single cell with only image (not counting nested tables) = layout table
            # Only check direct images, not images inside nested tables
            direct_imgs = [c for c in cell.children if isinstance(c, Tag) and c.name.lower() == "img"]
            # Get text but exclude nested tables
            text_parts = []
            for c in cell.children:
                if isinstance(c, NavigableString):
                    text_parts.append(str(c).strip())
                elif isinstance(c, Tag) and c.name.lower() != "table":
                    text_parts.append(c.get_text(strip=True))
            text = " ".join(text_parts).strip()

            if direct_imgs and not text:
                return True
            # Single cell with width="100%" = likely layout
            if width == "100%" or cell.get("width") == "100%":
                return True

        if has_null_cells:
            return True

        return False

    def _convert_table_cell(self, cell: Tag) -> str:
        """Convert a table cell's content, including images.

        Unlike _get_text_content, this preserves images as markdown.
        """
        result = []

        for child in cell.children:
            if isinstance(child, NavigableString):
                text = str(child).strip()
                if text:
                    # Escape angle brackets to prevent markdown interpreting them as HTML
                    result.append(escape_angle_brackets(text))
            elif isinstance(child, Tag):
                if child.name.lower() == "img":
                    # Convert image to markdown
                    img_md = self._convert_image(child)
                    if img_md:
                        result.append(img_md)
                elif child.name.lower() == "a":
                    # Handle links (may contain images)
                    href = child.get("href", "")
                    name = child.get("name")
                    if name:
                        # Named anchor - skip
                        continue
                    # Check for image inside link
                    img = child.find("img")
                    if img:
                        img_md = self._convert_image(img)
                        if href and img_md:
                            result.append(f"[{img_md}]({href})")
                        elif img_md:
                            result.append(img_md)
                    else:
                        # Text link
                        text = child.get_text(strip=True)
                        if text and href:
                            result.append(f"[{escape_angle_brackets(text)}]({href})")
                        elif text:
                            result.append(escape_angle_brackets(text))
                elif child.name.lower() == "br":
                    result.append(" ")
                elif child.name.lower() in ("b", "strong"):
                    text = child.get_text(strip=True)
                    if text:
                        result.append(f"**{escape_angle_brackets(text)}**")
                elif child.name.lower() in ("i", "em"):
                    text = child.get_text(strip=True)
                    if text:
                        result.append(f"*{escape_angle_brackets(text)}*")
                elif child.name.lower() in ("code", "tt"):
                    text = child.get_text(strip=True)
                    if text:
                        result.append(f"`{text}`")
                else:
                    # Recursively get text from other elements
                    text = child.get_text(strip=True)
                    if text:
                        result.append(escape_angle_brackets(text))

        return " ".join(result)

    def _convert_code(self, element: Tag) -> str:
        """Convert code/pre elements and track conversion statistics."""
        # Check if it's inline code or a code block
        if element.name.lower() == "pre":
            # Track the <pre> tag
            self.code_block_stats.html_pre_tags += 1

            code = element.find("code")
            if code:
                content = code.get_text()
            else:
                content = element.get_text()
            # Determine language if possible
            lang = ""

            # Track the markdown code block output
            self.code_block_stats.markdown_code_blocks += 1
            return f"\n\n```{lang}\n{content}\n```\n\n"
        else:
            # Inline code
            content = element.get_text()
            return f"`{content}`"

    def _convert_inline_code(self, element: Tag) -> str:
        """Convert TT (teletype) elements to inline code."""
        content = element.get_text()
        return f"`{content}`"

    def _convert_bold(self, element: Tag) -> str:
        """Convert bold elements."""
        content = self._convert_children(element).strip()
        if not content:
            return ""
        return f"**{content}**"

    def _convert_italic(self, element: Tag) -> str:
        """Convert italic elements."""
        content = self._convert_children(element).strip()
        if not content:
            return ""
        return f"*{content}*"

    def _convert_blockquote(self, element: Tag) -> str:
        """Convert blockquote elements."""
        # In Ghidra help, blockquotes are often used for indentation
        # We'll just process the content without the > prefix to keep it cleaner
        content = self._convert_children(element)
        return content

    def _convert_div_span(self, element: Tag) -> str:
        """Convert div and span elements, checking for special classes."""
        classes = element.get("class", [])
        if isinstance(classes, str):
            classes = [classes]

        # Handle special div classes (tips, notes, warnings)
        # These often contain complex table structures - extract just the text
        if "note" in classes:
            text = self._extract_callout_text(element)
            return f"\n\n> **Note:** {text}\n\n"
        elif "tip" in classes:
            text = self._extract_callout_text(element)
            return f"\n\n> **Tip:** {text}\n\n"
        elif "warning" in classes:
            text = self._extract_callout_text(element)
            return f"\n\n> **Warning:** {text}\n\n"
        elif "informalexample" in classes:
            # Check if this contains a code block (pre tag)
            pre = element.find("pre")
            if pre:
                # Convert as code block
                return self._convert_code(pre)
            # Otherwise treat as a note-like block
            text = self._extract_callout_text(element)
            return f"\n\n> {text}\n\n"
        elif "mediaobject" in classes:
            # DocBook mediaobject divs contain images wrapped in tables for sizing
            # Extract the image directly instead of converting the wrapper table
            img = element.find("img")
            if img:
                return "\n\n" + self._convert_image(img) + "\n\n"
            # Fall through to default handling if no image found

        content = self._convert_children(element)
        return content

    def _extract_callout_text(self, element: Tag) -> str:
        """Extract text content from callout boxes (note/tip/warning divs)."""
        # These often have complex table structures with icons
        # We want just the actual text content
        text_parts = []

        # Find all text-containing elements, skipping icon cells
        for td in element.find_all("td"):
            # Skip cells that only contain images
            if td.find("img") and not td.get_text(strip=True):
                continue
            text = td.get_text(separator=" ", strip=True)
            if text:
                text_parts.append(text)

        # If no table cells found, get text from the whole element
        if not text_parts:
            text_parts.append(element.get_text(separator=" ", strip=True))

        return " ".join(text_parts)

    def _extract_anchor(self, element: Tag) -> Optional[str]:
        """Extract anchor name from element or its children (slugified)."""
        # Check for name attribute
        name = element.get("name")
        if name:
            slug_name = slugify(name)
            if slug_name:
                self.anchors.append(slug_name)
                return slug_name

        # Check for anchor child
        anchor = element.find("a", attrs={"name": True})
        if anchor:
            name = anchor.get("name")
            if name:
                slug_name = slugify(name)
                if slug_name:
                    self.anchors.append(slug_name)
                    return slug_name

        return None

    def _extract_all_anchors(self, element: Tag) -> list[str]:
        """Extract ALL anchor names from element and its children (slugified).

        This is important for headings that have multiple anchors, e.g.:
        <H2><A name="Delete_Equate"></A><A name="Remove_Equate"></A>Remove Equate</H2>
        Both anchors need to be preserved for TOC links to work correctly.
        """
        anchors = []

        # Check for name attribute on element itself
        name = element.get("name")
        if name:
            slug_name = slugify(name)
            if slug_name:
                anchors.append(slug_name)
                self.anchors.append(slug_name)

        # Find ALL anchor children with name attribute
        for anchor in element.find_all("a", attrs={"name": True}):
            name = anchor.get("name")
            if name:
                slug_name = slugify(name)
                if slug_name and slug_name not in anchors:
                    anchors.append(slug_name)
                    self.anchors.append(slug_name)

        return anchors

    def _get_text_content(self, element: Tag) -> str:
        """Get the text content of an element, handling nested elements."""
        result = []

        for child in element.children:
            if isinstance(child, NavigableString):
                result.append(str(child))
            elif isinstance(child, Tag):
                if child.name.lower() == "a" and child.get("name"):
                    # Named anchor, skip but record (slugified)
                    name = child.get("name")
                    if name:
                        slug_name = slugify(name)
                        if slug_name:
                            self.anchors.append(slug_name)
                    # Include any text inside the anchor
                    result.append(child.get_text())
                elif child.name.lower() in ("b", "strong"):
                    result.append(f"**{child.get_text()}**")
                elif child.name.lower() in ("i", "em"):
                    result.append(f"*{child.get_text()}*")
                elif child.name.lower() in ("code", "tt"):
                    result.append(f"`{child.get_text()}`")
                else:
                    result.append(child.get_text())

        return "".join(result)

    def _cleanup_markdown(self, markdown: str) -> str:
        """Clean up the generated markdown."""
        # Remove excessive blank lines (more than 2)
        markdown = re.sub(r"\n{4,}", "\n\n\n", markdown)

        # Process lines - strip whitespace appropriately
        lines = markdown.split("\n")
        cleaned_lines = []
        in_code_block = False

        for line in lines:
            # Track fenced code blocks - preserve their content exactly
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                cleaned_lines.append(line.rstrip())
                continue

            if in_code_block:
                # Preserve code block content (only rstrip)
                cleaned_lines.append(line.rstrip())
            else:
                # For regular content, strip both leading and trailing whitespace
                # This prevents HTML source indentation from creating markdown code blocks
                cleaned_lines.append(line.strip())

        markdown = "\n".join(cleaned_lines)

        # Ensure single newline at end
        markdown = markdown.strip() + "\n"

        return markdown


def convert_html_file(
    html_path: Path,
    used_anchors: Optional[set[str]] = None,
    icon_resolver: Optional["IconResolver"] = None,
    output_dir: Optional[Path] = None,
    output_md_path: Optional[Path] = None,
) -> str:
    """Convenience function to convert an HTML file to Markdown."""
    converter = HTMLToMarkdownConverter(
        used_anchors=used_anchors,
        icon_resolver=icon_resolver,
        output_dir=output_dir,
        output_md_path=output_md_path,
    )
    return converter.convert_file(html_path)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m ghidra_help_to_markdown.html_converter <html_file>")
        sys.exit(1)

    html_path = Path(sys.argv[1])
    markdown = convert_html_file(html_path)
    print(markdown)
