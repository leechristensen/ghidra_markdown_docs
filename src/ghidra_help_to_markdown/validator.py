"""
Markdown Documentation Validator.

Validates generated markdown files for:
1. Proper rendering (headers, lists, tables, code blocks)
2. Valid image references (files exist)
3. Valid internal and external links
"""

import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from urllib.parse import unquote, urlparse


@dataclass
class ValidationIssue:
    """Represents a single validation issue."""

    file: Path
    line: int
    issue_type: str  # 'error' or 'warning'
    category: str  # 'render', 'image', 'link'
    message: str


@dataclass
class ValidationResult:
    """Result of validating a single file."""

    file: Path
    issues: list[ValidationIssue] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        return any(i.issue_type == "error" for i in self.issues)

    @property
    def has_warnings(self) -> bool:
        return any(i.issue_type == "warning" for i in self.issues)


@dataclass
class ValidationReport:
    """Complete validation report for all files."""

    results: list[ValidationResult] = field(default_factory=list)
    total_files: int = 0
    files_with_errors: int = 0
    files_with_warnings: int = 0
    total_errors: int = 0
    total_warnings: int = 0

    def add_result(self, result: ValidationResult) -> None:
        self.results.append(result)
        self.total_files += 1
        if result.has_errors:
            self.files_with_errors += 1
        if result.has_warnings:
            self.files_with_warnings += 1
        self.total_errors += sum(1 for i in result.issues if i.issue_type == "error")
        self.total_warnings += sum(1 for i in result.issues if i.issue_type == "warning")


