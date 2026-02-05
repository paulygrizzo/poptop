#!/bin/bash
# PopTop Automation Tools
# Quick launcher for all PopTop scripts
#
# Usage: ./poptop-tools.sh [command]
#
# Commands:
#   watch     - Start watching for meeting note changes (auto-commit/push)
#   email     - Generate HTML email from today's meeting notes
#   email [date] - Generate HTML email for specific date (YYYY-MM-DD)
#   process   - Process meeting notes with Claude
#   status    - Show automation status
#   help      - Show this help

POPTOP_DIR="${POPTOP_DIR:-$HOME/Projects/poptop}"
SCRIPTS_DIR="$POPTOP_DIR/scripts"

case "${1:-help}" in
    watch)
        echo "Starting meeting notes watcher..."
        echo "Press Ctrl+C to stop"
        "$SCRIPTS_DIR/watch-meeting-notes.sh"
        ;;

    email)
        DATE="${2:-$(date +%Y-%m-%d)}"
        "$SCRIPTS_DIR/generate-email-html.sh" "$DATE"
        ;;

    process)
        DATE="${2:-$(date +%Y-%m-%d)}"
        "$SCRIPTS_DIR/process-meeting-notes.sh" "$DATE"
        ;;

    status)
        echo "=== PopTop Automation Status ==="
        echo ""

        # Check if watcher is running
        if pgrep -f "watch-meeting-notes" > /dev/null; then
            echo "File Watcher: RUNNING"
        else
            echo "File Watcher: NOT RUNNING (start with: poptop watch)"
        fi

        # Check git status
        echo ""
        echo "Git Status:"
        cd "$POPTOP_DIR" && git status -s

        # Check recent commits
        echo ""
        echo "Recent Commits:"
        cd "$POPTOP_DIR" && git log --oneline -3

        # Check if fswatch is installed
        echo ""
        echo "Dependencies:"
        if command -v fswatch &> /dev/null; then
            echo "  fswatch: installed"
        else
            echo "  fswatch: NOT INSTALLED (brew install fswatch)"
        fi

        if command -v pandoc &> /dev/null; then
            echo "  pandoc: installed"
        else
            echo "  pandoc: NOT INSTALLED (brew install pandoc)"
        fi
        ;;

    help|*)
        echo "PopTop Automation Tools"
        echo ""
        echo "Usage: poptop [command]"
        echo ""
        echo "Commands:"
        echo "  watch       Start file watcher (auto-commit on save)"
        echo "  email       Generate HTML email from today's notes"
        echo "  email DATE  Generate HTML email for specific date"
        echo "  process     Process notes with Claude (extract ARs)"
        echo "  status      Show automation status"
        echo "  help        Show this help"
        echo ""
        echo "Examples:"
        echo "  poptop watch"
        echo "  poptop email 2026-02-06"
        echo "  poptop status"
        ;;
esac
