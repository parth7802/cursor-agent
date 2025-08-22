#!/usr/bin/env bash
# Block commits if watermark not found in changed code files

WMK_ID="WMK_PARTH_2025_A1"
PATTERN1="_wp[0-9]"           # identifier suffix like _wp1, _wp2
PATTERN2="$WMK_ID"            # literal ID (e.g., in a comment once per repo)

# Only check staged source files
FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(py|js|ts|tsx|java|go|php)$') || true

if [ -z "$FILES" ]; then
  exit 0
fi

FOUND_PATTERN1=0
FOUND_PATTERN2=0

for f in $FILES; do
  if grep -Eq "$PATTERN1" "$f"; then FOUND_PATTERN1=1; fi
  if grep -Eq "$PATTERN2" "$f"; then FOUND_PATTERN2=1; fi
done

if [ $FOUND_PATTERN1 -eq 0 ] || [ $FOUND_PATTERN2 -eq 0 ]; then
  echo "❌ Watermark missing."
  echo "   Ensure at least one identifier with pattern '$PATTERN1' and one '$WMK_ID' comment exist in changed files."
  echo "   Example:  # $WMK_ID"
  echo "             def compute_tax_wp1(...):"
  exit 1
fi

exit 0
