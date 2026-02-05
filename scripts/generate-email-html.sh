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

# Use Python to convert markdown to HTML with nice styling
python3 << PYTHON_SCRIPT
import markdown
from pathlib import Path

# Read the markdown file
md_content = Path("$DRAFT_FILE").read_text()

# Remove the title line and metadata if present (we'll add our own header)
lines = md_content.split('\n')
# Skip the "# Email Draft" line if present
if lines and lines[0].startswith('# '):
    lines = lines[1:]
# Skip the To/Subject lines - we'll handle those in Gmail
content_start = 0
for i, line in enumerate(lines):
    if line.startswith('---'):
        content_start = i + 1
        break
md_content = '\n'.join(lines[content_start:])

# Convert markdown to HTML with table extension
html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

# Wrap in styled HTML template
html_template = '''<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      font-family: Arial, sans-serif;
      max-width: 700px;
      margin: 20px auto;
      padding: 20px;
      line-height: 1.6;
      color: #333;
    }
    h1 {
      color: #1a365d;
      font-size: 20px;
      border-bottom: 2px solid #c9a227;
      padding-bottom: 8px;
    }
    h2 {
      color: #1a365d;
      font-size: 16px;
      margin-top: 24px;
      margin-bottom: 12px;
    }
    h3 {
      color: #1a365d;
      font-size: 14px;
      margin-top: 16px;
    }
    table {
      border-collapse: collapse;
      width: 100%;
      margin: 16px 0;
      font-size: 13px;
    }
    th {
      background: #1a365d;
      color: white;
      padding: 10px;
      text-align: left;
    }
    td {
      padding: 8px 10px;
      border-bottom: 1px solid #e2e8f0;
    }
    tr:nth-child(even) {
      background: #f7fafc;
    }
    ul, ol {
      margin: 8px 0;
      padding-left: 24px;
    }
    li {
      margin: 4px 0;
    }
    a {
      color: #3182ce;
      text-decoration: none;
    }
    a:hover {
      text-decoration: underline;
    }
    strong {
      color: #1a365d;
    }
    em {
      color: #666;
    }
    hr {
      border: none;
      border-top: 1px solid #e2e8f0;
      margin: 24px 0;
    }
    code {
      background: #f7fafc;
      padding: 2px 6px;
      border-radius: 3px;
      font-size: 12px;
    }
  </style>
</head>
<body>
''' + html_content + '''
</body>
</html>'''

# Write the output file
Path("$OUTPUT_FILE").write_text(html_template)
print(f"Generated: $OUTPUT_FILE")
PYTHON_SCRIPT

echo "Opening in browser..."
open "$OUTPUT_FILE"

echo ""
echo "=== Instructions ==="
echo "1. In browser: Cmd+A to select all"
echo "2. Cmd+C to copy"
echo "3. Paste into Gmail compose window"
echo "4. Add recipients and subject line"
echo "5. Attach: PopTop-Execution-Plan-v2.1.pdf"
