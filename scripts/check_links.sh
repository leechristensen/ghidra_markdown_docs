#!/usr/bin/env bash
# Build the mkdocs site in strict mode to validate every link and anchor
# in the converted docs. Strict mode promotes mkdocs's link/anchor
# warnings to errors, so this script exits non-zero if *anything* is off
# — broken `[text](file.md#anchor)`, an unrecognized relative link,
# missing fragment, etc.
#
# Run this after re-running the converter or hand-editing any markdown
# under `docs/`. The script does not require the mkdocs serve task to be
# stopped; it builds into a side directory.
#
# Usage: ./scripts/check_links.sh

set -euo pipefail

cd "$(dirname "$0")/.."

OUTPUT_DIR="$(mktemp -d -t mkdocs-strict-XXXXXX)"
trap 'rm -rf "$OUTPUT_DIR"' EXIT

LOG="$(mktemp -t mkdocs-strict-log-XXXXXX)"
trap 'rm -f "$LOG"' EXIT

echo "Building mkdocs in --strict mode (any warning = failure)..."
if ! uvx --from mkdocs --with mkdocs-literate-nav mkdocs build \
        --strict --site-dir "$OUTPUT_DIR" 2>&1 | tee "$LOG" >/dev/null; then
    echo
    echo "FAIL: mkdocs --strict reported warnings or errors:"
    echo
    grep -E "WARNING|ERROR|Aborted" "$LOG" || true
    exit 1
fi

echo "OK: no broken links or anchors."
