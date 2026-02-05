#!/bin/bash
# PopTop Meeting Notes Watcher
# Watches for changes to meeting notes and auto-processes them
#
# Usage: ./watch-meeting-notes.sh
# To run in background: nohup ./watch-meeting-notes.sh &
# To stop: pkill -f "watch-meeting-notes"

POPTOP_DIR="${POPTOP_DIR:-$HOME/Projects/poptop}"
NOTES_DIR="$POPTOP_DIR/10-Team-Docs/meeting-notes"
LOG_FILE="$POPTOP_DIR/scripts/watcher.log"

echo "=== PopTop Meeting Notes Watcher ===" | tee -a "$LOG_FILE"
echo "Watching: $NOTES_DIR" | tee -a "$LOG_FILE"
echo "Started: $(date)" | tee -a "$LOG_FILE"
echo ""

# Check if fswatch is installed
if ! command -v fswatch &> /dev/null; then
    echo "Installing fswatch..."
    brew install fswatch
fi

# Function to process a changed file
process_file() {
    local file="$1"
    local filename=$(basename "$file")

    # Only process markdown files
    if [[ ! "$filename" == *.md ]]; then
        return
    fi

    # Skip email drafts
    if [[ "$filename" == *"email-draft"* ]]; then
        return
    fi

    echo ""
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] File changed: $filename" | tee -a "$LOG_FILE"

    # Wait a moment for file to finish saving
    sleep 2

    # Auto-commit and push
    cd "$POPTOP_DIR"

    # Check if there are actual changes
    if git diff --quiet "$file" 2>/dev/null; then
        echo "  No changes to commit" | tee -a "$LOG_FILE"
        return
    fi

    echo "  Adding and committing..." | tee -a "$LOG_FILE"
    git add "$file"
    git commit -m "Update meeting notes: $filename

Auto-committed by watcher script

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"

    echo "  Pushing to GitHub..." | tee -a "$LOG_FILE"
    git push

    echo "  Done!" | tee -a "$LOG_FILE"

    # Play a sound to notify (optional)
    afplay /System/Library/Sounds/Glass.aiff 2>/dev/null &
}

export -f process_file
export POPTOP_DIR LOG_FILE

# Watch for changes
fswatch -0 "$NOTES_DIR" | while IFS= read -r -d '' file; do
    process_file "$file"
done
