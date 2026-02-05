# PopTop Meeting Recording & Automation Setup

## Overview

This document outlines how to automatically:
1. Record and transcribe meetings
2. Extract action items from transcripts
3. Update meeting notes (.md files)
4. Sync to Google Sheets Action Items tab
5. Email meeting notes to the team

---

## Recommended Stack (Free)

### Option A: Otter.ai + Manual Workflow (Simplest)
- **Recording/Transcription:** Otter.ai (free: 300 min/month, 3 imports)
- **Notes Processing:** Manual copy/paste transcript → Claude → update .md
- **Email:** Google Sheet Apps Script (already built)

### Option B: Fathom + Zapier (Semi-Automated)
- **Recording/Transcription:** Fathom (unlimited free for Zoom/Meet)
- **Automation:** Zapier free tier (100 tasks/month)
- **Email:** Apps Script

### Option C: Full Automation (Recommended for Scale)
- **Recording:** Google Meet or Zoom native recording
- **Transcription:** AssemblyAI or Whisper (local)
- **Processing:** Claude API for action item extraction
- **Automation:** n8n (self-hosted, free) or GitHub Actions

---

## Setup Instructions

### Step 1: Choose Your Recording Tool

#### Otter.ai (Recommended for Starting Out)
1. Sign up at https://otter.ai (free tier)
2. Connect to Google Calendar
3. Otter will auto-join and record scheduled meetings
4. Access transcripts at https://otter.ai/my-notes

#### Fathom (Best for Zoom/Meet)
1. Sign up at https://fathom.video
2. Install Chrome extension
3. Grant calendar access
4. Fathom auto-joins and records

### Step 2: After Each Meeting

**Current Manual Workflow:**
1. Get transcript from recording tool
2. Open meeting notes .md file in Obsidian
3. Paste/summarize key points
4. Highlight action items with `==Owner==` notation
5. Save file (auto-syncs to Google Drive)
6. Run Claude to extract ARs and update AR table
7. Push to GitHub
8. Paste ARs into Google Sheet "Action Items" tab
9. Use Apps Script "Send Meeting Notes" to email team

---

## Automation Scripts

### Local Script: Process Transcript and Update Notes

Create a script that can:
1. Take a transcript file as input
2. Use Claude API to extract action items
3. Update the meeting notes .md file
4. Push to GitHub

**Prerequisites:**
- Node.js installed
- Anthropic API key (set in environment)

```bash
# Install dependencies
npm install @anthropic-ai/sdk

# Run the processor
node scripts/process-meeting.js <transcript-file> <meeting-date>
```

### GitHub Action: Auto-Process on Push

When meeting notes are updated, automatically:
1. Extract any new action items
2. Update the Google Sheet via API

---

## Google Sheet Integration

### New Tab: Action Items

Already created `initial-action-items-data.tsv` with columns:
- AR# (e.g., AR-001)
- Meeting Date
- Owner
- Action
- Due
- Status (Open/Complete/Closed)
- Completed Date
- Notes

### Apps Script Functions (Already Added)

- `getActionItemsData()` - Read action items from sheet
- `getOpenActionItemsForOwner()` - Get open items by owner
- `sendMeetingNotesEmail()` - Email notes with AR table
- `showOpenActionItems()` - Display summary dialog

### Menu Items Added

- PopTop > Send Meeting Notes
- PopTop > Review Open Action Items

---

## Quick Reference: Post-Meeting Workflow

1. **During meeting:** Otter/Fathom auto-records
2. **After meeting:**
   - Open transcript in recording tool
   - Copy key points to Obsidian (.md file)
   - Add `==Name==` highlights for action items
   - Save (auto-syncs to Google Drive)
3. **Run automation:**
   ```bash
   cd ~/Projects/poptop
   # Claude extracts ARs, updates table, commits
   claude "Process meeting notes for today, extract ARs"
   ```
4. **Update Google Sheet:**
   - Paste `initial-action-items-data.tsv` into Action Items tab
   - OR manually add new ARs
5. **Email team:**
   - In Google Sheet: PopTop > Send Meeting Notes

---

## Future Enhancements

### Level 2: Watch for File Changes
- Use `fswatch` or `chokidar` to detect .md file saves
- Auto-trigger Claude processing
- Auto-push to GitHub

### Level 3: Webhook Integration
- Otter/Fathom webhook → n8n workflow
- Transcript auto-pulled → Claude API → .md updated → Git push → Sheet sync

### Level 4: Voice Commands
- "Hey Claude, process today's meeting notes"
- Triggered via iOS Shortcut or terminal alias

---

## Costs

| Tool | Free Tier | Paid |
|------|-----------|------|
| Otter.ai | 300 min/month | $17/mo Pro |
| Fathom | Unlimited | $19/mo Premium |
| Zapier | 100 tasks/month | $20/mo |
| n8n | Self-hosted free | Cloud $20/mo |
| Claude API | N/A | ~$0.01/meeting |

**Recommendation:** Start with Otter.ai free + manual workflow. Upgrade to automation when meeting frequency increases.

---

## Team Email Templates

### Whitney's Email
- whitneychristine89@gmail.com

### Full Team Distribution
Already configured in Google Sheet Team tab with emails.

---

*Last Updated: February 5, 2026*
