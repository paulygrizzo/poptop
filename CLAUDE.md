# PopTop Project Checkpoint

**Last Updated:** February 5, 2026 (4:30 PM)
**Session Context:** Automation setup complete. Apps Script deployed, triggers active, CLI tools working. Thursday call done, meeting notes sent to team.

---

## Current Goal

Launch PopTop (premium beverage dispenser for collegiate tailgating) before the **2026 College Football season** (target: September 1, 2026).

**Immediate focus:** Complete automation testing (Fathom for recording, `poptop watch` for auto-commits), then focus on Brian's prototype delivery (WW06.2) and Alex's trademark authorization.

---

## Completed This Session (Feb 5, 2026 Afternoon)

### Automation Infrastructure - FULLY SET UP
- **`poptop` CLI command** -- Added alias to `.zshrc`, launcher at `scripts/poptop-tools.sh`
- **`poptop status`** -- Shows automation health, git status, dependencies
- **`poptop email [date]`** -- Generates beautiful HTML email from meeting notes (uses Python markdown)
- **`poptop watch`** -- File watcher that auto-commits when you save in Obsidian
- **fswatch installed** -- macOS file watching tool (via brew)
- **Python markdown** -- Using instead of pandoc (simpler, already installed)

### Apps Script - DEPLOYED & ACTIVE
- **Web App deployed** -- URL: `https://script.google.com/macros/s/AKfycbzWD42frFfsTheIbAbJRrk6H_PB_lsyzB-M5u8jUutArE_M566xpR-qb9SC1Js08R8f/exec`
- **PopTop menu** -- Shows in Google Sheet (Refresh Dashboard, Send Meeting Notes, Review Open ARs)
- **Triggers set up** -- Auto-refresh on edit, daily digest (Mon/Wed 8am), overdue alerts (9am daily), weekly summary (Mon 9am)
- **Email preferences** -- Added column F to Team tab; Ross set to "meeting-notes-only"

### Meeting Notes & Email
- **Action Items table** -- Added to top of Thursday meeting agenda
- **8 ARs extracted** -- AR-001 through AR-008 with owners, due dates, status
- **Email sent to team** -- Used `poptop email` to generate HTML, copy/pasted to Gmail
- **Ross added** -- MunnRoss3@gmail.com (meeting notes only)
- **Whitney confirmed** -- whitneychristine89@gmail.com

### Files Created/Modified
- `scripts/poptop-tools.sh` -- Main CLI launcher
- `scripts/watch-meeting-notes.sh` -- File watcher for auto-commit
- `scripts/generate-email-html.sh` -- Markdown to HTML converter
- `scripts/process-meeting-notes.sh` -- Claude processing helper
- `.github/workflows/sync-to-sheets.yml` -- GitHub Action (webhook disabled due to Google limitation)
- `dashboard/apps-script/Code.gs` -- Full automation suite with email prefs support
- `~/.zshrc` -- Added `poptop` alias and `POPTOP_DIR` env var

---

## In Progress / Paused

### To Test
- [ ] **Fathom signup** -- fathom.video for meeting recording (free, unlimited)
- [ ] **`poptop watch`** -- Test auto-commit when saving in Obsidian

### Action Items from Thursday Call (Open)
| AR# | Owner | Action | Due |
|-----|-------|--------|-----|
| AR-001 | Whitney | Reach out for follow-up call w/ Alex & Paul | WW06 (Feb 10-14) |
| AR-002 | Brian | Have 1st prototype pieces ready | WW06.2 (Feb 10) |
| AR-003 | Brian | Drop CAD files into Engineering folder | WW06.2 |
| AR-005 | Alex | Authorize Jeff Johnson trademark filing ($1,300) | WW06.5 |
| AR-007 | Alex | Confirm capital commitment for Phase 1-2 | Feb 13 |
| AR-008 | Alex | Register domain (drinkpoptop.com or getpoptop.com) | Feb 13 |

**Completed ARs:** AR-004 (calendar invite), AR-006 (share Command Center)

---

## Next Steps

### Immediate (This Week)
1. [ ] Sign up for Fathom at fathom.video
2. [ ] Test `poptop watch` in a terminal while editing Obsidian
3. [ ] Follow up with Brian on prototype (due WW06.2 = Feb 10)
4. [ ] Follow up with Alex on trademark authorization

### Next Thursday Call (Feb 13)
- Review AR status
- Brian prototype progress
- Trademark filing status
- Domain registration status

---

