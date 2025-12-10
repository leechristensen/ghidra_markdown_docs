"""
Main entry point for Ghidra Help to Markdown converter.

Converts Ghidra's HTML help documentation to Markdown files with
proper cross-references, navigation, and table of contents.
"""

import argparse
import re
import shutil
from pathlib import Path
from typing import Optional

from .html_converter import HTMLToMarkdownConverter, slugify
from .icon_resolver import IconResolver
from .link_resolver import LinkResolver, build_link_resolver
from .toc_parser import TOCEntry, TOCTree, build_toc_tree, flatten_toc, get_unique_html_files

# Build-generated artifacts that should be skipped
BUILD_ARTIFACTS = {"Tips.htm", "Tips.html"}


class GhidraHelpConverter:
    """Main converter class that orchestrates the conversion process."""

    def __init__(self, ghidra_root: Path, output_dir: Path, verbose: bool = False) -> None:
        self.ghidra_root = ghidra_root
        self.output_dir = output_dir
        self.verbose = verbose
        self.toc_tree: Optional[TOCTree] = None
        self.html_files: dict[str, list[TOCEntry]] = {}
        self.link_resolver: Optional[LinkResolver] = None
        self.flat_toc: list[TOCEntry] = []
        # Map from html_path -> set of anchors that are referenced in that file
        self.used_anchors: dict[str, set[str]] = {}
        # Additional HTML files discovered via link references (not in TOC)
        self.discovered_files: set[str] = set()
        # Cache: maps topic_path (e.g., "PluginName/File.htm") -> full Path
        # Built once at startup for fast lookups
        self._html_file_cache: dict[str, Path] = {}
        # Icon resolver for programmatic icon references
        self.icon_resolver: Optional[IconResolver] = None

    def log(self, message: str) -> None:
        """Print message if verbose mode is enabled."""
        if self.verbose:
            print(message)

    def _build_html_file_cache(self) -> None:
        """
        Build a cache of all HTML files in help/topics directories.
        This is done once at startup to avoid repeated glob() calls.
        """
        pattern = "**/src/main/help/help/topics/**/*.htm*"
        for path in self.ghidra_root.glob(pattern):
            if path.is_file() and path.suffix.lower() in (".htm", ".html"):
                # Extract the topic path (e.g., "PluginName/File.htm")
                path_str = str(path).replace("\\", "/")
                if "/help/topics/" in path_str:
                    idx = path_str.find("/help/topics/")
                    topic_path = path_str[idx + len("/help/topics/") :]
                    self._html_file_cache[topic_path] = path
                    # Also add lowercase version for case-insensitive lookup
                    self._html_file_cache[topic_path.lower()] = path

    def run(self, module_filter: Optional[str] = None, copy_images: bool = True) -> None:
        """Run the full conversion process."""
        print(f"Converting Ghidra help from {self.ghidra_root}")
        print(f"Output directory: {self.output_dir}")

        # Step 0: Build HTML file cache for fast lookups
        print("\n[0/10] Building HTML file cache...")
        self._build_html_file_cache()
        print(
            f"  Indexed {len(self._html_file_cache) // 2} HTML files"
        )  # Divide by 2 because we store both case variants

        # Initialize icon resolver for programmatic icon references
        print("\n[0.5/10] Initializing icon resolver...")
        self.icon_resolver = IconResolver(self.ghidra_root)
        stats = self.icon_resolver.get_stats()
        print(
            f"  Loaded {stats['icons_field_to_id']} Icons.* mappings, "
            f"{stats['id_to_filename']} icon IDs, {stats['filename_to_path']} icon files"
        )

        # Step 1: Build TOC tree
        print("\n[1/9] Parsing TOC files...")
        self.toc_tree = build_toc_tree(self.ghidra_root)
        self.html_files = get_unique_html_files(self.toc_tree)
        self.flat_toc = flatten_toc(self.toc_tree)
        print(f"  Found {len(self.toc_tree.definitions)} TOC entries")
        print(f"  Found {len(self.html_files)} unique HTML files in TOC")

        # Step 2: Discover referenced HTML files not in TOC
        print("\n[2/9] Discovering referenced HTML files...")
        iteration = 0
        while iteration < 5:  # Safety limit
            iteration += 1
            new_files = self._discover_referenced_html_files()
            if not new_files:
                break
            self.log(f"  Iteration {iteration}: Found {len(new_files)} additional files")
            self.discovered_files.update(new_files)

        if self.discovered_files:
            print(f"  Discovered {len(self.discovered_files)} additional files via link references")
        else:
            print("  No additional files discovered")

        # Step 3: Build link resolver (including discovered files)
        print("\n[3/9] Building link resolver...")
        # Combine TOC files and discovered files for link resolution
        all_html_files = dict(self.html_files)
        for html_path in self.discovered_files:
            if html_path not in all_html_files:
                # Create empty entry for discovered files (not in TOC)
                all_html_files[html_path] = []
        self.link_resolver = build_link_resolver(all_html_files)
        print(f"  Mapped {len(self.link_resolver.html_to_md_map)} paths")

        # Step 4: Collect referenced anchors (pass 1)
        print("\n[4/9] Collecting referenced anchors...")
        self._collect_used_anchors()
        total_anchors = sum(len(v) for v in self.used_anchors.values())
        print(f"  Found {total_anchors} anchor references across {len(self.used_anchors)} files")

        # Step 5: Create output directory structure
        print("\n[5/9] Creating output directory structure...")
        self._create_output_structure()

        # Step 6: Convert HTML files to Markdown
        print("\n[6/9] Converting HTML files to Markdown...")
        converted_count, image_mismatches, code_block_mismatches = self._convert_all_html_files(module_filter)
        print(f"  Converted {converted_count} files")
        if image_mismatches:
            print(f"  WARNING: {len(image_mismatches)} files with image count mismatches")
            for file_path, msg in image_mismatches[:10]:  # Show first 10
                print(f"    - {file_path}")
            if len(image_mismatches) > 10:
                print(f"    ... and {len(image_mismatches) - 10} more")
        if code_block_mismatches:
            print(f"  WARNING: {len(code_block_mismatches)} files with code block count mismatches")
            for file_path, msg in code_block_mismatches[:10]:  # Show first 10
                print(f"    - {file_path}: {msg}")
            if len(code_block_mismatches) > 10:
                print(f"    ... and {len(code_block_mismatches) - 10} more")

        # Step 7: Convert external docs and generate special files
        print("\n[7/10] Converting external docs and special files...")
        extra_count = self._convert_external_docs()
        print(f"  Converted {extra_count} external docs")

        # Step 8: Copy images
        if copy_images:
            print("\n[8/10] Copying images...")
            image_count = self._copy_images()
            print(f"  Copied {image_count} images")
        else:
            print("\n[8/10] Skipping image copy")

        # Step 9: Generate index files
        print("\n[9/10] Generating index files...")
        self._generate_master_index()
        self._generate_module_indexes()
        print("  Generated index files")

        # Step 10: Validate links
        print("\n[10/10] Validating links...")
        broken_links = self._validate_links()
        if broken_links:
            print(f"  WARNING: {len(broken_links)} broken links found")
            for source_file, link, link_text in broken_links[:20]:  # Show first 20
                # Use ASCII-safe output to avoid encoding errors on Windows
                safe_text = link_text.encode("ascii", "replace").decode("ascii")
                print(f"    - {source_file}: [{safe_text}]({link})")
            if len(broken_links) > 20:
                print(f"    ... and {len(broken_links) - 20} more")
        else:
            print("  All links validated successfully")

        print("\n[OK] Conversion complete!")
        print(f"  Output: {self.output_dir}")

    def _collect_used_anchors(self) -> None:
        """
        Scan all HTML files to collect anchors that are actually referenced.

        This builds a map from html_path -> set of anchor names that are targeted
        by links (either within the same file or from other files).
        """
        # Pattern to match href attributes with anchors
        # Matches: href="#anchor" or href="path#anchor" or href="path.htm#anchor"
        href_pattern = re.compile(r'href=["\']([^"\']*#([^"\']+))["\']', re.IGNORECASE)

        # Scan both TOC files and discovered files
        all_html_paths = set(self.html_files.keys()) | self.discovered_files

        for html_path in all_html_paths:
            source_path = self._find_source_file(html_path)
            if not source_path or not source_path.exists():
                continue

            # Read the HTML file
            try:
                for encoding in ["utf-8", "windows-1252", "iso-8859-1"]:
                    try:
                        content = source_path.read_text(encoding=encoding)
                        break
                    except UnicodeDecodeError:
                        continue
                else:
                    content = source_path.read_text(encoding="utf-8", errors="ignore")

                # Find all href values with anchors
                for match in href_pattern.finditer(content):
                    full_href = match.group(1)
                    anchor = match.group(2)

                    # Determine the target file
                    if full_href.startswith("#"):
                        # Same file reference
                        target_html_path = html_path
                    else:
                        # Cross-file reference - extract the file path
                        href_path = full_href.split("#")[0]
                        # Normalize the path
                        href_path = href_path.replace("\\", "/")

                        if href_path.startswith("help/topics/"):
                            target_html_path = href_path
                        elif not href_path.startswith(("http://", "https://", "mailto:")):
                            # Relative path - resolve it
                            if html_path.startswith("help/topics/"):
                                base_dir = "/".join(html_path.split("/")[:-1])
                                target_html_path = f"{base_dir}/{href_path}"
                                # Normalize .. in path
                                parts = target_html_path.split("/")
                                normalized = []
                                for part in parts:
                                    if part == "..":
                                        if normalized:
                                            normalized.pop()
                                    elif part != ".":
                                        normalized.append(part)
                                target_html_path = "/".join(normalized)
                            else:
                                target_html_path = href_path
                        else:
                            # External URL, skip
                            continue

                    # Add the anchor to the target file's set (slugified for markdown compatibility)
                    if target_html_path not in self.used_anchors:
                        self.used_anchors[target_html_path] = set()
                    slug = slugify(anchor)
                    if slug:
                        self.used_anchors[target_html_path].add(slug)

            except Exception as e:
                self.log(f"  Warning: Error scanning {html_path}: {e}")

        # Also add anchors referenced by TOC entries (for index links)
        def add_toc_anchors(entry: TOCEntry) -> None:
            if entry.target and entry.anchor:
                # Normalize target path
                target = entry.target.replace("\\", "/")
                if target not in self.used_anchors:
                    self.used_anchors[target] = set()
                slug = slugify(entry.anchor)
                if slug:
                    self.used_anchors[target].add(slug)
            for child in entry.children:
                add_toc_anchors(child)

        for entry in self.toc_tree.entries:
            add_toc_anchors(entry)

    def _create_output_structure(self) -> None:
        """Create the output directory structure."""
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Create shared directory for common images
        (self.output_dir / "shared").mkdir(exist_ok=True)

        # Create directories for each module (including discovered files)
        modules = set()
        all_html_paths = set(self.html_files.keys()) | self.discovered_files
        for html_path in all_html_paths:
            if html_path.startswith("help/topics/"):
                parts = html_path[len("help/topics/") :].split("/")
                if parts:
                    modules.add(parts[0])

        for module in modules:
            (self.output_dir / module).mkdir(exist_ok=True)
            (self.output_dir / module / "images").mkdir(exist_ok=True)

    def _convert_all_html_files(
        self, module_filter: Optional[str] = None
    ) -> tuple[int, list[tuple[str, str]], list[tuple[str, str]]]:
        """Convert all HTML files to Markdown.

        Uses a two-pass approach:
        1. First pass: Convert all HTML to Markdown, collect anchor mappings
        2. Second pass: Resolve links using the complete anchor mapping

        Returns:
            Tuple of (converted_count, image_mismatches, code_block_mismatches) where:
            - image_mismatches is a list of (file_path, message) tuples for files with image count issues
            - code_block_mismatches is a list of (file_path, message) tuples for files with code block issues
        """
        converted = 0
        image_mismatches: list[tuple[str, str]] = []
        code_block_mismatches: list[tuple[str, str]] = []

        # Build a mapping from HTML files to their previous/next entries
        flat_entries_with_targets = [e for e in self.flat_toc if e.target]
        prev_next_map = {}
        for i, entry in enumerate(flat_entries_with_targets):
            prev_entry = flat_entries_with_targets[i - 1] if i > 0 else None
            next_entry = flat_entries_with_targets[i + 1] if i < len(flat_entries_with_targets) - 1 else None
            if entry.target:
                target = entry.target.replace("\\", "/")
                prev_next_map[target] = (prev_entry, entry, next_entry)

        # Combine TOC files and discovered files
        all_files_to_convert: dict[str, list[TOCEntry]] = dict(self.html_files)
        for html_path in self.discovered_files:
            if html_path not in all_files_to_convert:
                all_files_to_convert[html_path] = []

        # Store converted markdown content for second pass
        converted_files: list[tuple[str, str, str, Optional[tuple]]] = []  # (html_path, rel_path, markdown, prev_next)

        # PASS 1: Convert all HTML files to Markdown and collect anchor mappings
        for html_path, entries in all_files_to_convert.items():
            # Apply module filter
            if module_filter:
                if not html_path.startswith(f"help/topics/{module_filter}/"):
                    continue

            # Find the source file
            source_path = self._find_source_file(html_path)
            if not source_path or not source_path.exists():
                self.log(f"  Warning: Source file not found for {html_path}")
                continue

            # Determine output path
            if html_path.startswith("help/topics/"):
                rel_path = html_path[len("help/topics/") :]
            else:
                rel_path = html_path

            # Change extension to .md
            if rel_path.endswith(".htm"):
                rel_path = rel_path[:-4] + ".md"
            elif rel_path.endswith(".html"):
                rel_path = rel_path[:-5] + ".md"

            output_path = self.output_dir / rel_path

            # Convert the file
            try:
                # Get the set of anchors that are actually used for this file
                file_used_anchors = self.used_anchors.get(html_path, set())
                converter = HTMLToMarkdownConverter(
                    used_anchors=file_used_anchors,
                    icon_resolver=self.icon_resolver,
                    output_dir=self.output_dir,
                    output_md_path=output_path,  # Pass output path for correct icon relative paths
                )
                markdown = converter.convert_file(source_path)

                # Collect anchor mappings from this file
                if converter.anchor_to_heading_slug:
                    self.link_resolver.add_anchor_mappings(rel_path, converter.anchor_to_heading_slug)

                # Validate image counts
                is_valid, img_msg = converter.validate_image_counts()
                if not is_valid:
                    image_mismatches.append((rel_path, img_msg))
                    self.log(f"  WARNING: {rel_path} - {img_msg}")

                # Validate code block counts
                is_valid, code_msg = converter.validate_code_block_counts()
                if not is_valid:
                    code_block_mismatches.append((rel_path, code_msg))
                    self.log(f"  WARNING: {rel_path} - {code_msg}")

                # Store for second pass
                prev_next = prev_next_map.get(html_path)
                converted_files.append((html_path, rel_path, markdown, prev_next))

                self.log(f"  Converted: {rel_path}")

            except Exception as e:
                print(f"  Error converting {html_path}: {e}")

        # PASS 2: Resolve links and write files (now that all anchor mappings are collected)
        for html_path, rel_path, markdown, prev_next in converted_files:
            try:
                # Resolve links using complete anchor mapping
                markdown = self.link_resolver.transform_markdown_links(markdown, rel_path)

                # Add navigation
                if prev_next:
                    prev_entry, current_entry, next_entry = prev_next
                    markdown = self._add_navigation(markdown, rel_path, prev_entry, current_entry, next_entry)

                # Write output
                output_path = self.output_dir / rel_path
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(markdown, encoding="utf-8")
                converted += 1

            except Exception as e:
                print(f"  Error writing {rel_path}: {e}")

        return converted, image_mismatches, code_block_mismatches

    def _find_source_file(self, html_path: str) -> Optional[Path]:
        """Find the source file for an HTML path using the cache."""
        # html_path is like "help/topics/PluginName/File.htm"
        # Extract the topic path
        if html_path.startswith("help/topics/"):
            topic_path = html_path[len("help/topics/") :]
        else:
            topic_path = html_path

        # Try exact match in cache
        if topic_path in self._html_file_cache:
            return self._html_file_cache[topic_path]

        # Try lowercase match
        if topic_path.lower() in self._html_file_cache:
            return self._html_file_cache[topic_path.lower()]

        # Try alternate extension
        if topic_path.endswith(".htm"):
            alt_path = topic_path[:-4] + ".html"
        elif topic_path.endswith(".html"):
            alt_path = topic_path[:-5] + ".htm"
        else:
            return None

        if alt_path in self._html_file_cache:
            return self._html_file_cache[alt_path]
        if alt_path.lower() in self._html_file_cache:
            return self._html_file_cache[alt_path.lower()]

        return None

    def _resolve_html_path(self, source_path: Path, rel_path: str) -> Optional[Path]:
        """
        Resolve an HTML path relative to a source file, handling .htm/.html variations.
        Uses the cache for fast lookups.

        Args:
            source_path: The source HTML file containing the reference
            rel_path: The relative path from the href

        Returns:
            Path to the resolved file, or None if not found
        """
        # Clean up the path
        rel_path = rel_path.replace("\\", "/")

        # Handle absolute help/topics paths - use cache
        if "help/topics/" in rel_path:
            topics_idx = rel_path.find("help/topics/")
            topic_path = rel_path[topics_idx + len("help/topics/") :]
            # Use _find_source_file which already uses the cache
            return self._find_source_file(f"help/topics/{topic_path}")

        # Handle relative paths from source file
        target = source_path.parent / rel_path
        if target.exists():
            # Resolve to normalize paths with ..
            return target.resolve()

        # Try alternate extension
        if rel_path.endswith(".htm"):
            alt_path = rel_path[:-4] + ".html"
        elif rel_path.endswith(".html"):
            alt_path = rel_path[:-5] + ".htm"
        else:
            return None

        target = source_path.parent / alt_path
        return target.resolve() if target.exists() else None

    def _discover_referenced_html_files(self) -> set[str]:
        """
        Scan all HTML files to find referenced HTML files not yet in the conversion set.

        This discovers "orphaned" files that are linked from other documentation
        but not listed in any TOC_Source.xml.

        Returns:
            Set of new html_path strings (like "help/topics/Module/File.htm")
        """
        referenced_files: set[str] = set()
        # Match href with optional anchor: href="file.htm" or href="file.htm#anchor"
        # Allow whitespace/newlines between href= and the quote (some HTML files wrap long attributes)
        href_pattern = re.compile(r'href=\s*["\']([^"\'#]+\.html?)(?:#[^"\']*)?["\']', re.IGNORECASE)

        # Scan all files we're currently planning to convert
        all_current_paths = set(self.html_files.keys()) | self.discovered_files

        for html_path in all_current_paths:
            source_path = self._find_source_file(html_path)
            if not source_path or not source_path.exists():
                continue

            # Skip build artifacts
            if source_path.name in BUILD_ARTIFACTS:
                continue

            try:
                # Try different encodings
                content = None
                for encoding in ["utf-8", "windows-1252", "iso-8859-1"]:
                    try:
                        content = source_path.read_text(encoding=encoding)
                        break
                    except UnicodeDecodeError:
                        continue

                if content is None:
                    content = source_path.read_text(encoding="utf-8", errors="ignore")

                # Find all href values pointing to HTML files
                for match in href_pattern.finditer(content):
                    href = match.group(1)

                    # Skip external links
                    if href.startswith(("http://", "https://", "mailto:", "ftp://")):
                        continue

                    # Skip build artifacts
                    href_filename = href.split("/")[-1].split("?")[0]
                    if href_filename in BUILD_ARTIFACTS:
                        continue

                    # Resolve the target file
                    target_path = self._resolve_html_path(source_path, href)
                    if not target_path or not target_path.exists():
                        continue

                    # Convert to html_path format
                    # Find the topics directory to get the canonical path
                    try:
                        path_str = str(target_path).replace("\\", "/")
                        if "/help/topics/" in path_str:
                            idx = path_str.find("/help/topics/")
                            new_html_path = "help/topics/" + path_str[idx + len("/help/topics/") :]

                            # Check if we already have this file
                            if new_html_path not in all_current_paths:
                                referenced_files.add(new_html_path)
                    except Exception:
                        continue

            except Exception as e:
                self.log(f"  Warning: Error scanning {html_path}: {e}")

        return referenced_files

    def _add_navigation(
        self,
        markdown: str,
        current_path: str,
        prev_entry: Optional[TOCEntry],
        current_entry: TOCEntry,
        next_entry: Optional[TOCEntry],
    ) -> str:
        """Add breadcrumb and prev/next navigation to the markdown."""
        # Build breadcrumb with correct relative paths based on depth
        parts = current_path.split("/")
        module_name = parts[0] if parts else ""
        depth = len(parts) - 1  # Number of directories deep (file itself doesn't count)

        # Build relative paths based on depth
        # For Module/File.md (depth=1): Home=../index.md, Module=index.md
        # For Module/subdir/File.md (depth=2): Home=../../index.md, Module=../index.md
        home_path = "../" * depth + "index.md" if depth > 0 else "index.md"
        module_index_path = "../" * (depth - 1) + "index.md" if depth > 1 else "index.md"

        breadcrumb = f"[Home]({home_path}) > [{module_name}]({module_index_path})"
        if current_entry:
            breadcrumb += f" > {current_entry.text}"

        # Build prev/next links
        nav_links = []

        if prev_entry and prev_entry.target:
            prev_path = self._get_relative_md_path(prev_entry.target, current_path)
            nav_links.append(f"[← Previous: {prev_entry.text}]({prev_path})")

        if next_entry and next_entry.target:
            next_path = self._get_relative_md_path(next_entry.target, current_path)
            nav_links.append(f"[Next: {next_entry.text} →]({next_path})")

        nav_bar = " | ".join(nav_links) if nav_links else ""

        # Combine
        header = f"{breadcrumb}\n\n"
        footer = f"\n\n---\n\n{nav_bar}\n" if nav_bar else ""

        return header + markdown + footer

    def _get_relative_md_path(self, html_path: str, current_path: str) -> str:
        """Get relative markdown path from current file to target."""
        # Normalize
        html_path = html_path.replace("\\", "/")

        # Remove anchor
        if "#" in html_path:
            html_path, anchor = html_path.split("#", 1)
            anchor = "#" + anchor
        else:
            anchor = ""

        # Handle external docs (e.g., "external:docs/WhatsNew.html")
        if html_path.startswith("external:"):
            external_path = html_path[len("external:") :]
            if external_path.endswith(".html"):
                external_path = external_path[:-5] + ".md"
            elif external_path.endswith(".htm"):
                external_path = external_path[:-4] + ".md"
            # Calculate relative path from current file to external doc
            current_dir = Path(current_path).parent
            depth = len(current_dir.parts) if current_dir.parts else 0
            return "../" * depth + external_path + anchor

        # Convert to md path
        if html_path.startswith("help/topics/"):
            md_path = html_path[len("help/topics/") :]
        else:
            md_path = html_path

        if md_path.endswith(".htm"):
            md_path = md_path[:-4] + ".md"
        elif md_path.endswith(".html"):
            md_path = md_path[:-5] + ".md"

        # Make relative
        current_dir = Path(current_path).parent
        target = Path(md_path)

        try:
            relative = target.relative_to(current_dir)
            return str(relative).replace("\\", "/") + anchor
        except ValueError:
            # Calculate relative path manually
            current_parts = list(current_dir.parts)
            target_parts = list(target.parts)

            # Find common prefix
            common = 0
            for c, t in zip(current_parts, target_parts):
                if c == t:
                    common += 1
                else:
                    break

            # Build path
            up = len(current_parts) - common
            down = target_parts[common:]
            result = "/".join([".."] * up + list(down))
            return result + anchor

    def _copy_images(self) -> int:
        """Copy images to the output directory."""
        copied = 0

        # Copy shared images
        shared_patterns = [
            "**/src/main/help/help/shared/*",
            "**/src/main/resources/help/shared/*",
        ]

        shared_dir = self.output_dir / "shared"
        for pattern in shared_patterns:
            for img_path in self.ghidra_root.glob(pattern):
                if img_path.is_file() and img_path.suffix.lower() in (".png", ".gif", ".jpg", ".jpeg", ".svg", ".css"):
                    dest = shared_dir / img_path.name
                    if not dest.exists():
                        shutil.copy2(img_path, dest)
                        copied += 1

        # Copy topic images (including from discovered files)
        all_html_paths = set(self.html_files.keys()) | self.discovered_files
        copied_dirs = set()  # Track which directories we've already processed

        for html_path in all_html_paths:
            if html_path.startswith("help/topics/"):
                topic_dir = html_path[len("help/topics/") :].rsplit("/", 1)[0]

                # Skip if we've already copied images from this directory
                if topic_dir in copied_dirs:
                    continue
                copied_dirs.add(topic_dir)

                images_pattern = f"**/src/main/help/help/topics/{topic_dir}/images/*"

                for img_path in self.ghidra_root.glob(images_pattern):
                    if img_path.is_file():
                        dest_dir = self.output_dir / topic_dir / "images"
                        dest_dir.mkdir(parents=True, exist_ok=True)
                        dest = dest_dir / img_path.name
                        if not dest.exists():
                            shutil.copy2(img_path, dest)
                            copied += 1

        return copied

    def _convert_external_docs(self) -> int:
        """
        Convert external documentation files and generate special files.

        This handles:
        1. README_PDB.html - PDB Parser documentation
        2. WhatsNew.md - What's New in Ghidra (already markdown, just copy)
        3. tips.txt - Tips of the Day (converted to Tips.md)
        """
        converted = 0

        # External HTML docs to convert (pattern -> output path)
        external_html_docs = {
            "**/PDB/src/global/docs/README_PDB.html": "docs/README_PDB.md",
            "**/GhidraDocs/InstallationGuide.html": "docs/InstallationGuide.md",
        }

        # External markdown docs to copy (pattern -> output path)
        external_md_docs = {
            "**/Public_Release/src/global/docs/WhatsNew.md": "docs/WhatsNew.md",
            "**/Public_Release/src/global/docs/ChangeHistory.md": "docs/ChangeHistory.md",
        }

        # Create docs directory
        docs_dir = self.output_dir / "docs"
        docs_dir.mkdir(exist_ok=True)

        # Convert HTML docs
        for pattern, output_path in external_html_docs.items():
            matches = list(self.ghidra_root.glob(pattern))
            if matches:
                source_path = matches[0]
                try:
                    # Read and convert
                    content = source_path.read_text(encoding="utf-8", errors="replace")
                    converter = HTMLToMarkdownConverter()
                    markdown = converter.convert(content)

                    # Write output
                    output_file = self.output_dir / output_path
                    output_file.parent.mkdir(parents=True, exist_ok=True)
                    output_file.write_text(markdown, encoding="utf-8")

                    self.log(f"  Converted: {output_path}")
                    converted += 1
                except Exception as e:
                    print(f"  Error converting {source_path}: {e}")

        # Copy markdown docs (fix links as needed)
        for pattern, output_path in external_md_docs.items():
            matches = list(self.ghidra_root.glob(pattern))
            if matches:
                source_path = matches[0]
                try:
                    # Read markdown content
                    markdown = source_path.read_text(encoding="utf-8", errors="replace")

                    # Fix links in docs that reference sibling files
                    markdown = markdown.replace("](InstallationGuide.html)", "](InstallationGuide.md)")
                    markdown = markdown.replace("](ChangeHistory.html)", "](ChangeHistory.md)")

                    # Write output
                    output_file = self.output_dir / output_path
                    output_file.parent.mkdir(parents=True, exist_ok=True)
                    output_file.write_text(markdown, encoding="utf-8")

                    self.log(f"  Copied: {output_path}")
                    converted += 1
                except Exception as e:
                    print(f"  Error copying {source_path}: {e}")

        # Generate Tips.md from tips.txt
        tips_pattern = "**/Base/src/main/resources/ghidra/app/plugin/core/totd/tips.txt"
        tips_matches = list(self.ghidra_root.glob(tips_pattern))
        if tips_matches:
            tips_path = tips_matches[0]
            try:
                tips_content = tips_path.read_text(encoding="utf-8")
                tips_md = self._generate_tips_markdown(tips_content)

                # Create Misc directory if it doesn't exist
                misc_dir = self.output_dir / "Misc"
                misc_dir.mkdir(exist_ok=True)

                tips_output = misc_dir / "Tips.md"
                tips_output.write_text(tips_md, encoding="utf-8")

                self.log("  Generated: Misc/Tips.md")
                converted += 1
            except Exception as e:
                print(f"  Error generating Tips.md: {e}")

        return converted

    def _generate_tips_markdown(self, tips_content: str) -> str:
        """Generate a Markdown file from tips.txt content."""
        lines = ["# Tips of the Day", "", "A collection of useful tips for working with Ghidra.", ""]

        tips = []
        current_tip = []

        for line in tips_content.split("\n"):
            line = line.strip()
            if line:
                current_tip.append(line)
            else:
                if current_tip:
                    tips.append(" ".join(current_tip))
                    current_tip = []

        # Don't forget the last tip
        if current_tip:
            tips.append(" ".join(current_tip))

        # Format as numbered list
        for i, tip in enumerate(tips, 1):
            lines.append(f"{i}. {tip}")
            lines.append("")

        lines.append("---")
        lines.append("")
        lines.append("*Tips extracted from Ghidra's Tips of the Day feature*")
        lines.append("")

        return "\n".join(lines)

    def _generate_master_index(self) -> None:
        """Generate the master index.md file with Welcome content."""
        # Copy the Ghidra logo to the output directory
        logo_pattern = "**/src/main/resources/images/GHIDRA_1.png"
        logo_matches = list(self.ghidra_root.glob(logo_pattern))
        if logo_matches:
            images_dir = self.output_dir / "images"
            images_dir.mkdir(exist_ok=True)
            dest = images_dir / "GHIDRA_1.png"
            if not dest.exists():
                shutil.copy2(logo_matches[0], dest)

        lines = [
            "# Welcome to Ghidra Help",
            "",
            "![Ghidra Logo](images/GHIDRA_1.png)",
            "",
            "Ghidra provides context sensitive help on menu items, dialogs, buttons,",
            "and tool windows. To access the help, press **F1** or **Help** on",
            "any menu item or dialog. If specific help is not available for an item,",
            "this page will be displayed.",
            "",
            "---",
            "",
            "## What's New",
            "",
            "- [What's New in Ghidra](docs/WhatsNew.md)",
            "- [Change History](docs/ChangeHistory.md)",
            "",
            "---",
            "",
            "## Table of Contents",
            "",
        ]

        def write_entry(entry: TOCEntry, level: int = 0) -> None:
            indent = "  " * level
            if entry.target:
                target = entry.target

                # Handle external docs (e.g., "external:docs/WhatsNew.html")
                if target.startswith("external:"):
                    external_path = target[len("external:") :]
                    if external_path.endswith(".html"):
                        external_path = external_path[:-5] + ".md"
                    elif external_path.endswith(".htm"):
                        external_path = external_path[:-4] + ".md"
                    lines.append(f"{indent}- [{entry.text}]({external_path})")
                    for child in entry.children:
                        write_entry(child, level + 1)
                    return

                # Get the markdown path
                if target.startswith("help/topics/"):
                    md_path = target[len("help/topics/") :]
                else:
                    md_path = target

                # Remove anchor for file path
                if "#" in md_path:
                    md_path = md_path.split("#")[0]

                if md_path.endswith(".htm"):
                    md_path = md_path[:-4] + ".md"
                elif md_path.endswith(".html"):
                    md_path = md_path[:-5] + ".md"

                # Add anchor if this entry has one (points to a section)
                # Slugify and resolve the anchor for markdown compatibility
                anchor_suffix = ""
                if entry.anchor:
                    anchor_slug = slugify(entry.anchor)
                    resolved_anchor = self.link_resolver._resolve_anchor(anchor_slug, md_path)
                    anchor_suffix = f"#{resolved_anchor}"

                lines.append(f"{indent}- [{entry.text}]({md_path}{anchor_suffix})")
            else:
                lines.append(f"{indent}- **{entry.text}**")

            for child in entry.children:
                write_entry(child, level + 1)

        for entry in self.toc_tree.entries:
            # Skip "What's New" since it's already at the top
            if entry.target and entry.target.startswith("external:docs/WhatsNew"):
                continue
            write_entry(entry)

        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("*Generated from Ghidra HTML help documentation*")
        lines.append("")

        index_path = self.output_dir / "index.md"
        index_path.write_text("\n".join(lines), encoding="utf-8")

    def _generate_module_indexes(self) -> None:
        """Generate index.md files for each module."""
        # Group entries by module
        modules: dict[str, list[TOCEntry]] = {}

        for html_path, entries in self.html_files.items():
            if html_path.startswith("help/topics/"):
                parts = html_path[len("help/topics/") :].split("/")
                if parts:
                    module = parts[0]
                    if module not in modules:
                        modules[module] = []
                    modules[module].extend(entries)

        for module, entries in modules.items():
            lines = [
                f"# {module}",
                "",
                "[← Back to Home](../index.md)",
                "",
                "## Contents",
                "",
            ]

            # Deduplicate entries
            seen_ids = set()
            unique_entries = []
            for entry in entries:
                if entry.id not in seen_ids:
                    seen_ids.add(entry.id)
                    unique_entries.append(entry)

            # Sort by sortgroup
            unique_entries.sort(key=lambda e: e.sortgroup)

            for entry in unique_entries:
                if entry.target:
                    # Get relative path within module
                    if entry.target.startswith("help/topics/"):
                        rel_path = entry.target[len("help/topics/") :]
                        if rel_path.startswith(f"{module}/"):
                            rel_path = rel_path[len(f"{module}/") :]
                    else:
                        rel_path = entry.target

                    if "#" in rel_path:
                        rel_path = rel_path.split("#")[0]

                    if rel_path.endswith(".htm"):
                        rel_path = rel_path[:-4] + ".md"
                    elif rel_path.endswith(".html"):
                        rel_path = rel_path[:-5] + ".md"

                    # Add anchor if this entry has one (points to a section)
                    # Slugify and resolve the anchor for markdown compatibility
                    anchor_suffix = ""
                    if entry.anchor:
                        anchor_slug = slugify(entry.anchor)
                        # Compute full md path for anchor resolution
                        target_md_path = f"{module}/{rel_path}"
                        resolved_anchor = self.link_resolver._resolve_anchor(anchor_slug, target_md_path)
                        anchor_suffix = f"#{resolved_anchor}"

                    lines.append(f"- [{entry.text}]({rel_path}{anchor_suffix})")

            lines.append("")

            index_path = self.output_dir / module / "index.md"
            index_path.parent.mkdir(parents=True, exist_ok=True)
            index_path.write_text("\n".join(lines), encoding="utf-8")

    def _validate_links(self) -> list[tuple[str, str, str]]:
        """
        Validate all internal links in the generated markdown files.

        Scans all .md files in the output directory and checks that each
        internal link points to an existing file (and optionally anchor).

        Returns:
            List of (source_file, broken_link, link_text) tuples for broken links
        """
        broken_links: list[tuple[str, str, str]] = []

        # Pattern to match markdown links: [text](url)
        # Captures: group(1)=text, group(2)=url
        link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

        # Scan all markdown files
        for md_file in self.output_dir.rglob("*.md"):
            try:
                content = md_file.read_text(encoding="utf-8")
                rel_source = md_file.relative_to(self.output_dir)

                for match in link_pattern.finditer(content):
                    link_text = match.group(1)
                    href = match.group(2)

                    # Skip external links
                    if href.startswith(("http://", "https://", "mailto:", "ftp://")):
                        continue

                    # Skip image links (these are checked by image validation)
                    if href.startswith("images/") or "/images/" in href:
                        continue

                    # Parse the link
                    if "#" in href:
                        file_path, _ = href.split("#", 1)
                    else:
                        file_path = href

                    # Skip empty file paths (same-file anchors)
                    if not file_path:
                        # TODO: Could validate anchor exists in same file
                        continue

                    # Resolve the target path
                    if file_path.startswith("/"):
                        # Absolute path from docs root
                        target_path = self.output_dir / file_path[1:]
                    else:
                        # Relative path from current file
                        target_path = md_file.parent / file_path

                    # Normalize the path
                    try:
                        target_path = target_path.resolve()
                    except OSError:
                        broken_links.append((str(rel_source), href, link_text))
                        continue

                    # Check if target exists
                    if not target_path.exists():
                        broken_links.append((str(rel_source), href, link_text))
                        self.log(f"  Broken link in {rel_source}: [{link_text}]({href})")

            except Exception as e:
                self.log(f"  Warning: Error validating {md_file}: {e}")

        return broken_links


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Convert Ghidra HTML help documentation to Markdown",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ghidra-help-to-markdown /path/to/ghidra ./docs
  ghidra-help-to-markdown /path/to/ghidra ./docs --module Decompiler
  ghidra-help-to-markdown /path/to/ghidra ./docs --no-images --verbose
        """,
    )

    parser.add_argument("ghidra_root", type=Path, help="Path to Ghidra source root directory")
    parser.add_argument("output_dir", type=Path, help="Output directory for Markdown files")
    parser.add_argument("--module", "-m", type=str, default=None, help="Process only a specific module")
    parser.add_argument("--no-images", action="store_true", help="Skip copying images")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed progress")

    args = parser.parse_args()

    converter = GhidraHelpConverter(
        ghidra_root=args.ghidra_root,
        output_dir=args.output_dir,
        verbose=args.verbose,
    )

    converter.run(
        module_filter=args.module,
        copy_images=not args.no_images,
    )


if __name__ == "__main__":
    main()
