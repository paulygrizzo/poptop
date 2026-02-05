#!/bin/bash
# Generate HTML email preview from meeting notes markdown
#
# Usage: ./generate-email-html.sh [meeting-date]
# Example: ./generate-email-html.sh 2026-02-06
#
# Opens the HTML in your browser - just Cmd+A, Cmd+C, paste into Gmail

set -e

POPTOP_DIR="${POPTOP_DIR:-$HOME/Projects/poptop}"
MEETING_DATE="${1:-$(date +%Y-%m-%d)}"
NOTES_DIR="$POPTOP_DIR/10-Team-Docs/meeting-notes"
OUTPUT_DIR="/tmp/poptop-emails"

mkdir -p "$OUTPUT_DIR"

# Find email draft for the date
DRAFT_FILE=$(find "$NOTES_DIR" -name "*$MEETING_DATE*email-draft*" -type f 2>/dev/null | head -1)

if [ -z "$DRAFT_FILE" ]; then
    # Fall back to agenda file
    DRAFT_FILE=$(find "$NOTES_DIR" -name "*$MEETING_DATE*agenda*" -type f 2>/dev/null | head -1)
fi

if [ -z "$DRAFT_FILE" ]; then
    echo "Error: No meeting notes found for $MEETING_DATE"
    echo "Looking in: $NOTES_DIR"
    exit 1
fi

echo "Processing: $DRAFT_FILE"

OUTPUT_FILE="$OUTPUT_DIR/email-$MEETING_DATE.html"

# Generate HTML with inline styles (Gmail-friendly)
cat > "$OUTPUT_FILE" << 'HTMLHEAD'
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: Arial, sans-serif; max-width: 700px; margin: 20px auto; padding: 20px; line-height: 1.6; color: #333; }
    h1 { color: #1a365d; font-size: 20px; border-bottom: 2px solid #c9a227; padding-bottom: 8px; margin-top: 0; }
    h2 { color: #1a365d; font-size: 16px; margin-top: 24px; margin-bottom: 12px; }
    table { border-collapse: collapse; width: 100%; margin: 16px 0; font-size: 13px; }
    th { background: #1a365d; color: white; padding: 10px; text-align: left; }
    td { padding: 8px 10px; border-bottom: 1px solid #e2e8f0; }
    tr:nth-child(even) { background: #f7fafc; }
    .complete { color: #38a169; font-weight: bold; }
    .open { color: #3182ce; }
    ul, ol { margin: 8px 0; padding-left: 24px; }
    li { margin: 4px 0; }
    a { color: #3182ce; text-decoration: none; }
    a:hover { text-decoration: underline; }
    .header { background: #1a365d; color: white; padding: 16px 20px; margin: -20px -20px 20px -20px; }
    .header h1 { color: white; border: none; margin: 0; }
    .header .gold { color: #c9a227; }
    blockquote { background: #f7fafc; border-left: 4px solid #c9a227; padding: 12px 16px; margin: 16px 0; }
    hr { border: none; border-top: 1px solid #e2e8f0; margin: 24px 0; }
  </style>
</head>
<body>
HTMLHEAD

# Check if pandoc is available
if command -v pandoc &> /dev/null; then
    # Use pandoc for conversion
    pandoc "$DRAFT_FILE" -f markdown -t html >> "$OUTPUT_FILE"
else
    # Simple fallback: basic markdown conversion with sed
    echo "<p><em>Note: Install pandoc for better formatting: brew install pandoc</em></p>" >> "$OUTPUT_FILE"
    echo "<pre style='white-space: pre-wrap; font-family: Arial;'>" >> "$OUTPUT_FILE"
    cat "$DRAFT_FILE" >> "$OUTPUT_FILE"
    echo "</pre>" >> "$OUTPUT_FILE"
fi

cat >> "$OUTPUT_FILE" << 'HTMLFOOT'
</body>
</html>
HTMLFOOT

echo "Generated: $OUTPUT_FILE"
echo "Opening in browser..."

open "$OUTPUT_FILE"

echo ""
echo "=== Instructions ==="
echo "1. In browser: Cmd+A to select all"
echo "2. Cmd+C to copy"
echo "3. Paste into Gmail compose window"
echo "4. Add recipients and subject line"
echo "5. Attach: PopTop-Execution-Plan-v2.1.pdf"