class MarkdownValidator:
    """Validates markdown documentation files."""

    def __init__(self, docs_dir: Path, verbose: bool = False) -> None:
        self.docs_dir = docs_dir
        self.verbose = verbose
        # Build index of all markdown files for link validation
        self.md_files: set[str] = set()
        self._index_files()

    def _index_files(self) -> None:
        """Index all markdown files in the docs directory."""
        for md_file in self.docs_dir.rglob("*.md"):
            rel_path = md_file.relative_to(self.docs_dir)
            self.md_files.add(str(rel_path).replace("\\", "/"))

    def _count_table_columns(self, line: str) -> int:
        """
        Count table columns by counting unescaped pipes outside of inline code spans.

        This handles:
        - Escaped pipes (\\|) which are content, not delimiters
        - Pipes inside backtick code spans (`code|here`)

        Args:
            line: A markdown table row line

        Returns:
            Number of columns (unescaped pipes - 1)
        """
        # First, remove content inside backticks to avoid counting pipes in code
        # Handle both single and double backticks
        cleaned = line

        # Remove double-backtick code spans first (they can contain single backticks)
        cleaned = re.sub(r"``[^`]*``", "", cleaned)

        # Remove single-backtick code spans
        cleaned = re.sub(r"`[^`]*`", "", cleaned)

        # Now count unescaped pipes (pipes not preceded by backslash)
        # Use regex to find pipes that are NOT preceded by backslash
        unescaped_pipes = len(re.findall(r"(?<!\\)\|", cleaned))

        # Columns = unescaped pipes - 1 (first and last are delimiters)
        return unescaped_pipes - 1 if unescaped_pipes > 0 else 0

    def validate_all(self) -> ValidationReport:
        """Validate all markdown files in the docs directory."""
        report = ValidationReport()

        md_files = list(self.docs_dir.rglob("*.md"))
        for md_file in md_files:
            if self.verbose:
                print(f"  Validating: {md_file.relative_to(self.docs_dir)}")
            result = self.validate_file(md_file)
            report.add_result(result)

        return report

    def validate_file(self, md_file: Path) -> ValidationResult:
        """Validate a single markdown file."""
        result = ValidationResult(file=md_file)

        try:
            content = md_file.read_text(encoding="utf-8")
            lines = content.split("\n")

            # Validate rendering
            self._validate_rendering(md_file, lines, result)

            # Validate images
            self._validate_images(md_file, content, lines, result)

            # Validate tables
            self._validate_tables(md_file, lines, result)

            # Validate links
            self._validate_links(md_file, content, lines, result)

        except Exception as e:
            result.issues.append(
                ValidationIssue(
                    file=md_file, line=0, issue_type="error", category="render", message=f"Failed to read file: {e}"
                )
            )

        return result

    def _validate_rendering(self, md_file: Path, lines: list[str], result: ValidationResult) -> None:
        """Validate markdown rendering correctness."""

        in_code_block = False
        in_table = False
        table_columns = 0
        prev_line_blank = True

        for i, line in enumerate(lines, 1):
            # Track code blocks
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                continue

            if in_code_block:
                continue

            # Check for malformed headers
            header_match = re.match(r"^(#{1,6})\s*(.*)$", line)
            if header_match:
                hashes, text = header_match.groups()
                if not text.strip():
                    result.issues.append(
                        ValidationIssue(
                            file=md_file, line=i, issue_type="warning", category="render", message="Empty header"
                        )
                    )
                # Check if header follows blank line (proper markdown)
                if not prev_line_blank and i > 1:
                    result.issues.append(
                        ValidationIssue(
                            file=md_file,
                            line=i,
                            issue_type="warning",
                            category="render",
                            message="Header should be preceded by blank line",
                        )
                    )

            # Check for unclosed inline formatting
            # Count asterisks/underscores for bold/italic
            stripped = line.strip()
            if stripped and not stripped.startswith("|"):  # Skip table rows
                # Check for unmatched bold markers
                bold_count = len(re.findall(r"(?<!\*)\*\*(?!\*)", stripped))
                if bold_count % 2 != 0:
                    result.issues.append(
                        ValidationIssue(
                            file=md_file,
                            line=i,
                            issue_type="warning",
                            category="render",
                            message="Possibly unmatched bold markers (**)",
                        )
                    )

                # Check for unmatched backticks (inline code)
                backtick_count = stripped.count("`") - stripped.count("```") * 3
                if backtick_count % 2 != 0:
                    result.issues.append(
                        ValidationIssue(
                            file=md_file,
                            line=i,
                            issue_type="warning",
                            category="render",
                            message="Possibly unmatched backticks (`)",
                        )
                    )

            # Check table formatting
            if line.strip().startswith("|") and line.strip().endswith("|"):
                # Use smart column counting that ignores escaped pipes and pipes in code spans
                cells = self._count_table_columns(line)
                if not in_table:
                    in_table = True
                    table_columns = cells
                else:
                    if cells != table_columns:
                        result.issues.append(
                            ValidationIssue(
                                file=md_file,
                                line=i,
                                issue_type="error",
                                category="render",
                                message=f"Table row has {cells} columns, expected {table_columns}",
                            )
                        )
            else:
                if in_table:
                    in_table = False
                    table_columns = 0

            # Check for HTML anchor on same line as header (known issue we fixed)
            if re.search(r'<a name="[^"]+"></a>#+\s', line):
                result.issues.append(
                    ValidationIssue(
                        file=md_file,
                        line=i,
                        issue_type="error",
                        category="render",
                        message="Anchor and header on same line - won't render correctly",
                    )
                )

            prev_line_blank = not line.strip()

        # Check if code block was left open
        if in_code_block:
            result.issues.append(
                ValidationIssue(
                    file=md_file, line=len(lines), issue_type="error", category="render", message="Unclosed code block"
                )
            )

    def _is_indented_code_block(self, lines: list[str], line_idx: int) -> bool:
        """Check if a line is inside an indented code block.

        A line is in an indented code block if it starts with 4+ spaces or a tab,
        and is not part of a list item continuation.
        """
        line = lines[line_idx]

        # Check if line starts with 4+ spaces or a tab
        if not (line.startswith("    ") or line.startswith("\t")):
            return False

        # Look backwards to see if this is a list continuation
        # List continuations are indented but not code blocks
        for prev_idx in range(line_idx - 1, -1, -1):
            prev_line = lines[prev_idx]
            stripped = prev_line.strip()

            if not stripped:
                # Blank line - keep looking
                continue

            # Check if previous non-blank line is a list item
            if re.match(r"^(\s*)[-*+]\s", prev_line) or re.match(r"^(\s*)\d+\.\s", prev_line):
                # It's a list item - check if our line could be a continuation
                # Get the indentation of the list item content
                list_match = re.match(r"^(\s*)[-*+]\s+", prev_line) or re.match(r"^(\s*)\d+\.\s+", prev_line)
                if list_match:
                    list_indent = len(list_match.group(0).expandtabs(4))
                    line_indent_expanded = len(line.expandtabs(4)) - len(line.expandtabs(4).lstrip())
                    # If our indentation matches list continuation, not a code block
                    if line_indent_expanded <= list_indent + 4:
                        return False

            # Check if previous line is also indented (continuing code block)
            if prev_line.startswith("    ") or prev_line.startswith("\t"):
                continue

            # Previous line is not indented and not a list - this is a code block
            return True

        # Reached start of file with all indented lines - it's a code block
        return True

    def _validate_images(self, md_file: Path, content: str, lines: list[str], result: ValidationResult) -> None:
        """Validate image references."""
        # Pattern for markdown images: ![alt](src)
        img_pattern = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")

        in_fenced_code_block = False

        for i, line in enumerate(lines, 1):
            # Track fenced code blocks
            if line.strip().startswith("```"):
                in_fenced_code_block = not in_fenced_code_block
                continue

            if in_fenced_code_block:
                continue

            for match in img_pattern.finditer(line):
                alt_text = match.group(1)
                src = match.group(2)

                # Skip external URLs
                if src.startswith(("http://", "https://", "data:")):
                    continue

                # Skip programmatic icon references (already handled by converter)
                if src.startswith(("Icons.", "icon.")):
                    continue

                # Check if image is inside an indented code block (won't render)
                if self._is_indented_code_block(lines, i - 1):  # i is 1-indexed
                    result.issues.append(
                        ValidationIssue(
                            file=md_file,
                            line=i,
                            issue_type="error",
                            category="image",
                            message=f"Image inside indented code block (won't render): {src}",
                        )
                    )
                    continue

                # Resolve the image path
                src = unquote(src)  # Handle URL-encoded paths
                if src.startswith("/"):
                    img_path = self.docs_dir / src[1:]
                else:
                    img_path = md_file.parent / src

                # Normalize the path
                try:
                    img_path = img_path.resolve()
                except OSError:
                    pass

                if not img_path.exists():
                    result.issues.append(
                        ValidationIssue(
                            file=md_file,
                            line=i,
                            issue_type="error",
                            category="image",
                            message=f"Image not found: {src}",
                        )
                    )
                elif not alt_text:
                    result.issues.append(
                        ValidationIssue(
                            file=md_file,
                            line=i,
                            issue_type="warning",
                            category="image",
                            message=f"Image missing alt text: {src}",
                        )
                    )

    def _validate_tables(self, md_file: Path, lines: list[str], result: ValidationResult) -> None:
        """Validate markdown tables for content.

        Detects:
        - Blank tables (all cells empty) - likely layout tables from HTML
        - Tables with no content rows (only header + separator)
        """
        i = 0
        while i < len(lines):
            line = lines[i]

            # Check if this line starts a table (starts with |)
            if not line.strip().startswith("|"):
                i += 1
                continue

            # Found a potential table - collect all table rows
            table_start = i
            table_lines = []

            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append((i + 1, lines[i]))  # Store 1-indexed line number
                i += 1

            if len(table_lines) < 2:
                # Not a valid table (needs at least header + separator)
                continue

            # Analyze the table
            self._analyze_table(md_file, table_start + 1, table_lines, result)

    def _analyze_table(
        self, md_file: Path, start_line: int, table_lines: list[tuple[int, str]], result: ValidationResult
    ) -> None:
        """Analyze a markdown table for content issues."""
        # Separate header, separator, and content rows
        header_line = table_lines[0][1] if table_lines else ""
        separator_line = table_lines[1][1] if len(table_lines) > 1 else ""
        content_rows = table_lines[2:] if len(table_lines) > 2 else []

        # Check if separator line is valid (contains only |, -, :, and whitespace)
        separator_stripped = separator_line.strip()
        if not re.match(r"^[\|\-:\s]+$", separator_stripped):
            # Second line isn't a separator - this might not be a table
            return

        # Extract cell contents from header
        header_cells = self._extract_table_cells(header_line)

        # Check if header is blank
        header_has_content = any(cell.strip() for cell in header_cells)

        # Check content rows
        content_has_data = False
        for line_num, row in content_rows:
            cells = self._extract_table_cells(row)
            if any(cell.strip() for cell in cells):
                content_has_data = True
                break

        # Determine table status
        if not header_has_content and not content_has_data:
            # Completely blank table
            result.issues.append(
                ValidationIssue(
                    file=md_file,
                    line=start_line,
                    issue_type="warning",
                    category="table",
                    message="Blank table (all cells empty) - likely a layout table from HTML",
                )
            )
        elif not header_has_content and len(content_rows) == 0:
            # Single-row blank table (just header + separator, no content)
            result.issues.append(
                ValidationIssue(
                    file=md_file,
                    line=start_line,
                    issue_type="warning",
                    category="table",
                    message="Table has only empty header row - likely a layout table from HTML",
                )
            )
        elif header_has_content and len(content_rows) == 0:
            # Header-only table (no data rows)
            result.issues.append(
                ValidationIssue(
                    file=md_file,
                    line=start_line,
                    issue_type="warning",
                    category="table",
                    message="Table has header but no data rows",
                )
            )

    def _extract_table_cells(self, row: str) -> list[str]:
        """Extract cell contents from a markdown table row."""
        # Remove leading/trailing pipes and split
        row = row.strip()
        if row.startswith("|"):
            row = row[1:]
        if row.endswith("|"):
            row = row[:-1]
        return row.split("|")

    def _validate_links(self, md_file: Path, content: str, lines: list[str], result: ValidationResult) -> None:
        """Validate internal and external links."""
        # Pattern for markdown links: [text](url)
        # Exclude image links which start with !
        link_pattern = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)")

        for i, line in enumerate(lines, 1):
            for match in link_pattern.finditer(line):
                text = match.group(1)
                href = match.group(2)

                # Parse the URL
                parsed = urlparse(href)

                # External links - just check format
                if parsed.scheme in ("http", "https", "mailto", "ftp"):
                    if not text.strip():
                        result.issues.append(
                            ValidationIssue(
                                file=md_file,
                                line=i,
                                issue_type="warning",
                                category="link",
                                message=f"External link with empty text: {href}",
                            )
                        )
                    continue

                # Internal links
                href_path = unquote(parsed.path)
                anchor = parsed.fragment

                if not href_path and anchor:
                    # Same-file anchor reference
                    self._validate_anchor(md_file, content, anchor, i, result)
                elif href_path:
                    # Cross-file reference
                    self._validate_internal_link(md_file, href_path, anchor, i, result)

    def _validate_internal_link(
        self, md_file: Path, href_path: str, anchor: Optional[str], line: int, result: ValidationResult
    ) -> None:
        """Validate an internal link to another file."""
        # Resolve the target file path
        if href_path.startswith("/"):
            target_path = self.docs_dir / href_path[1:]
        else:
            target_path = md_file.parent / href_path

        # Normalize
        try:
            target_path = target_path.resolve()
            target_path.relative_to(self.docs_dir.resolve())
        except (ValueError, OSError):
            result.issues.append(
                ValidationIssue(
                    file=md_file,
                    line=line,
                    issue_type="error",
                    category="link",
                    message=f"Invalid link path: {href_path}",
                )
            )
            return

        # Check if target file exists
        if not target_path.exists():
            result.issues.append(
                ValidationIssue(
                    file=md_file,
                    line=line,
                    issue_type="error",
                    category="link",
                    message=f"Broken link - file not found: {href_path}",
                )
            )
            return

        # If there's an anchor, validate it exists in target file
        if anchor:
            try:
                target_content = target_path.read_text(encoding="utf-8")
                self._validate_anchor_in_content(md_file, target_content, anchor, line, href_path, result)
            except Exception as e:
                result.issues.append(
                    ValidationIssue(
                        file=md_file,
                        line=line,
                        issue_type="warning",
                        category="link",
                        message=f"Could not validate anchor in {href_path}: {e}",
                    )
                )

    def _validate_anchor(self, md_file: Path, content: str, anchor: str, line: int, result: ValidationResult) -> None:
        """Validate an anchor reference within the same file."""
        self._validate_anchor_in_content(md_file, content, anchor, line, None, result)

    def _validate_anchor_in_content(
        self, md_file: Path, content: str, anchor: str, line: int, target_file: Optional[str], result: ValidationResult
    ) -> None:
        """Validate that an anchor exists in content."""
        # Look for HTML anchors: <a name="anchor"></a> or <a id="anchor"></a>
        anchor_patterns = [
            rf'<a\s+name="{re.escape(anchor)}"',
            rf'<a\s+id="{re.escape(anchor)}"',
            rf'id="{re.escape(anchor)}"',
            # Markdown extended syntax: {#anchor} at end of header
            rf"\{{#{re.escape(anchor)}\}}",
        ]

        found = False
        for pattern in anchor_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                found = True
                break

        if not found:
            # Try matching as a header anchor (slugified)
            # Convert anchor to potential header match
            # e.g., "some-header" might match "## Some Header"
            # Extract words from anchor and look for them in sequence in headings
            # This handles bold markers, backticks, parentheses, etc.
            words = [w for w in re.split(r"[-_]", anchor) if w]
            if words:
                # Build pattern allowing formatting chars between words
                word_pattern = r"[\s\(\)\*`\-_]*".join(re.escape(w) for w in words)
                if re.search(rf"^#+\s+.*{word_pattern}", content, re.IGNORECASE | re.MULTILINE):
                    found = True

        if not found:
            # Try matching by slugifying all headings and comparing to the anchor
            # This handles cases like "## Add/Edit Label Dialog" -> "addedit-label-dialog"
            heading_pattern = re.compile(r"^#+\s+(.+)$", re.MULTILINE)
            for match in heading_pattern.finditer(content):
                heading_text = match.group(1).strip()
                # Remove markdown image syntax ![alt](src) from heading text
                heading_text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", heading_text)
                # Remove markdown formatting from heading text
                heading_text = re.sub(r"[*_`\[\]()]", "", heading_text)
                # Slugify the heading text (same algorithm as GFM)
                slug = heading_text.lower()
                slug = re.sub(r"[\s_]+", "-", slug)
                slug = re.sub(r"[^a-z0-9-]", "", slug)
                slug = re.sub(r"-+", "-", slug)
                slug = slug.strip("-")
                if slug == anchor:
                    found = True
                    break

        if not found:
            if target_file:
                msg = f"Broken anchor in {target_file}#{anchor}"
            else:
                msg = f"Broken anchor: #{anchor}"
            result.issues.append(
                ValidationIssue(file=md_file, line=line, issue_type="error", category="link", message=msg)
            )


