# PopTop Project Checkpoint

**Last Updated:** February 4, 2026
**Session Context:** Call prep session. Updated execution plan + agenda with Jeff Johnson trademark findings, built Dashboard tab function, regenerated PDF.

---

## Current Goal

Launch PopTop (premium beverage dispenser for collegiate tailgating) before the **2026 College Football season** (target: September 1, 2026). Immediate focus: execute Thursday Feb 6 reboot call, get team re-committed, authorize trademark filing, move to Wednesday standing calls.

---

## Completed This Session (Feb 4, 2026)

### Updates Made
- **Execution Plan v2.1** -- Updated trademark section with Jeff Johnson's actual attorney findings (he recommends proceeding, $1,300 to file). Updated standing call day to Wednesday (with Thursday Feb 6 kickoff). Updated risk register. Regenerated PDF.
- **Thursday Agenda** (`10-Team-Docs/meeting-notes/2026-02-06-thursday-standup-agenda.md`) -- Added trademark update section (Jeff Johnson's findings + $1,300 filing decision). Updated action items. Added Section 5 for trademark decision. Updated standing call logistics to propose Wednesday recurring.
- **Dashboard function** -- Wrote `updateDashboard()` in Apps Script (`dashboard/apps-script/Code.gs`). Auto-populates the blank Dashboard tab with live data: quick stats, phase progress bars, overdue tasks, team workload, milestones. Added to PopTop menu. Auto-refreshes on task edits.
- **PDF regenerated** (`10-Team-Docs/PopTop-Execution-Plan-v2.pdf`) -- Matches updated markdown.

### Jeff Johnson Trademark Thread (Summarized from Emails)
- **Apr 17-22, 2025:** Engaged Jeff Johnson (IP Law USA, Mesa AZ). Told him product is beverage dispensers -- canned/bottled first, then liquid/carbonated.
- **Apr 28, 2025:** Jeff delivered search results. Found "Pop Top" (Class 21, water bottles) and "Top Pop" (Class 32, soft drinks). **His assessment: neither is a showstopper. Recommends proceeding.** Filing cost: $1,300 (1 class), $350/class extra if needed.
- **Apr 30 & May 29, 2025:** Jeff followed up twice asking for authorization.
- **Jun 13, 2025:** Paul replied -- said he wanted to proceed, promised answer by Monday/Tuesday.
- **Jun 18, 2025:** Jeff acknowledged, said "sit tight until you give the green light."
- **Current status:** Jeff's firm is **waiting for authorization to file. ~8 months waiting.** Decision needed on Feb 6 call.

---

## In Progress / Paused

- **Team email send** -- Paul needs to send v2.1 PDF + agenda to Alex, Brian, Nathan before Thursday call.
- **Calendar invite** -- Paul needs to send Thursday Feb 6 invite with video link, then set up recurring Wednesday starting Feb 11.
- **Ross Munn outreach** -- Not on Thursday call. Paul needs to contact separately by Feb 8.
- **Dashboard deployment** -- `updateDashboard()` function written in local Code.gs file. Paul needs to copy updated Apps Script into the Google Sheet (Extensions > Apps Script > replace code > save > run `updateDashboard` once).

---

## Next Steps

### Before Thursday (Feb 6)
- [ ] **Paul:** Send team email with v2.1 PDF + Thursday agenda
- [ ] **Paul:** Send Thursday calendar invite with video link
- [ ] **Paul:** Copy updated Apps Script into Google Sheet and run `updateDashboard()`

### Thursday Call (Feb 6) -- Key Decisions
1. **Team commitment** -- Is everyone still in, same roles?
2. **Timeline** -- Fall 2026 (Sep 1) target agreed?
3. **Capital** -- Can we fund initial phases ($4-10K near-term)?
4. **Brian's agreement** -- Signed or path to signing?
5. **Trademark** -- Authorize Jeff Johnson to file ($1,300)? Attorney recommends proceeding.
6. **Standing call day** -- Move to Wednesdays starting Feb 11?
7. **Communication** -- How do we stay in touch between calls?

### After Thursday
- [ ] Email Jeff Johnson: "Go ahead and file" (if authorized on call)
- [ ] Share Google Sheets Command Center with team (Editor access)
- [ ] Send user guide (`dashboard/docs/user-guide.md`)
- [ ] Contact Ross Munn separately with update
- [ ] Begin CLC licensing research (Phase 4)
- [ ] Brian: review existing CAD files, confirm design freeze timeline
- [ ] Alex: register domain (drinkpoptop.com or getpoptop.com)
- [ ] Nathan: social media handles + communication channel setup

---

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Project folder name | `poptop` (lowercase) | Per user preference |
| Dashboard platform | Google Sheets + Apps Script | 100% free, collaborative, automation capable |
| TAM figure | $500M+ | Validated vs YETI comparable |
| GTM strategy | Licensing-First | CLC/Fanatics approach |
| **RTM target** | **Sep 1, 2026 (Fall 2026)** | Before College Football season |
| **Standing call** | **Wednesdays (kickoff: Thursday Feb 6)** | Recurring cadence for execution |
| **Execution Plan version** | **v2.1** | Aggressive 7-month reset, all 2026 dates |
| **Trademark approach** | **Jeff Johnson recommends proceeding** | Professional search found no showstoppers. $1,300 to file. Awaiting team authorization. |
| **Domain strategy** | **drinkpoptop.com or getpoptop.com** | poptop.com too expensive (Sedo premium) |

---

## Team Roster

| Name | Role | Primary Focus | Status |
|------|------|---------------|--------|
| Paul Giarrizzo | Business Lead | Execution driver, licensing, GTM | Active |
| Alex Munn | Co-Founder | Strategic decisions, capital | Active |
| Ross Munn | Co-Founder | Manufacturing, suppliers | TBD (needs outreach before call) |
| Brian Williams | Engineer | SolidWorks CAD, prototyping, 3D printing | TBD (Thursday call) |
| Nathan Childress | Operations | Task support, social media | TBD (Thursday call) |

---

## Key Dates

- **Kickoff Call:** February 6, 2026 (Thursday)
- **Recurring Standing Call:** Wednesdays starting February 11, 2026
- **Design Freeze Target:** April 24, 2026
- **CLC Submission Target:** May 1, 2026
- **Public Launch Target:** September 1, 2026

---

## Relevant Files

### Key Documents (Share with Team)
```
01-Business-Plan/final/PopTop-Business-Plan-v1.pdf         <- For investors & team
10-Team-Docs/PopTop-Execution-Plan-v2.pdf                   <- CURRENT -- share this one
10-Team-Docs/PopTop-Execution-Plan-v2.md                    <- Text version (source of truth)
10-Team-Docs/meeting-notes/2026-02-06-thursday-standup-agenda.md  <- Thursday call agenda
```

### Legal/IP
```
02-Legal-IP/trademark-domain-research-2025-02-03.md         <- Internal trademark + domain research
```

### Dashboard (DEPLOYED)
```
dashboard/initial-task-data.tsv          <- 94 tasks (in Google Sheet)
dashboard/initial-phases-data.tsv        <- 7 phases
dashboard/initial-risks-data.tsv         <- 8 risks
dashboard/initial-config-data.tsv        <- Config settings
dashboard/apps-script/Code.gs            <- Automation code (UPDATED -- includes updateDashboard())
dashboard/sheets-template.md             <- Template reference
dashboard/docs/user-guide.md             <- For team members
dashboard/docs/automation-guide.md       <- Setup instructions
```

### PDF Generators
```
10-Team-Docs/generate_execution_pdf_v2.py       <- v2.1 PDF generator (UPDATED)
```

### CAD Files (Brian's Work)
```
~/Desktop/Pop Top Drawings/CenterMag_With_Cradle.SLDASM
~/Desktop/Pop Top Drawings/PopTop_Can_Holder.STEP
~/Desktop/Pop Top Drawings/PopTop_Container_Top.STEP
~/Desktop/Pop Top Drawings/PopTop_Lid.STEP
~/Desktop/Pop Top Drawings/PopTop_Tube.STEP
~/Desktop/Pop Top Drawings/PopTop_CenterMag.STL
~/Desktop/Pop Top Drawings/PopTop_Curved_Part.STL
```

---

## Trademark Situation (READY TO FILE)

**Jeff Johnson (IP Law USA)** completed a professional federal trademark search in April 2025. Found two potentially relevant marks but **recommends proceeding** -- neither is a showstopper for beverage dispensers.

**Filing cost:** $1,300 (1 class). $350/class extra if USPTO requires additional classes.

**Current status:** Jeff's firm has been waiting for authorization since June 18, 2025. Paul indicated intent to proceed but never gave final green light. **Team decision needed on Feb 6 call.**

**Key contacts:**
- Jeff Johnson, Partner -- jjohnson@iplawusa.com
- Steven Adams -- sadams@iplawusa.com
- Firm: SOW, 18 E. University Drive, Suite 101, Mesa, AZ 85201

---

## Notes

- Brian has a Product Development & Royalty Agreement pending (5% royalty, Option A: 5-year term OR Option B: $175K cap) -- UNSIGNED
- Google Sheet Command Center: [Link](https://docs.google.com/spreadsheets/d/1JJjYJitZ_jg7ui0JqdID7MtuhGamyZxS1wNbDVw0cp4/)
- Dashboard tab was blank -- `updateDashboard()` function now written in Code.gs. Paul needs to update the Apps Script in the Sheet and run it once.
- Ross Munn not on Thursday call -- needs separate update by Feb 8
- v1 execution plan and business plan are still valid reference docs but v2.1 execution plan is the current source of truth
