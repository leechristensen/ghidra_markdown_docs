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
    """Convert text to an anchor slug compatible with python-markdown/kramdown.

    Both engines (mkdocs default + Jekyll default) auto-id headings by:
        - lowercasing
        - stripping characters that aren't `\\w`, whitespace, or hyphen
        - collapsing whitespace/hyphens to a single `-`

    `\\w` includes underscore, so `foo_bar` stays `foo_bar` — replacing the
    underscore with a hyphen here would break cross-references whose target
    rendered with the underscore intact.

    Examples:
        "Error Dialogs" -> "error-dialogs"
        "P-code"         -> "p-code"
        "bsim_ctl"       -> "bsim_ctl"
    """
    slug = text.lower()
    # Strip everything except word chars (a-z, 0-9, _), whitespace, hyphen.
    slug = re.sub(r"[^\w\s-]", "", slug)
    # Collapse whitespace + hyphen runs into a single hyphen.
    slug = re.sub(r"[\s-]+", "-", slug)
    return slug.strip("-")


def _wrap_inline_code(content: str) -> str:
    """Wrap `content` as a markdown inline code span, using a backtick fence
    long enough to contain any backticks in the content.

    CommonMark allows multi-backtick fences to embed shorter backtick runs:
    `` ``foo`bar`` `` renders as the literal code "foo`bar". Without this,
    `<CODE>foo`bar</CODE>` would become `` `foo`bar` `` which markdown
    parses as two code spans with stray text.
    """
    if not content:
        return ""
    # Find the longest run of backticks in the content and use one more.
    longest = max((len(m) for m in re.findall(r"`+", content)), default=0)
    fence = "`" * (longest + 1)
    pad = " " if content.startswith("`") or content.endswith("`") else ""
    return f"{fence}{pad}{content}{pad}{fence}"


def _ends_with_emphasis(text: str) -> bool:
    """Return True if `text` ends with a markdown bold/italic marker.

    We skip backticks here: two adjacent code spans render fine
    (`<code>a</code><code>b</code>`) and inserting a visible space between
    them would break things like multi-part file paths in the source.
    """
    if not text:
        return False
    if text.endswith("*"):
        return not text.endswith("\\*")
    return False


def _starts_with_emphasis(text: str) -> bool:
    """Return True if `text` starts with a markdown bold/italic marker."""
    return bool(text) and text[0] == "*"


def _escape_markdown_specials(text: str) -> str:
    """Backslash-escape literal `*` and `` ` `` in plain text.

    The Ghidra HTML source uses `<B>`/`<I>`/`<EM>` for emphasis and
    `<CODE>`/`<TT>` for code, so any `*` or backtick that survives into
    NavigableString text is meant as a literal character (wildcard, C
    pointer, placeholder, keyboard mention, etc.). Without escaping, those
    end up creating spurious emphasis/code spans in the rendered markdown.
    """
    return text.replace("*", "\\*").replace("`", "\\`")


def _escape_emphasis_boundaries(content: str) -> str:
    """Escape literal `*` at the start/end of emphasis content.

    The upstream Ghidra HTML wraps wildcard patterns like `*.gpr` in `<em>` and
    file extensions like `*.mv.db` in `<b>`. Emitting these as `*<text>*` or
    `**<text>**` produces ambiguous markdown where the boundary asterisks
    collide with the emphasis markers — e.g. `**.mv.db*` parses as italic
    italic-`<em>.mv.db</em>` + trailing `*`. Backslash-escape boundary
    asterisks so the rendered output is `<strong>*.mv.db</strong>`.
    """
    if content.startswith("*"):
        content = "\\" + content
    if content.endswith("*") and not content.endswith("\\*"):
        content = content[:-1] + "\\*"
    return content


