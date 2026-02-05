# PopTop Automation Framework

## Overview

This guide explains how to set up and manage the automated systems that keep the team coordinated and moving forward.

---

## Automation Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    AUTOMATION FLOW                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   TRIGGERS                    ACTIONS                            │
│   ════════                    ═══════                            │
│                                                                  │
│   ⏰ 8:00 AM Daily ────────► 📧 Daily Digest Email               │
│                               • Stats summary                     │
│                               • Overdue tasks                     │
│                               • Team workload                     │
│                                                                  │
│   ⏰ Every 6 Hours ────────► 🚨 Overdue Alerts                   │
│                               • Personal task alerts              │
│                               • Sent to task owners               │
│                                                                  │
│   ⏰ Monday 9 AM ──────────► 📈 Weekly Summary                   │
│                               • Week's progress                   │
│                               • Completed tasks                   │
│                               • Phase status                      │
│                                                                  │
│   ✏️ Cell Edit ────────────► 📋 Auto-Updates                     │
│                               • Complete date auto-fill           │
│                               • Dashboard refresh                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Setup Instructions

### Step 1: Create the Google Sheet

1. Go to [sheets.google.com](https://sheets.google.com)
2. Create a new spreadsheet
3. Name it: **PopTop Command Center**
4. Create these tabs:
   - Dashboard
   - Tasks
   - Phases
   - Team
   - Meetings
   - Decisions
   - Risks
   - Config

### Step 2: Set Up Sheet Structure

Follow the structure in `sheets-template.md` for each tab.

**Quick setup for Tasks sheet:**

| A | B | C | D | E | F | G | H | I | J | K | L |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ID | Phase | Task Name | Owner | Status | Priority | Start | Due | Completed | Days Left | Blocker | Notes |

### Step 3: Add Team Members

In the **Team** tab, add:

| Name | Role | Email | Phone | Primary Area |
|------|------|-------|-------|--------------|
| Paul Giarrizzo | Business Lead | paul@email.com | | Execution, Licensing |
| Brian Williams | Engineer | brian@email.com | | CAD, Prototyping |
| Ross Munn | Co-Founder | ross@email.com | | Manufacturing |
| Nathan Childress | Operations | nathan@email.com | | Task Support |
| Alex Munn | Co-Founder | alex@email.com | | Strategy |

**Important:** The email column must have valid emails for notifications to work!

### Step 4: Add Apps Script

1. In your Google Sheet, go to **Extensions → Apps Script**
2. Delete any existing code in `Code.gs`
3. Copy the entire contents of `apps-script/Code.gs` from this project
4. Paste into the Apps Script editor
5. Click **Save** (Ctrl+S or Cmd+S)
6. Name the project: "PopTop Automation"

### Step 5: Authorize & Run Setup

1. In Apps Script, find the function dropdown (near the Run button)
2. Select **setupTriggers**
3. Click **Run**
4. A popup will appear - click **Review permissions**
5. Choose your Google account
6. Click **Advanced** → **Go to PopTop Automation (unsafe)**
7. Click **Allow**
8. Wait for confirmation message

### Step 6: Verify Setup

1. Run the **testSetup** function to verify everything
2. You should see all sheets found and triggers active
3. Check that email quota is available

### Step 7: Test Notifications

1. Go back to your spreadsheet
2. Click the **🚀 PopTop** menu (top menu bar)
3. Select **📧 Send Daily Digest Now**
4. Check your email for the digest

---

## Automation Features

### 1. Daily Digest Email

**When:** Every day at 8:00 AM
**Who:** All team members with valid emails
**Contents:**
- Quick stats (total, completed, in progress, overdue)
- List of overdue tasks with owner and days overdue
- Tasks due within 3 days
- Blocked tasks with blockers
- Team workload breakdown

### 2. Overdue Task Alerts

**When:** Every 6 hours
**Who:** Individual task owners
**Contents:**
- Personal notification of YOUR overdue tasks
- List with task names and days overdue
- Link to dashboard

### 3. Weekly Summary

**When:** Every Monday at 9:00 AM
**Who:** All team members
**Contents:**
- Tasks completed in the past week
- Phase progress with visual bars
- Overall project health

### 4. Auto-Complete Date

**When:** Task status changes to "Complete"
**Action:** Automatically fills the "Completed" date column

---

## Custom Menu

After setup, you'll see a **🚀 PopTop** menu with these options:

| Option | What it does |
|--------|--------------|
| 📧 Send Daily Digest Now | Manually trigger daily digest |
| 📈 Send Weekly Summary Now | Manually trigger weekly summary |
| 🔔 Check Overdue Tasks | Manually send overdue alerts |
| ⚙️ Setup Automation | Re-run trigger setup |
| 🗑️ Remove Automation | Turn off all automation |

---

## Customization

### Change Email Time

In `Code.gs`, find the `setupTriggers` function:

```javascript
// Change from 8 AM to 7 AM:
ScriptApp.newTrigger('sendDailyDigest')
  .timeBased()
  .atHour(7)  // Change this number
  .everyDays(1)
  .create();
```

### Change Warning Days

In the CONFIG section at the top:

```javascript
// Change from 3 to 5 days:
WARNING_DAYS: 5,
```

### Add Custom Notifications

You can add Slack integration by adding a webhook:

```javascript
function sendSlackNotification(message) {
  const webhookUrl = 'YOUR_SLACK_WEBHOOK_URL';
  const payload = {
    text: message
  };
  UrlFetchApp.fetch(webhookUrl, {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify(payload)
  });
}
```

---

## Troubleshooting

### Emails not sending

1. Check Team sheet has valid emails
2. Verify you have email quota: run `testSetup`
3. Check spam/junk folders
4. Make sure triggers are set up: Extensions → Apps Script → Triggers (clock icon)

### Triggers not running

1. Go to Apps Script → Triggers (clock icon on left)
2. Verify triggers are listed
3. Check for failed executions (red X)
4. Re-run `setupTriggers` if needed

### Permission errors

1. Run any function manually first
2. Complete the authorization flow
3. Make sure you're using the same Google account

### "Script function not found"

1. Make sure you copied ALL the code
2. Check for syntax errors (red underlines)
3. Save the script (Ctrl+S)

---

## Advanced: Connecting to Neon PostgreSQL

For future expansion, you can connect to a Neon database:

```javascript
function queryNeonDB(query) {
  const connectionString = 'postgresql://user:pass@host/db';
  // Use JDBC or external service
  // This requires additional setup
}
```

This enables:
- Historical data storage
- Advanced reporting
- API access to project data

---

## Email Quota Limits

Google Apps Script has daily email limits:

| Account Type | Daily Limit |
|--------------|-------------|
| Consumer Gmail | 100 emails |
| Google Workspace | 1,500 emails |

With a 5-person team getting 3 emails/day max = 15 emails/day, well within limits.

---

## Security Notes

1. **Don't share the Apps Script link** publicly
2. **Review permissions** before authorizing
3. **Team emails are visible** to sheet editors
4. **Sensitive data** should not go in shared sheets

---

## Quick Reference

| What | How |
|------|-----|
| Add a task | Tasks tab → new row |
| Update status | Tasks tab → column E |
| See overview | Dashboard tab |
| Manual digest | 🚀 PopTop menu → Send Daily Digest |
| Check triggers | Extensions → Apps Script → Triggers |
| View logs | Extensions → Apps Script → Executions |

---

*Last updated: January 2025*
