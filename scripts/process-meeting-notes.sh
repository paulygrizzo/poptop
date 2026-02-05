#!/bin/bash
# PopTop Meeting Notes Processor
# Usage: ./process-meeting-notes.sh [meeting-date]
# Example: ./process-meeting-notes.sh 2026-02-06

set -e

POPTOP_DIR="${POPTOP_DIR:-$HOME/Projects/poptop}"
MEETING_DATE="${1:-$(date +%Y-%m-%d)}"
NOTES_DIR="$POPTOP_DIR/10-Team-Docs/meeting-notes"

echo "=== PopTop Meeting Notes Processor ==="
echo "Date: $MEETING_DATE"
echo ""

# Find meeting notes file for the date
NOTES_FILE=$(find "$NOTES_DIR" -name "*$MEETING_DATE*" -type f 2>/dev/null | head -1)

if [ -z "$NOTES_FILE" ]; then
    echo "Error: No meeting notes found for $MEETING_DATE"
    echo "Looking in: $NOTES_DIR"
    exit 1
fi

echo "Found: $NOTES_FILE"
echo ""

# Check if Claude CLI is available
if ! command -v claude &> /dev/null; then
    echo "Error: Claude CLI not found. Please install it first."
    exit 1
fi

# Process the meeting notes with Claude
echo "Processing with Claude..."
echo ""

cd "$POPTOP_DIR"

# Use Claude to extract action items and update the notes
claude --print "Read the meeting notes at $NOTES_FILE.

1. Look for any action items indicated by ==Name== highlights or items assigned to specific people
2. Extract them into the Action Items table at the top of the file (if not already there)
3. Make sure each AR has a unique AR# (e.g., AR-001, AR-002)
4. Clean up any ==highlight== markers after extracting

After updating the notes:
1. Show me a summary of the action items found
2. Commit the changes with an appropriate message
3. Push to GitHub"

echo ""
echo "=== Done ==="