def print_report(report: ValidationReport, verbose: bool = False) -> None:
    """Print a validation report."""
    print("\n" + "=" * 60)
    print("VALIDATION REPORT")
    print("=" * 60)

    print(f"\nTotal files validated: {report.total_files}")
    print(f"Files with errors: {report.files_with_errors}")
    print(f"Files with warnings: {report.files_with_warnings}")
    print(f"Total errors: {report.total_errors}")
    print(f"Total warnings: {report.total_warnings}")

    if report.total_errors > 0 or report.total_warnings > 0:
        # Group issues by category
        by_category: dict[str, list[ValidationIssue]] = {}
        for result in report.results:
            for issue in result.issues:
                if issue.category not in by_category:
                    by_category[issue.category] = []
                by_category[issue.category].append(issue)

        for category in ["render", "image", "table", "link"]:
            if category in by_category:
                issues = by_category[category]
                errors = [i for i in issues if i.issue_type == "error"]
                warnings = [i for i in issues if i.issue_type == "warning"]

                print(f"\n--- {category.upper()} ISSUES ---")
                print(f"  Errors: {len(errors)}, Warnings: {len(warnings)}")

                if verbose or len(errors) <= 20:
                    for issue in errors[:50]:
                        rel_path = issue.file.name
                        print(f"  [ERROR] {rel_path}:{issue.line} - {issue.message}")

                if verbose or len(warnings) <= 10:
                    for issue in warnings[:20]:
                        rel_path = issue.file.name
                        print(f"  [WARN]  {rel_path}:{issue.line} - {issue.message}")

                if not verbose:
                    if len(errors) > 50:
                        print(f"  ... and {len(errors) - 50} more errors")
                    if len(warnings) > 20:
                        print(f"  ... and {len(warnings) - 20} more warnings")

    print("\n" + "=" * 60)
    if report.total_errors == 0:
        print("RESULT: PASSED (no errors)")
    else:
        print(f"RESULT: FAILED ({report.total_errors} errors)")
    print("=" * 60)


