# PopTop Project Checkpoint

**Last Updated:** February 5, 2026 (11:30 AM)
**Session Context:** Post-call updates. Added Action Items tracking system, meeting notes email automation, AR tab for Google Sheet. Thursday call completed.

---

## Current Goal

Launch PopTop (premium beverage dispenser for collegiate tailgating) before the **2026 College Football season** (target: September 1, 2026).

**Immediate focus:** Execute Thursday Feb 6 reboot call, get team re-committed, authorize trademark filing ($1,300), establish Wednesday standing calls.

---

## Completed This Session (Feb 4-5, 2026)

### Infrastructure Setup
- **Git initialized** -- Local repo created, initial commit with all project files
- **GitHub repo** -- Pushed to https://github.com/paulygrizzo/poptop (private)
- **SSH key** -- Created `~/.ssh/paulygrizzo_github` for paulygrizzo account (separate from paulgiarrizzofortis)
- **Google Drive Desktop** -- Installed, streaming mode (files stay in cloud, don't fill local disk)
- **Poptop folder moved to Google Drive** -- Now syncs to cloud automatically
- **Symlink created** -- `/Users/paulgiarrizzo/Projects/poptop` → Google Drive location (both paths work)
- **Obsidian installed** -- For viewing/editing .md files with Live Preview mode

### Documents Updated
- **Execution Plan v2.1** -- Updated trademark section with Jeff Johnson's actual findings, changed standing call to Wednesdays, updated risk register
- **PDF renamed** to `PopTop-Execution-Plan-v2.1.pdf`
- **Thursday Agenda** -- Added Section 5 for trademark decision ($1,300), updated action items
- **Team roster** -- Replaced Nathan Childress with Whitney Sanchez (Alex's sister) in all files

### New Files Created
- **`dashboard/expanded-tasks-v2.tsv`** -- 71 new detailed tasks covering:
  - Landing page / coming soon site (8 tasks)
  - Business formation & admin (12 tasks)
  - ERP / QuickBooks setup (6 tasks)
  - E-commerce / Shopify (20 tasks)
  - Marketing / content (15 tasks)
  - Distributor channel (8 tasks)
  - Customer service (2 tasks)
- **`dashboard/initial-meetings-data.tsv`** -- Meetings tab data (Feb 6 call + weekly placeholders)
- **`dashboard/initial-decisions-data.tsv`** -- Decisions tab data (10 key decisions made to date)

### Jeff Johnson Trademark Summary (from email thread)
- **Apr 2025:** Professional trademark search completed
- **Finding:** "Pop Top" (Class 21) and "Top Pop" (Class 32) found, but **neither is a showstopper**
- **Recommendation:** Proceed with filing
- **Cost:** $1,300 (1 class), $350/class extra if needed
- **Status:** Jeff's firm waiting for authorization since June 18, 2025 (~8 months)
- **Action:** Team decision needed on Feb 6 call

### Completed Feb 5, 2026 (This Session)
- **Action Items system** -- Added AR tracking to meeting notes with numbered items (AR-001, etc.)
- **Action Items tab data** -- Created `dashboard/initial-action-items-data.tsv` for Google Sheet
- **Apps Script updated** -- Added Action Items tab support, meeting notes email function
- **Meeting notes updated** -- Added AR table to top, extracted 8 action items from call
- **Email draft created** -- `10-Team-Docs/meeting-notes/2026-02-06-email-draft.md`
- **Meeting automation docs** -- `dashboard/docs/meeting-automation-setup.md`
- **Processing script** -- `scripts/process-meeting-notes.sh` for future automation
- **Whitney added** -- Email: whitneychristine89@gmail.com

---

## In Progress / Paused

### Paul's Pre-Call Tasks
- [ ] Send team email with v2.1 PDF + Thursday agenda (invite already sent)
- [ ] Copy updated Apps Script into Google Sheet and run `updateDashboard()`
- [ ] Paste Meetings tab data into Google Sheet
- [ ] Paste Decisions tab data into Google Sheet
- [ ] Expanded tasks already pasted (assigned to Whitney for now)
- [ ] Contact Ross Munn separately by Feb 8

### Pending Automation (Tomorrow/Friday)
- [ ] **Level 2: GitHub → Google Sheets auto-sync** -- Changes pushed to GitHub auto-update the Sheet
- [ ] **Meeting recorder integration** -- Free tool to record call → transcribe → auto-update .md notes → update Sheet → email minutes to team
- [ ] **Auto-detect saved notes** -- Trigger processing without Paul prompting "I finished notes"
- [ ] **Apps Script Dashboard tab** -- Copy `dashboard/apps-script/Code.gs` into Google Sheet

---

## Next Steps

### Before Thursday Call (Feb 6)
- [ ] Send team email with v2.1 PDF + agenda
- [ ] Paste Meetings and Decisions data into Google Sheet
- [ ] Run `updateDashboard()` in Google Sheet Apps Script

### Thursday Call (Feb 6) -- Key Decisions Needed
1. **Team commitment** -- Is everyone still in, same roles?
2. **Timeline** -- Fall 2026 (Sep 1) target agreed?
3. **Capital** -- Can we fund initial phases ($4-10K near-term)?
4. **Brian's agreement** -- Signed or path to signing?
5. **Trademark** -- Authorize Jeff Johnson to file ($1,300)?
6. **Standing call day** -- Move to Wednesdays starting Feb 11?
7. **Communication** -- Group text, Slack, or Discord?

### After Thursday
- [ ] Email Jeff Johnson: "Go ahead and file" (if authorized)
- [ ] Share Google Sheets Command Center with team (Editor access)
- [ ] Set up Level 2 automation (GitHub → Sheets sync)
- [ ] Set up meeting recorder workflow
- [ ] Contact Ross Munn with update
- [ ] Begin CLC licensing research

---

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Project folder name | `poptop` (lowercase) | Per user preference |
| Dashboard platform | Google Sheets + Apps Script | 100% free, collaborative, automation capable |
| RTM target | **Sep 1, 2026 (Fall 2026)** | Before College Football season |
| Standing call | **Wednesdays** (kickoff Thu Feb 6) | Recurring cadence for execution |
| Trademark approach | **Jeff Johnson recommends proceeding** | Professional search found no showstoppers. $1,300 to file. |
| Domain strategy | drinkpoptop.com or getpoptop.com | poptop.com too expensive |
| Team change | **Whitney Sanchez replaces Nathan** | Nathan unavailable; Whitney is Alex's sister |
| Version control | **GitHub (paulygrizzo/poptop)** | Private repo, SSH key configured |
| File sync | **Google Drive Desktop (streaming mode)** | Cloud backup without filling local disk |
| Markdown editor | **Obsidian** | Live Preview mode, beautiful UI |

---

## Team Roster

| Name | Role | Primary Focus | Status |
|------|------|---------------|--------|
| Paul Giarrizzo | Business Lead | Execution driver, licensing, GTM | Active |
| Alex Munn | Co-Founder | Strategic decisions, capital | Active |
| Ross Munn | Co-Founder | Manufacturing, suppliers | TBD (needs outreach) |
| Brian Williams | Engineer | SolidWorks CAD, prototyping, 3D printing | TBD (Thursday call) |
| Whitney Sanchez | Operations | Task support, social media | New (Alex's sister) |

---

## Key Dates

- **Kickoff Call:** February 6, 2026 (Thursday) -- TOMORROW
- **Recurring Standing Call:** Wednesdays starting February 11, 2026
- **Design Freeze Target:** April 24, 2026
- **CLC Submission Target:** May 1, 2026
- **Public Launch Target:** September 1, 2026

---

## Relevant Files

### Project Location
```
ACTUAL:   /Users/paulgiarrizzo/Library/CloudStorage/GoogleDrive-paul.giarrizzo@gmail.com/My Drive/poptop
SYMLINK:  /Users/paulgiarrizzo/Projects/poptop  (points to above)
GITHUB:   https://github.com/paulygrizzo/poptop (private)
```

### Key Documents
```
10-Team-Docs/PopTop-Execution-Plan-v2.1.pdf                <- Share with team
10-Team-Docs/PopTop-Execution-Plan-v2.md                   <- Source of truth
10-Team-Docs/meeting-notes/2026-02-06-thursday-standup-agenda.md  <- Tomorrow's agenda
01-Business-Plan/final/PopTop-Business-Plan-v1.pdf         <- For investors
```

### Dashboard Data (paste into Google Sheet)
```
dashboard/expanded-tasks-v2.tsv            <- 71 new tasks (ALREADY PASTED by Paul)
dashboard/initial-meetings-data.tsv        <- Meetings tab data (NEEDS PASTE)
dashboard/initial-decisions-data.tsv       <- Decisions tab data (NEEDS PASTE)
dashboard/initial-action-items-data.tsv    <- Action Items tab (NEEDS PASTE - 8 ARs)
dashboard/apps-script/Code.gs              <- Updated with AR support + email (NEEDS COPY TO SHEET)
```

### SSH Key (for GitHub pushes)
```
~/.ssh/paulygrizzo_github               <- Private key
~/.ssh/paulygrizzo_github.pub           <- Public key (added to github.com/paulygrizzo)
~/.ssh/config                           <- Has Host github-paulygrizzo entry
```

---

## Google Sheet

**URL:** https://docs.google.com/spreadsheets/d/1JJjYJitZ_jg7ui0JqdID7MtuhGamyZxS1wNbDVw0cp4/

**Tab Status:**
| Tab | Status |
|-----|--------|
| Tasks | Populated (87 original + 71 expanded = 158 tasks) |
| Phases | Populated |
| Team | Whitney added (whitneychristine89@gmail.com), Nathan removed |
| Meetings | EMPTY -- paste `initial-meetings-data.tsv` |
| Decisions | EMPTY -- paste `initial-decisions-data.tsv` |
| Action Items | NEW -- paste `initial-action-items-data.tsv` (8 ARs from Feb 6 call) |
| Risks | Populated |
| Config | Populated |
| Dashboard | EMPTY -- run `updateDashboard()` after updating Apps Script |

---

## Trademark Situation (READY TO FILE)

**Jeff Johnson (IP Law USA)** completed professional search April 2025. Recommends proceeding.

**Filing cost:** $1,300 (1 class)

**Status:** Waiting for authorization since June 2025. **Decision needed Feb 6 call.**

**Contacts:**
- Jeff Johnson -- jjohnson@iplawusa.com
- Steven Adams -- sadams@iplawusa.com
- Firm: SOW, 18 E. University Drive, Suite 101, Mesa, AZ 85201

---

## Pending Automation (Tomorrow/Friday)

1. **GitHub → Google Sheets sync** -- Push changes, Sheet auto-updates
2. **Meeting recorder** -- Record call → transcribe → update .md → update Sheet → email team
3. **Auto-detect saved notes** -- No manual "I'm done" prompt needed
4. **Obsidian + Git hooks** -- Auto-commit/push on save (optional)

---

## Notes

- Brian's Product Development & Royalty Agreement still UNSIGNED (5% royalty, $175K cap or 5-year term)
- Ross Munn not on Thursday call -- needs separate update by Feb 8
- Paul uses Obsidian for .md files (Live Preview mode) -- auto-saves
- poptop folder syncs via Google Drive (streaming mode -- doesn't fill local disk)
- Git remote uses SSH via `github-paulygrizzo` host alias