## Key Decisions (This Session)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Markdown converter | **Python markdown** (not pandoc) | Simpler dependency, already installed |
| GitHub → Sheets sync | **Skip webhook, use triggers** | Google Apps Script POST redirect limitation |
| Standing call day | **Thursdays at 12:15pm EST** | Changed from Wednesdays per team preference |
| Ross email preference | **meeting-notes-only** | He only wants weekly meeting notes, not daily digests |
| Email generation | **`poptop email` → HTML → copy to Gmail** | Beautiful formatting, works reliably |

---

## Automation Summary

### Working Commands
```bash
poptop status              # Check automation health
poptop email               # Generate HTML email for today
poptop email 2026-02-06    # Generate for specific date
poptop watch               # Start file watcher (auto-commit on save)
```

### Google Sheet Automation (Active)
- **PopTop menu** -- Manual triggers for dashboard, emails, AR review
- **Auto-refresh** -- Dashboard updates when any cell is edited
- **Daily digest** -- Mon & Wed at 8am to team (except Ross)
- **Overdue alerts** -- Daily at 9am to task owners (except Ross)
- **Weekly summary** -- Monday at 9am to team (except Ross)

### Email Recipients
| Name | Email | Preference |
|------|-------|------------|
| Paul | (in Sheet) | all |
| Alex | (in Sheet) | all |
| Brian | (in Sheet) | all |
| Whitney | whitneychristine89@gmail.com | all |
| Ross | MunnRoss3@gmail.com | meeting-notes-only |

---

## Team Roster

| Name | Role | Primary Focus | Status |
|------|------|---------------|--------|
| Paul Giarrizzo | Business Lead | Execution driver, licensing, GTM | Active |
| Alex Munn | Co-Founder | Strategic decisions, capital | Active |
| Ross Munn | Co-Founder | Manufacturing, suppliers | Active (meeting notes only) |
| Brian Williams | Engineer | SolidWorks CAD, prototyping, 3D printing | Active |
| Whitney Sanchez | Operations | Task support, social media | Active |

---

## Key Dates

- **Thursday Call Completed:** February 6, 2026
- **Next Standing Call:** Thursday, February 13, 2026 at 12:15pm EST
- **Brian Prototype Due:** WW06.2 (Feb 10, 2026)
- **Design Freeze Target:** April 24, 2026
- **CLC Submission Target:** May 1, 2026
- **Public Launch Target:** September 1, 2026

---

## Relevant Files

### Automation Scripts
```
scripts/poptop-tools.sh           <- Main CLI launcher (aliased as 'poptop')
scripts/watch-meeting-notes.sh    <- File watcher for auto-commit
scripts/generate-email-html.sh    <- Markdown → HTML email generator
scripts/process-meeting-notes.sh  <- Claude processing helper
.github/workflows/sync-to-sheets.yml  <- GitHub Action (webhook disabled)
```

### Meeting Notes
```
10-Team-Docs/meeting-notes/2026-02-06-thursday-standup-agenda.md  <- Call notes with ARs
10-Team-Docs/meeting-notes/2026-02-06-email-draft.md              <- Email template
```

### Apps Script
```
dashboard/apps-script/Code.gs     <- Full automation (1181 lines)
```
**Deployed at:** https://script.google.com/macros/s/AKfycbzWD42frFfsTheIbAbJRrk6H_PB_lsyzB-M5u8jUutArE_M566xpR-qb9SC1Js08R8f/exec

### Project Location
```
ACTUAL:   /Users/paulgiarrizzo/Library/CloudStorage/GoogleDrive-paul.giarrizzo@gmail.com/My Drive/poptop
SYMLINK:  /Users/paulgiarrizzo/Projects/poptop
GITHUB:   https://github.com/paulygrizzo/poptop (private)
```

---

## Google Sheet

**URL:** https://docs.google.com/spreadsheets/d/1JJjYJitZ_jg7ui0JqdID7MtuhGamyZxS1wNbDVw0cp4/

**Tab Status:**
| Tab | Status |
|-----|--------|
| Tasks | Populated |
| Phases | Populated |
| Team | Updated (Whitney added, Email Prefs column F added) |
| Meetings | Needs data paste |
| Decisions | Needs data paste |
| Action Items | Created, needs AR data paste |
| Risks | Populated |
| Config | Populated |
| Dashboard | Working (auto-refreshes) |

---

## Notes

- **GitHub webhook skipped** -- Google Apps Script can't handle POST redirects; using time-based triggers instead
- **Pandoc not installed** -- Using Python markdown module instead (simpler)
- **fswatch installed** -- For file watching (`poptop watch`)
- **Shell alias active** -- `poptop` command works in new terminal windows
- Brian's Product Development & Royalty Agreement still UNSIGNED
- Ross added to meeting notes distribution (MunnRoss3@gmail.com)