def main() -> int:
    """Main entry point for the validator."""
    parser = argparse.ArgumentParser(
        description="Validate generated Markdown documentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ghidra-docs-validator ./docs
  ghidra-docs-validator ./docs --verbose
  ghidra-docs-validator ./docs --file BSimSearchPlugin/BSimSearch.md
        """,
    )

    parser.add_argument("docs_dir", type=Path, help="Path to the docs directory")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed output")
    parser.add_argument("--file", "-f", type=str, default=None, help="Validate only a specific file (relative path)")

    args = parser.parse_args()

    if not args.docs_dir.exists():
        print(f"Error: Directory not found: {args.docs_dir}")
        return 1

    print(f"Validating documentation in: {args.docs_dir}")

    validator = MarkdownValidator(args.docs_dir, verbose=args.verbose)

    if args.file:
        # Validate single file
        file_path = args.docs_dir / args.file
        if not file_path.exists():
            print(f"Error: File not found: {file_path}")
            return 1
        result = validator.validate_file(file_path)
        report = ValidationReport()
        report.add_result(result)
    else:
        # Validate all files
        print("Scanning markdown files...")
        report = validator.validate_all()

    print_report(report, verbose=args.verbose)

    return 0 if report.total_errors == 0 else 1


if __name__ == "__main__":
    exit(main())