def _alt_from_filename(filename: str) -> str:
    """Synthesize human-readable alt text from an image filename.

    The upstream Ghidra HTML uses `alt=""` for nearly every inline icon,
    which lints as an accessibility warning when carried verbatim into
    markdown. Derive something useful from the filename instead:

    - Drop the extension.
    - Split CamelCase: `ArchiveProject` -> `Archive Project`.
    - Treat `_` and `-` as word separators.
    - Title-case and collapse repeated whitespace.
    """
    stem = Path(filename).stem
    # Split CamelCase boundaries: insert a space before any uppercase letter
    # that follows a lowercase letter or digit.
    stem = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", stem)
    # Underscores and hyphens become spaces.
    stem = stem.replace("_", " ").replace("-", " ")
    # Collapse runs of whitespace and title-case the result.
    return " ".join(stem.split()).title()


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
        # Track current heading slug for mapping orphan anchors (on non-heading elements)
        self.current_heading_slug: str = ""

    def _preprocess_html(self, html_content: str) -> str:
        """Preprocess HTML to fix common issues in Ghidra help files.

        Fixes:
        - Mismatched heading tags (e.g., <H3>...</H2> -> <H3>...</H3>)
        - Self-closing <a/> + stray </a> patterns that confuse HTML parsers,
          e.g. `<A name="foo"/><A name="bar"/></A>Text</H3>` — html.parser
          and lxml both drop the trailing text out of the heading.
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

        # Normalize self-closing <a/> tags to <a></a> (HTML doesn't allow
        # void <a>, but Ghidra sources frequently use <A name="x"/>).
        html_content = re.sub(r"<([Aa])\s+([^>]*?)\s*/>", r"<\1 \2></\1>", html_content)
        # Fix mismatched table cell closers: `<TH>...</TD>` and `<TD>...</TH>`
        # appear in some Ghidra sources (notably DataPlugin/Data.htm). Both
        # html.parser and lxml mis-nest these into a single outer cell with
        # the second cell's text merged in, which collapses table columns.
        html_content = re.sub(r"(<[Tt][Hh][^>]*>[^\n]*?)</[Tt][Dd]>", r"\1</th>", html_content)
        html_content = re.sub(r"(<[Tt][Dd][^>]*>[^\n]*?)</[Tt][Hh]>", r"\1</td>", html_content)
        # Merge adjacent `<CODE>...</CODE><CODE>...</CODE>` runs (often used
        # to compose long paths / commands across attribute styles, like
        # `<CODE class="path">DIR/</CODE><CODE>name</CODE>`). Without the
        # merge, the converter emits two adjacent backtick spans that
        # python-markdown then interprets as a double-backtick fence,
        # swallowing the inner backticks as literal text.
        prev = None
        while prev != html_content:
            prev = html_content
            html_content = re.sub(
                r"</[Cc][Oo][Dd][Ee]>\s*<[Cc][Oo][Dd][Ee][^>]*>", "", html_content
            )
        # Drop unmatched stray </a> tags directly following a closed anchor —
        # the pattern in some headings is `<a/><a/></a>` which after the prior
        # normalization becomes `<a></a><a></a></a>`.
        prev = None
        while prev != html_content:
            prev = html_content
            html_content = re.sub(r"(</[Aa]>)\s*</[Aa]>", r"\1", html_content)

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
        self.current_heading_slug = ""

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
            # Ghidra source HTML uses <B>/<I>/<EM> for emphasis, so any
            # literal `*` or `_` in raw text is meant as a character —
            # often a wildcard like `*.gpr`, a C pointer type like `int *`,
            # or a placeholder like `***TODO***`. Without escaping, those
            # turn into spurious italic/bold spans.
            text = _escape_markdown_specials(text)
            # Escape angle brackets so markdown doesn't interpret <Ctrl>,
            # <Shift> etc. as HTML.
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
        elif tag_name == "dl":
            return self._convert_definition_list(element)
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
        elif tag_name == "u":
            # Markdown has no native underline; pass through as HTML.
            # GFM renders inline <u> correctly. ~80 uses in corpus for emphasis.
            content = self._convert_children(element).strip()
            return f"<u>{content}</u>" if content else ""
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
            converted = self._convert_element(child)
            if not converted:
                continue
            # Adjacent emphasis or code markers from sibling tags (e.g.
            # `<I>foo</I><I>bar</I>`) would concatenate to `*foo**bar*`,
            # which markdown parses as italic + bold-open. Insert a thin
            # separator so each span stays distinct.
            if result and _starts_with_emphasis(converted) and _ends_with_emphasis(result[-1]):
                result.append(" ")
            result.append(converted)
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

        # Check for images in the heading (e.g., <H2>Clear <IMG src="..."></H2>)
        # These should be included after the heading text
        heading_images = []
        for img in element.find_all("img"):
            img_md = self._convert_image(img)
            if img_md:
                heading_images.append(img_md)

        # The markdown renderer auto-IDs the FINAL heading line. Markdown
        # `![alt](src)` images are rendered to <img> tags and their syntax is
        # stripped from the slug, but non-image image_md (text placeholders
        # like `[Undo]`, ` → `, or RUNTIME_ICONS strings) stays as text and
        # contributes to the slug. Include only the non-image placeholders so
        # the converter's slug matches what python-markdown/kramdown produce.
        text_placeholders = [im for im in heading_images if not im.startswith("!")]
        slug_input = text if not text_placeholders else text + " " + " ".join(text_placeholders)
        heading_slug = slugify(slug_input)

        # Update current heading slug for orphan anchor mapping
        self.current_heading_slug = heading_slug

        # Build mapping from HTML anchor slugs to GFM heading slug
        # This allows link resolver to convert old anchor references to correct GFM anchors
        for html_anchor in html_anchors:
            if html_anchor and html_anchor != heading_slug:
                self.anchor_to_heading_slug[html_anchor] = heading_slug

        # Include any images found in the heading
        if heading_images:
            images_str = " " + " ".join(heading_images)
            return f"\n\n{prefix} {text}{images_str}\n\n"

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
            callout = None
            if "note.png" in src:
                callout = "Note"
            elif "tip.png" in src:
                callout = "Tip"
            elif "warning.png" in src:
                callout = "Warning"
            if callout:
                text = element.get_text(separator=" ", strip=True)
                anchor_markup = self._emit_nested_anchors(element)
                return f"\n\n> {anchor_markup}**{callout}:** {text}\n\n"

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
            # If the inner content already has emphasis markers (e.g.
            # `Provided by: *PluginName*`), wrapping in another `*...*`
            # produces malformed `*Provided by: *PluginName**` that
            # python-markdown parses as italic-`Provided by:` + literal `**`.
            # Keep the inner emphasis only in that case.
            if "*" in content:
                return f"\n\n{content}\n\n"
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
                # Map orphan anchor to current heading (if we have one and it's different)
                if self.current_heading_slug and slug_name != self.current_heading_slug:
                    self.anchor_to_heading_slug[slug_name] = self.current_heading_slug
            # Named anchors can also contain content that needs to be converted
            # e.g., <A name="foo"><B>Title</B> Description</A>
            content = self._convert_children(element).strip()
            # Emit HTML anchor tag to preserve link target for non-heading anchors
            # (headings get auto-anchors from GFM, but table cells, spans, etc. don't)
            if slug_name:
                # Add newline after anchor if content starts with a heading
                # to avoid "anchor on same line as header" rendering issue
                if content.startswith("#") or content.startswith("\n#"):
                    return f'<a name="{slug_name}"></a>\n\n{content}'
                return f'<a name="{slug_name}"></a>{content}'
            return content

        # Regular link
        href = element.get("href", "")
        text = self._get_text_content(element).strip()

        if not text:
            # Image link or empty
            img = element.find("img")
            if img:
                img_md = self._convert_image(img)
                if href and img_md.startswith("!["):
                    # Clickable image: wrap markdown image in a link
                    href = href.replace("/#", "#")
                    return f"[{img_md}]({href})"
                return img_md
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
                resolved_path = self.icon_resolver.resolve(src, self.source_path)
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
                    return f"![{alt or _alt_from_filename(filename)}]({icon_ref})"

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
        return f"![{alt or _alt_from_filename(filename)}]({src})"

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
            elif isinstance(child, Tag) and child.name.lower() in ("ul", "ol"):
                # Handle nested list that's a sibling of <li> elements (technically invalid HTML
                # but Ghidra uses this pattern). Convert the nested list and indent it.
                nested_content = self._convert_list(child).strip()
                if nested_content:
                    # Indent each line of the nested list
                    indented_lines = []
                    for line in nested_content.split("\n"):
                        if line.strip():
                            indented_lines.append("  " + line)
                    if indented_lines:
                        # Append to the previous item (if any) so it renders as a nested list
                        if items:
                            items[-1] += "\n" + "\n".join(indented_lines)
                        else:
                            items.append("\n".join(indented_lines))

        return "\n\n" + "\n".join(items) + "\n\n"

    def _convert_list_item(self, element: Tag) -> str:
        """Convert a list item (handled by _convert_list)."""
        return self._convert_children(element)

    def _convert_definition_list(self, element: Tag) -> str:
        """Convert a <dl> definition list to pandoc-style markdown.

        Pandoc syntax:
            term
            :   definition text

            continuation paragraph of the same definition

            next term
            :   next definition

        Multiple <dt> in a row before a <dd> produce multiple terms for the same definition.
        Definition continuation paragraphs are indented 4 spaces; the first line uses ":   ".
        """
        pairs: list[tuple[list[str], list[str]]] = []  # [(terms, definitions)]
        current_terms: list[str] = []

        for child in element.children:
            if not isinstance(child, Tag):
                continue
            name = child.name.lower()
            if name == "dt":
                # Preserve any <a name>/id anchors inside the <dt> so cross-file
                # links like Foo.md#bar still resolve. Without this, term-level
                # anchors are stripped entirely by _get_text_content.
                dt_anchors: list[str] = []
                for a in child.find_all("a"):
                    anchor_name = a.get("name") or a.get("id")
                    if not anchor_name:
                        continue
                    slug = slugify(anchor_name)
                    if not slug or slug in dt_anchors:
                        continue
                    self.anchors.append(slug)
                    if self.current_heading_slug and slug != self.current_heading_slug:
                        self.anchor_to_heading_slug[slug] = self.current_heading_slug
                    dt_anchors.append(slug)

                term = self._get_text_content(child).strip()
                term = " ".join(term.split())  # collapse whitespace
                if term:
                    if dt_anchors:
                        anchor_markup = "".join(f'<a name="{a}"></a>' for a in dt_anchors)
                        term = anchor_markup + term
                    current_terms.append(term)
            elif name == "dd":
                if not current_terms:
                    # <dd> with no preceding <dt>; skip orphan
                    continue
                definition = self._convert_children(child).strip()
                pairs.append((current_terms, [definition]))
                current_terms = []

        if not pairs:
            return ""

        out_lines: list[str] = [""]
        for terms, definitions in pairs:
            for term in terms:
                out_lines.append(term)
            for definition in definitions:
                if not definition:
                    out_lines.append(":")
                    continue
                lines = definition.split("\n")
                first = True
                for line in lines:
                    if first and line.strip():
                        out_lines.append(f":   {line}")
                        first = False
                    elif line.strip():
                        out_lines.append(f"    {line}")
                    else:
                        out_lines.append("")
            out_lines.append("")  # blank line between pairs
        out_lines.append("")
        return "\n".join(out_lines)

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

        # Layout tables (used for positioning rather than tabular data) have no
        # meaningful structure to render — emit their inner content directly so
        # we don't produce single-cell or blank markdown tables that lint tools
        # flag (and that look ugly).
        if is_layout_table:
            self.table_stats.layout_tables += 1
            return "\n\n" + self._convert_children(element).strip() + "\n\n"

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

        # Determine column count
        max_cols = max(len(r[0]) for r in rows)

        # A leading "title" row (single non-empty cell that spans all
        # columns) followed by a real `<TH>` header row produces invalid
        # markdown — the engine needs the separator on line 2. Pull the
        # title out as a bold caption ABOVE the table so the actual column
        # headers can occupy row 0.
        caption = ""
        if len(rows) >= 2:
            first_cells, first_is_header = rows[0]
            non_empty = [c for c in first_cells if c.strip()]
            has_following_header = any(h for _, h in rows[1:])
            if (
                len(non_empty) == 1
                and not first_is_header
                and has_following_header
            ):
                caption = non_empty[0]
                rows = rows[1:]
                max_cols = max(len(r[0]) for r in rows)

        # Build markdown table
        result = ["\n"]
        if caption:
            result.append(caption)
            result.append("")

        # Markdown tables allow exactly one header separator. Place it after
        # the LAST header row so all `<TH>` rows stay in the header section.
        # Fall back to "first row is header" when no `<TH>` is present.
        last_header_idx = -1
        for idx, (_, is_header) in enumerate(rows):
            if is_header:
                last_header_idx = idx
        separator_after = last_header_idx + 1 if last_header_idx >= 0 else 1
        separator_after = min(separator_after, len(rows))

        for i, (cells, is_header) in enumerate(rows):
            # Pad cells if needed
            while len(cells) < max_cols:
                cells.append("")

            row_str = "| " + " | ".join(cells) + " |"
            result.append(row_str)

            if i + 1 == separator_after:
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
        - Have only ONE row (markdown tables require header + separator +
          data rows; a single-row source table renders as "header but no
          data rows" otherwise)
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

        # Single-row tables (any number of cells) can't be rendered as valid
        # markdown tables — markdown requires a header row + separator + data
        # rows, so a 1-row source becomes a header-only table that lints flag.
        # Treat them as layout containers and let their cell content render
        # inline.
        if len(direct_rows) == 1 and all(c.name.lower() == "td" for c in direct_cells):
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
                        # Named anchor - emit HTML anchor tag to preserve link target
                        slug_name = slugify(name)
                        if slug_name:
                            self.anchors.append(slug_name)
                            if self.current_heading_slug and slug_name != self.current_heading_slug:
                                self.anchor_to_heading_slug[slug_name] = self.current_heading_slug
                            result.append(f'<a name="{slug_name}"></a>')
                        # Emit the anchor's children too — text inside <a name="x">Text</a>
                        # is real content and must not be dropped (12 instances in corpus).
                        inner_text = child.get_text(strip=True)
                        if inner_text:
                            result.append(escape_angle_brackets(inner_text))
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
                        anchor_markup = self._emit_nested_anchors(child)
                        result.append(f"**{anchor_markup}{escape_angle_brackets(text)}**")
                elif child.name.lower() in ("i", "em"):
                    text = child.get_text(strip=True)
                    if text:
                        anchor_markup = self._emit_nested_anchors(child)
                        result.append(f"*{anchor_markup}{escape_angle_brackets(text)}*")
                elif child.name.lower() in ("code", "tt"):
                    text = child.get_text(strip=True)
                    if text:
                        anchor_markup = self._emit_nested_anchors(child)
                        result.append(f"{anchor_markup}`{text}`")
                else:
                    # Recursively get text from other elements
                    text = child.get_text(strip=True)
                    if text:
                        anchor_markup = self._emit_nested_anchors(child)
                        result.append(f"{anchor_markup}{escape_angle_brackets(text)}")

        return " ".join(result)

    def _emit_nested_anchors(self, element: Tag) -> str:
        """Find any <a name>/id anchors inside element, record them in the
        anchor-to-heading mapping, and return inline `<a name="x"></a>` markup
        to prepend before the element's text. Used by table-cell and similar
        text-flattening paths so nested anchors aren't silently dropped.
        """
        found: list[str] = []
        for a in element.find_all("a"):
            anchor_name = a.get("name") or a.get("id")
            if not anchor_name:
                continue
            slug = slugify(anchor_name)
            if not slug or slug in found:
                continue
            self.anchors.append(slug)
            if self.current_heading_slug and slug != self.current_heading_slug:
                self.anchor_to_heading_slug[slug] = self.current_heading_slug
            found.append(slug)
        return "".join(f'<a name="{a}"></a>' for a in found)

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
            # Inline code — collapse internal whitespace so the span doesn't
            # break across a line and split the backtick pair across lines.
            content = " ".join(element.get_text().split())
            return _wrap_inline_code(content)

    def _convert_inline_code(self, element: Tag) -> str:
        """Convert TT (teletype) elements to inline code."""
        content = " ".join(element.get_text().split())
        return _wrap_inline_code(content)

    def _convert_bold(self, element: Tag) -> str:
        """Convert bold elements."""
        content = self._convert_children(element).strip()
        if not content:
            return ""
        # Collapse internal whitespace so the bold span stays on one line —
        # multi-line `**...**` looks unmatched to lint tools and renderers.
        content = " ".join(content.split())
        return f"**{_escape_emphasis_boundaries(content)}**"

    def _convert_italic(self, element: Tag) -> str:
        """Convert italic elements."""
        content = self._convert_children(element).strip()
        if not content:
            return ""
        content = " ".join(content.split())
        return f"*{_escape_emphasis_boundaries(content)}*"

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
            # Check if this contains a definition list (variablelist) FIRST
            # These need to be fully converted to preserve anchors and structure
            # Must check before pre because nested informalexample divs inside dd elements contain pre tags
            dl = element.find("dl")
            if dl:
                return self._convert_children(element)
            # Check if this directly contains a code block (pre tag)
            pre = element.find("pre", recursive=False)
            if pre:
                # Convert as code block
                return self._convert_code(pre)
            # Check nested divs for direct pre children (code blocks inside wrapper divs)
            for child_div in element.find_all("div", recursive=False):
                pre = child_div.find("pre", recursive=False)
                if pre:
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
                # Map orphan anchor to current heading
                if self.current_heading_slug and slug_name != self.current_heading_slug:
                    self.anchor_to_heading_slug[slug_name] = self.current_heading_slug
                return slug_name

        # Check for anchor child
        anchor = element.find("a", attrs={"name": True})
        if anchor:
            name = anchor.get("name")
            if name:
                slug_name = slugify(name)
                if slug_name:
                    self.anchors.append(slug_name)
                    # Map orphan anchor to current heading
                    if self.current_heading_slug and slug_name != self.current_heading_slug:
                        self.anchor_to_heading_slug[slug_name] = self.current_heading_slug
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
                    inner = " ".join(child.get_text().split())
                    result.append(f"**{_escape_emphasis_boundaries(inner)}**" if inner else "")
                elif child.name.lower() in ("i", "em"):
                    inner = " ".join(child.get_text().split())
                    result.append(f"*{_escape_emphasis_boundaries(inner)}*" if inner else "")
                elif child.name.lower() in ("code", "tt"):
                    inner = " ".join(child.get_text().split())
                    result.append(_wrap_inline_code(inner) if inner else "")
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
                # Check if this is a list item (may have indentation for nested lists)
                stripped = line.lstrip()
                if stripped.startswith("- ") or stripped.startswith("* ") or re.match(r"\d+\. ", stripped):
                    # Preserve list item indentation, only rstrip
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
