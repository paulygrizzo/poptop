# PopTop Dashboard - Google Sheets Template

## Sheet 1: Dashboard (Overview)

This is the main view everyone sees. It pulls data from other sheets.

```
┌────────────────────────────────────────────────────────────────────┐
│                    POPTOP COMMAND CENTER                            │
│                    Last Updated: [Auto]                             │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  PHASE PROGRESS                          QUICK STATS                │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ━━━━━━━━━━━━━━━━━━━━━━━━━ │
│  Phase 1: Design      ████████░░ 80%    Total Tasks: 47            │
│  Phase 2: Brand       ████░░░░░░ 40%    Completed: 12              │
│  Phase 3: Mfg         ░░░░░░░░░░  0%    In Progress: 8             │
│  Phase 4: Licensing   ██░░░░░░░░ 20%    Blocked: 2                 │
│  Phase 5: GTM         ░░░░░░░░░░  0%    Not Started: 25            │
│  Phase 6: Launch      ░░░░░░░░░░  0%                               │
│                                                                     │
│  OVERDUE TASKS (Action Required!)        THIS WEEK'S FOCUS         │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ━━━━━━━━━━━━━━━━━━━━━━━━━ │
│  • Finalize CAD dims (Brian) - 2d late  • Complete SolidWorks asm  │
│  • Trademark search (Paul) - 1d late    • Schedule team sync       │
│                                          • Begin prototype V1       │
│  TEAM WORKLOAD                                                      │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│  Paul: 12 tasks (5 active)                                         │
│  Brian: 8 tasks (3 active)                                         │
│  Ross: 6 tasks (1 active)                                          │
│  Nathan: 4 tasks (2 active)                                        │
│                                                                     │
│  UPCOMING MILESTONES                                                │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│  Feb 15: Design Freeze (Phase 1 Gate)                              │
│  Mar 1: Trademark Filed                                            │
│  Apr 1: T1 Samples                                                 │
│  May 15: CLC Approval (Target)                                     │
│  Jul 1: RTM Launch                                                 │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

### Dashboard Formulas (Key Cells)

| Cell | Description | Formula |
|------|-------------|---------|
| B3 | Total Tasks | `=COUNTA(Tasks!A:A)-1` |
| B4 | Completed | `=COUNTIF(Tasks!E:E,"Complete")` |
| B5 | In Progress | `=COUNTIF(Tasks!E:E,"In Progress")` |
| B6 | Blocked | `=COUNTIF(Tasks!E:E,"Blocked")` |

---

## Sheet 2: Tasks (Master Task List)

**Column Structure:**

| Column | Header | Width | Type | Notes |
|--------|--------|-------|------|-------|
| A | ID | 50 | Auto | =ROW()-1 |
| B | Phase | 80 | Dropdown | Phase 1-6 |
| C | Task Name | 300 | Text | Description of task |
| D | Owner | 100 | Dropdown | Team member |
| E | Status | 100 | Dropdown | Not Started/In Progress/Complete/Blocked |
| F | Priority | 80 | Dropdown | High/Medium/Low |
| G | Start Date | 100 | Date | When work begins |
| H | Due Date | 100 | Date | Target completion |
| I | Completed | 100 | Date | Actual completion |
| J | Days Left | 80 | Formula | =IF(E2="Complete","Done",H2-TODAY()) |
| K | Blocker | 200 | Text | What's blocking (if any) |
| L | Notes | 300 | Text | Additional context |
| M | Dependencies | 150 | Text | Task IDs this depends on |

**Dropdown Values:**

**Status:**
- Not Started
- In Progress
- Complete
- Blocked
- On Hold

**Priority:**
- High
- Medium
- Low

**Phase:**
- Phase 1: Design
- Phase 2: Brand
- Phase 3: Manufacturing
- Phase 4: Licensing
- Phase 5: GTM
- Phase 6: Launch

**Owner:**
- Paul Giarrizzo
- Brian Williams
- Ross Munn
- Nathan Childress
- Alex Munn
- Team

---

## Sheet 3: Phases (Phase Tracking)

| Column | Header | Description |
|--------|--------|-------------|
| A | Phase | Phase 1-6 |
| B | Name | Design, Brand, etc. |
| C | Owner | Primary owner |
| D | Start Date | Phase start |
| E | Target End | Phase target |
| F | Status | Not Started/In Progress/Complete |
| G | % Complete | =COUNTIF(Tasks!B:B,A2&"*")/COUNTIF... |
| H | Total Tasks | Count from Tasks |
| I | Completed Tasks | Count completed |
| J | Gate Criteria | What defines "done" |
| K | Gate Status | Not Met/Met |

**Initial Data:**

| Phase | Name | Owner | Gate Criteria |
|-------|------|-------|---------------|
| Phase 1 | Design & Prototyping | Brian | Design freeze approved |
| Phase 2 | Brand Identity & IP | Paul | TM filed, logo approved |
| Phase 3 | Manufacturing | Ross | T1 samples approved |
| Phase 4 | Licensing | Paul | CLC + 3 schools |
| Phase 5 | Go-To-Market Prep | Paul | Store live, assets ready |
| Phase 6 | Launch & Operations | Team | Successful launch |

---

## Sheet 4: Team (Team Members)

| Column | Header | Description |
|--------|--------|-------------|
| A | Name | Full name |
| B | Role | Title/role |
| C | Email | For automation |
| D | Phone | Contact |
| E | Primary Area | Main responsibility |
| F | Active Tasks | =COUNTIFS(Tasks!D:D,A2,Tasks!E:E,"In Progress") |
| G | Total Tasks | =COUNTIF(Tasks!D:D,A2) |
| H | Completed | =COUNTIFS(Tasks!D:D,A2,Tasks!E:E,"Complete") |
| I | Completion Rate | =H2/G2 |
| J | Notes | Availability, etc. |

**Initial Data:**

| Name | Role | Primary Area |
|------|------|--------------|
| Paul Giarrizzo | Business Lead | Execution, Licensing, GTM |
| Brian Williams | Engineer | CAD, Prototyping, DFM |
| Ross Munn | Co-Founder | Manufacturing, Supply Chain |
| Nathan Childress | Operations | Task Support, Social |
| Alex Munn | Co-Founder | Strategy, Capital |

---

## Sheet 5: Meetings (Meeting Notes)

| Column | Header | Description |
|--------|--------|-------------|
| A | Date | Meeting date |
| B | Type | Weekly Sync/Ad-hoc/etc. |
| C | Attendees | Who was there |
| D | Agenda | What was discussed |
| E | Decisions | Decisions made |
| F | Action Items | Tasks created |
| G | Notes Link | Link to detailed notes |

---

## Sheet 6: Decisions (Decision Log)

| Column | Header | Description |
|--------|--------|-------------|
| A | ID | Decision ID |
| B | Date | When decided |
| C | Decision | What was decided |
| D | Context | Why/background |
| E | Made By | Who made it |
| F | Impact | What it affects |
| G | Reversible | Yes/No |

---

## Sheet 7: Risks (Risk Register)

| Column | Header | Description |
|--------|--------|-------------|
| A | ID | Risk ID |
| B | Risk | Description |
| C | Probability | High/Medium/Low |
| D | Impact | High/Medium/Low |
| E | Score | =IF(C2="High",3,IF(C2="Medium",2,1))*IF(D2="High",3,IF(D2="Medium",2,1)) |
| F | Mitigation | How we address it |
| G | Owner | Who monitors |
| H | Status | Active/Mitigated/Occurred |

**Initial Risks:**

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Tooling delays | Medium | High | Early kick-off, buffer time |
| CLC approval delays | Medium | High | Early application, multiple schools |
| Manufacturing quality issues | Low | High | T1 validation, QC process |
| Capital constraints | Medium | Medium | Phased approach, pre-orders |
| Design iteration needs | Medium | Medium | Rapid prototyping capability |

---

## Sheet 8: Config (Settings)

| Setting | Value | Notes |
|---------|-------|-------|
| Project Name | PopTop | |
| Target RTM | 2025-07-01 | |
| Weekly Sync Day | Tuesday | |
| Email Digest Time | 8:00 AM | |
| Overdue Alert Days | 2 | Days before alerting |
| Dashboard Refresh | Daily | |

---

## Conditional Formatting Rules

### Tasks Sheet

1. **Overdue Tasks (Red background)**
   - Apply to: E:E (Status column row)
   - Condition: Custom formula `=AND(E2<>"Complete",H2<TODAY())`
   - Format: Red background

2. **Due Soon (Yellow background)**
   - Condition: `=AND(E2<>"Complete",H2-TODAY()<=3,H2>=TODAY())`
   - Format: Yellow background

3. **Completed (Green text, strikethrough)**
   - Condition: `=E2="Complete"`
   - Format: Green text, strikethrough

4. **Blocked (Orange background)**
   - Condition: `=E2="Blocked"`
   - Format: Orange background

5. **High Priority (Bold)**
   - Condition: `=F2="High"`
   - Format: Bold

### Dashboard Sheet

1. **Progress bars using REPT function**
   - `=REPT("█",ROUND(G2*10,0))&REPT("░",10-ROUND(G2*10,0))`

---

## Data Validation Rules

### Tasks!B:B (Phase)
- List from range: Phases!A:A

### Tasks!D:D (Owner)
- List from range: Team!A:A

### Tasks!E:E (Status)
- List of items: Not Started,In Progress,Complete,Blocked,On Hold

### Tasks!F:F (Priority)
- List of items: High,Medium,Low

---

## Named Ranges (Recommended)

| Name | Range | Purpose |
|------|-------|---------|
| AllTasks | Tasks!A:M | Reference all tasks |
| TeamMembers | Team!A:A | Dropdown source |
| PhaseList | Phases!A:A | Dropdown source |
| ConfigSettings | Config!A:B | Settings lookup |
