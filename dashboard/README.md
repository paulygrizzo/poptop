# PopTop Project Dashboard

## System Architecture

This dashboard system uses **100% free tools** to provide professional project management capabilities:

```
┌─────────────────────────────────────────────────────────────────┐
│                     POPTOP COMMAND CENTER                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │   GOOGLE     │    │   GOOGLE     │    │    MIRO      │       │
│  │   SHEETS     │◄──►│   DRIVE      │◄──►│  (Visual)    │       │
│  │  (Dashboard) │    │  (Files)     │    │              │       │
│  └──────┬───────┘    └──────────────┘    └──────────────┘       │
│         │                                                        │
│         │ Apps Script                                            │
│         ▼                                                        │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │   EMAIL      │    │   GITHUB     │    │    NEON      │       │
│  │ AUTOMATION   │    │   (Code)     │    │  (Database)  │       │
│  │              │    │              │    │  [Optional]  │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Components

### 1. Google Sheets Dashboard (Primary Hub)
- **Master Task Tracker** - All tasks, owners, statuses, dates
- **Phase Overview** - Visual phase progress
- **Team Workload** - Who's doing what
- **Timeline View** - Gantt-style view
- **Metrics Dashboard** - KPIs and progress

### 2. Google Apps Script (Automation Engine)
- Daily status email digest
- Overdue task alerts
- Weekly progress reports
- Auto-status updates
- Slack/email notifications

### 3. Google Drive (File Management)
- Organized folder structure
- Design files, documents, contracts
- Version control for non-code assets

### 4. GitHub (Optional - Code/Scripts)
- Apps Script version control
- Any future web components
- Issue tracking for technical items

### 5. Neon PostgreSQL (Optional - Future)
- Structured data storage if needed
- API-accessible database
- Free tier: 512MB storage

### 6. Miro (Visual Collaboration)
- Brainstorming
- Product design ideation
- Process mapping

---

## Setup Instructions

### Step 1: Create Google Sheet Dashboard

1. Go to [Google Sheets](https://sheets.google.com)
2. Create new spreadsheet named "PopTop Command Center"
3. Create the following sheets (tabs):
   - `Dashboard` (overview)
   - `Tasks` (master task list)
   - `Phases` (phase tracking)
   - `Team` (team members)
   - `Meetings` (meeting notes)
   - `Decisions` (decision log)
   - `Risks` (risk register)
   - `Config` (settings)

### Step 2: Set Up Sheet Structure

See `sheets-template.md` for detailed column structures.

### Step 3: Add Apps Script Automation

1. In your Google Sheet: Extensions → Apps Script
2. Copy code from `apps-script/` folder
3. Set up triggers (see automation guide)

### Step 4: Share with Team

1. Click Share button
2. Add team members:
   - paul.giarrizzo@[email] - Editor
   - alex.munn@[email] - Editor
   - ross.munn@[email] - Editor
   - brian.williams@[email] - Editor
   - nathan.childress@[email] - Editor

---

## File Structure

```
dashboard/
├── README.md                    # This file
├── sheets-template.md           # Google Sheets structure guide
├── apps-script/
│   ├── Code.gs                  # Main Apps Script code
│   ├── Triggers.gs              # Automation triggers
│   ├── Email.gs                 # Email functions
│   └── Utils.gs                 # Utility functions
└── docs/
    ├── automation-guide.md      # How automation works
    └── user-guide.md            # How to use the dashboard
```

---

## Quick Start

1. **Copy the template** (link will be provided after setup)
2. **Add your team** as editors
3. **Enable automation** in Apps Script
4. **Start tracking tasks** in the Tasks sheet

---

## Support

Questions? Contact Paul Giarrizzo
