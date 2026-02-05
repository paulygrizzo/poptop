/**
 * PopTop Command Center - Google Apps Script
 * Main automation code for project management dashboard
 *
 * SETUP INSTRUCTIONS:
 * 1. Open your Google Sheet
 * 2. Go to Extensions → Apps Script
 * 3. Delete any existing code
 * 4. Copy and paste this entire file
 * 5. Save (Ctrl+S)
 * 6. Run 'setupTriggers' function once
 * 7. Authorize when prompted
 */

// ============================================
// CONFIGURATION
// ============================================

const CONFIG = {
  // Sheet names
  SHEETS: {
    TASKS: 'Tasks',
    PHASES: 'Phases',
    TEAM: 'Team',
    DASHBOARD: 'Dashboard',
    MEETINGS: 'Meetings',
    ACTION_ITEMS: 'Action Items',
    DECISIONS: 'Decisions',
    CONFIG: 'Config'
  },

  // Email settings
  EMAIL: {
    DIGEST_SUBJECT: '📋 PopTop Daily Digest',
    ALERT_SUBJECT: '🚨 PopTop: Action Required',
    FROM_NAME: 'PopTop Command Center'
  },

  // Task status values
  STATUS: {
    NOT_STARTED: 'Not Started',
    IN_PROGRESS: 'In Progress',
    COMPLETE: 'Complete',
    BLOCKED: 'Blocked',
    ON_HOLD: 'On Hold'
  },

  // Days before due date to send warning
  WARNING_DAYS: 3,

  // Days overdue before escalation
  ESCALATION_DAYS: 5
};

// ============================================
// TRIGGER SETUP
// ============================================

/**
 * Run this function ONCE to set up all automated triggers
 */
function setupTriggers() {
  // Clear existing triggers first
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => ScriptApp.deleteTrigger(trigger));

  // Digest on Monday at 8 AM
  ScriptApp.newTrigger('sendDailyDigest')
    .timeBased()
    .onWeekDay(ScriptApp.WeekDay.MONDAY)
    .atHour(8)
    .create();

  // Digest on Wednesday at 8 AM (day before Thursday standing call)
  ScriptApp.newTrigger('sendDailyDigest')
    .timeBased()
    .onWeekDay(ScriptApp.WeekDay.WEDNESDAY)
    .atHour(8)
    .create();

  // Check for overdue tasks once daily at 9 AM
  ScriptApp.newTrigger('checkOverdueTasks')
    .timeBased()
    .atHour(9)
    .everyDays(1)
    .create();

  // Weekly summary on Monday at 9 AM
  ScriptApp.newTrigger('sendWeeklySummary')
    .timeBased()
    .onWeekDay(ScriptApp.WeekDay.MONDAY)
    .atHour(9)
    .create();

  // Update dashboard on edit
  ScriptApp.newTrigger('onEditTrigger')
    .forSpreadsheet(SpreadsheetApp.getActive())
    .onEdit()
    .create();

  Logger.log('✅ All triggers set up successfully!');
  SpreadsheetApp.getUi().alert('Triggers set up successfully! Automation is now active.');
}

/**
 * Remove all triggers (for cleanup)
 */
function removeTriggers() {
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => ScriptApp.deleteTrigger(trigger));
  Logger.log('All triggers removed');
}

// ============================================
// DAILY DIGEST
// ============================================

/**
 * Send daily digest email to all team members
 */
function sendDailyDigest() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const tasksSheet = ss.getSheetByName(CONFIG.SHEETS.TASKS);
  const teamSheet = ss.getSheetByName(CONFIG.SHEETS.TEAM);

  if (!tasksSheet || !teamSheet) {
    Logger.log('Required sheets not found');
    return;
  }

  const tasks = getTasksData(tasksSheet);
  const team = getTeamData(teamSheet);

  // Get summary data
  const overdueTasks = tasks.filter(t => isOverdue(t));
  const dueSoonTasks = tasks.filter(t => isDueSoon(t, CONFIG.WARNING_DAYS));
  const inProgressTasks = tasks.filter(t => t.status === CONFIG.STATUS.IN_PROGRESS);
  const blockedTasks = tasks.filter(t => t.status === CONFIG.STATUS.BLOCKED);

  // Build email content
  const subject = `${CONFIG.EMAIL.DIGEST_SUBJECT} - ${formatDate(new Date())}`;

  let body = `
<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
  <div style="background: #1a365d; color: white; padding: 20px; text-align: center;">
    <h1 style="margin: 0;">Pop<span style="color: #c9a227;">Top</span></h1>
    <p style="margin: 5px 0 0 0;">Daily Project Digest</p>
  </div>

  <div style="padding: 20px;">
    <h2 style="color: #1a365d; border-bottom: 2px solid #c9a227; padding-bottom: 10px;">
      📊 Quick Stats
    </h2>
    <table style="width: 100%; margin-bottom: 20px;">
      <tr>
        <td style="padding: 10px; background: #f7fafc; text-align: center;">
          <div style="font-size: 24px; font-weight: bold; color: #1a365d;">${tasks.length}</div>
          <div style="color: #718096;">Total Tasks</div>
        </td>
        <td style="padding: 10px; background: #f7fafc; text-align: center;">
          <div style="font-size: 24px; font-weight: bold; color: #38a169;">${tasks.filter(t => t.status === CONFIG.STATUS.COMPLETE).length}</div>
          <div style="color: #718096;">Completed</div>
        </td>
        <td style="padding: 10px; background: #f7fafc; text-align: center;">
          <div style="font-size: 24px; font-weight: bold; color: #3182ce;">${inProgressTasks.length}</div>
          <div style="color: #718096;">In Progress</div>
        </td>
        <td style="padding: 10px; background: #f7fafc; text-align: center;">
          <div style="font-size: 24px; font-weight: bold; color: #e53e3e;">${overdueTasks.length}</div>
          <div style="color: #718096;">Overdue</div>
        </td>
      </tr>
    </table>
`;

  // Overdue section
  if (overdueTasks.length > 0) {
    body += `
    <h2 style="color: #e53e3e;">🚨 Overdue Tasks (${overdueTasks.length})</h2>
    <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
      <tr style="background: #fed7d7;">
        <th style="padding: 8px; text-align: left;">Task</th>
        <th style="padding: 8px; text-align: left;">Owner</th>
        <th style="padding: 8px; text-align: left;">Days Overdue</th>
      </tr>
`;
    overdueTasks.forEach(task => {
      const daysOverdue = Math.floor((new Date() - task.dueDate) / (1000 * 60 * 60 * 24));
      body += `
      <tr style="background: #fff5f5;">
        <td style="padding: 8px; border-bottom: 1px solid #feb2b2;">${task.name}</td>
        <td style="padding: 8px; border-bottom: 1px solid #feb2b2;">${task.owner}</td>
        <td style="padding: 8px; border-bottom: 1px solid #feb2b2; color: #c53030; font-weight: bold;">${daysOverdue} days</td>
      </tr>
`;
    });
    body += `</table>`;
  }

  // Due soon section
  if (dueSoonTasks.length > 0) {
    body += `
    <h2 style="color: #d69e2e;">⚠️ Due Soon (${dueSoonTasks.length})</h2>
    <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
      <tr style="background: #fefcbf;">
        <th style="padding: 8px; text-align: left;">Task</th>
        <th style="padding: 8px; text-align: left;">Owner</th>
        <th style="padding: 8px; text-align: left;">Due Date</th>
      </tr>
`;
    dueSoonTasks.forEach(task => {
      body += `
      <tr style="background: #fffff0;">
        <td style="padding: 8px; border-bottom: 1px solid #ecc94b;">${task.name}</td>
        <td style="padding: 8px; border-bottom: 1px solid #ecc94b;">${task.owner}</td>
        <td style="padding: 8px; border-bottom: 1px solid #ecc94b;">${formatDate(task.dueDate)}</td>
      </tr>
`;
    });
    body += `</table>`;
  }

  // Blocked section
  if (blockedTasks.length > 0) {
    body += `
    <h2 style="color: #dd6b20;">🛑 Blocked Tasks (${blockedTasks.length})</h2>
    <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
      <tr style="background: #feebc8;">
        <th style="padding: 8px; text-align: left;">Task</th>
        <th style="padding: 8px; text-align: left;">Owner</th>
        <th style="padding: 8px; text-align: left;">Blocker</th>
      </tr>
`;
    blockedTasks.forEach(task => {
      body += `
      <tr style="background: #fffaf0;">
        <td style="padding: 8px; border-bottom: 1px solid #ed8936;">${task.name}</td>
        <td style="padding: 8px; border-bottom: 1px solid #ed8936;">${task.owner}</td>
        <td style="padding: 8px; border-bottom: 1px solid #ed8936;">${task.blocker || 'Not specified'}</td>
      </tr>
`;
    });
    body += `</table>`;
  }

  // Team workload
  body += `
    <h2 style="color: #1a365d;">👥 Team Workload</h2>
    <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
      <tr style="background: #1a365d; color: white;">
        <th style="padding: 8px; text-align: left;">Team Member</th>
        <th style="padding: 8px; text-align: center;">Active</th>
        <th style="padding: 8px; text-align: center;">Completed</th>
        <th style="padding: 8px; text-align: center;">Total</th>
      </tr>
`;

  team.forEach(member => {
    const memberTasks = tasks.filter(t => t.owner === member.name);
    const active = memberTasks.filter(t => t.status === CONFIG.STATUS.IN_PROGRESS).length;
    const completed = memberTasks.filter(t => t.status === CONFIG.STATUS.COMPLETE).length;
    body += `
      <tr style="background: #f7fafc;">
        <td style="padding: 8px; border-bottom: 1px solid #e2e8f0;">${member.name}</td>
        <td style="padding: 8px; border-bottom: 1px solid #e2e8f0; text-align: center;">${active}</td>
        <td style="padding: 8px; border-bottom: 1px solid #e2e8f0; text-align: center;">${completed}</td>
        <td style="padding: 8px; border-bottom: 1px solid #e2e8f0; text-align: center;">${memberTasks.length}</td>
      </tr>
`;
  });
  body += `</table>`;

  // Footer
  body += `
    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e2e8f0; text-align: center; color: #718096;">
      <p><a href="${ss.getUrl()}" style="color: #3182ce;">Open Dashboard</a></p>
      <p style="font-size: 12px;">PopTop Command Center • Automated Daily Digest</p>
    </div>
  </div>
</div>
`;

  // Send to all team members with emails
  team.forEach(member => {
    if (member.email && member.email.includes('@')) {
      try {
        MailApp.sendEmail({
          to: member.email,
          subject: subject,
          htmlBody: body
        });
        Logger.log(`Digest sent to ${member.name} (${member.email})`);
      } catch (e) {
        Logger.log(`Failed to send to ${member.email}: ${e.message}`);
      }
    }
  });
}

// ============================================
// OVERDUE TASK ALERTS
// ============================================

/**
 * Check for overdue tasks and send alerts to owners
 */
function checkOverdueTasks() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const tasksSheet = ss.getSheetByName(CONFIG.SHEETS.TASKS);
  const teamSheet = ss.getSheetByName(CONFIG.SHEETS.TEAM);

  if (!tasksSheet || !teamSheet) return;

  const tasks = getTasksData(tasksSheet);
  const team = getTeamData(teamSheet);
  const teamMap = {};
  team.forEach(m => teamMap[m.name] = m);

  const overdueTasks = tasks.filter(t => isOverdue(t));

  // Group by owner
  const byOwner = {};
  overdueTasks.forEach(task => {
    if (!byOwner[task.owner]) byOwner[task.owner] = [];
    byOwner[task.owner].push(task);
  });

  // Send individual alerts
  Object.keys(byOwner).forEach(ownerName => {
    const member = teamMap[ownerName];
    if (!member || !member.email) return;

    const ownerTasks = byOwner[ownerName];
    const subject = `🚨 PopTop Alert: You have ${ownerTasks.length} overdue task(s)`;

    let body = `
<div style="font-family: Arial, sans-serif; max-width: 500px;">
  <h2 style="color: #e53e3e;">Action Required</h2>
  <p>Hi ${ownerName.split(' ')[0]},</p>
  <p>The following tasks are overdue and need your attention:</p>
  <ul>
`;

    ownerTasks.forEach(task => {
      const daysOverdue = Math.floor((new Date() - task.dueDate) / (1000 * 60 * 60 * 24));
      body += `<li><strong>${task.name}</strong> - ${daysOverdue} days overdue</li>`;
    });

    body += `
  </ul>
  <p>Please update the status or complete these tasks as soon as possible.</p>
  <p><a href="${ss.getUrl()}" style="color: #3182ce;">Open Dashboard</a></p>
</div>
`;

    try {
      MailApp.sendEmail({
        to: member.email,
        subject: subject,
        htmlBody: body
      });
    } catch (e) {
      Logger.log(`Failed to send alert to ${member.email}: ${e.message}`);
    }
  });
}

// ============================================
// WEEKLY SUMMARY
// ============================================

/**
 * Send weekly summary every Monday
 */
function sendWeeklySummary() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const tasksSheet = ss.getSheetByName(CONFIG.SHEETS.TASKS);
  const teamSheet = ss.getSheetByName(CONFIG.SHEETS.TEAM);
  const phasesSheet = ss.getSheetByName(CONFIG.SHEETS.PHASES);

  if (!tasksSheet || !teamSheet) return;

  const tasks = getTasksData(tasksSheet);
  const team = getTeamData(teamSheet);
  const phases = phasesSheet ? getPhasesData(phasesSheet) : [];

  // Calculate week's progress
  const oneWeekAgo = new Date();
  oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);

  const completedThisWeek = tasks.filter(t =>
    t.completedDate && t.completedDate >= oneWeekAgo
  );

  const subject = `📈 PopTop Weekly Summary - Week of ${formatDate(oneWeekAgo)}`;

  let body = `
<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
  <div style="background: #1a365d; color: white; padding: 20px; text-align: center;">
    <h1 style="margin: 0;">Pop<span style="color: #c9a227;">Top</span></h1>
    <p style="margin: 5px 0 0 0;">Weekly Progress Report</p>
  </div>

  <div style="padding: 20px;">
    <h2 style="color: #38a169;">✅ Completed This Week (${completedThisWeek.length})</h2>
`;

  if (completedThisWeek.length > 0) {
    body += `<ul>`;
    completedThisWeek.forEach(task => {
      body += `<li><strong>${task.name}</strong> - ${task.owner}</li>`;
    });
    body += `</ul>`;
  } else {
    body += `<p style="color: #718096;">No tasks completed this week.</p>`;
  }

  // Phase progress
  if (phases.length > 0) {
    body += `
    <h2 style="color: #1a365d;">📊 Phase Progress</h2>
    <table style="width: 100%; border-collapse: collapse;">
`;
    phases.forEach(phase => {
      const phaseTasks = tasks.filter(t => t.phase && t.phase.includes(phase.name));
      const completed = phaseTasks.filter(t => t.status === CONFIG.STATUS.COMPLETE).length;
      const percent = phaseTasks.length > 0 ? Math.round((completed / phaseTasks.length) * 100) : 0;

      body += `
      <tr>
        <td style="padding: 8px;">${phase.name}</td>
        <td style="padding: 8px; width: 200px;">
          <div style="background: #e2e8f0; border-radius: 4px; overflow: hidden;">
            <div style="background: #38a169; height: 20px; width: ${percent}%;"></div>
          </div>
        </td>
        <td style="padding: 8px; text-align: right;">${percent}%</td>
      </tr>
`;
    });
    body += `</table>`;
  }

  body += `
    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e2e8f0; text-align: center;">
      <p><a href="${ss.getUrl()}" style="color: #3182ce;">Open Dashboard</a></p>
    </div>
  </div>
</div>
`;

  // Send to all team members
  team.forEach(member => {
    if (member.email && member.email.includes('@')) {
      try {
        MailApp.sendEmail({
          to: member.email,
          subject: subject,
          htmlBody: body
        });
      } catch (e) {
        Logger.log(`Failed to send weekly summary to ${member.email}: ${e.message}`);
      }
    }
  });
}

// ============================================
// ON EDIT TRIGGER
// ============================================

/**
 * Handle edits to the spreadsheet
 */
function onEditTrigger(e) {
  if (!e) return;

  const sheet = e.source.getActiveSheet();
  const range = e.range;

  // Only process Tasks sheet
  if (sheet.getName() !== CONFIG.SHEETS.TASKS) return;

  const col = range.getColumn();
  const row = range.getRow();

  // Skip header row
  if (row === 1) return;

  // Column E is Status (adjust if different)
  const STATUS_COL = 5;
  const COMPLETED_COL = 9;

  // If status changed to Complete, auto-fill completed date
  if (col === STATUS_COL && e.value === CONFIG.STATUS.COMPLETE) {
    sheet.getRange(row, COMPLETED_COL).setValue(new Date());
  }

  // Update dashboard on task edits
  updateDashboard();
}

// ============================================
// DASHBOARD BUILDER
// ============================================

/**
 * Build/refresh the Dashboard tab with live data from Tasks, Phases, and Team sheets.
 * Run manually from PopTop menu or auto-runs on task edits.
 */
function updateDashboard() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const tasksSheet = ss.getSheetByName(CONFIG.SHEETS.TASKS);
  const phasesSheet = ss.getSheetByName(CONFIG.SHEETS.PHASES);
  const teamSheet = ss.getSheetByName(CONFIG.SHEETS.TEAM);
  let dashSheet = ss.getSheetByName(CONFIG.SHEETS.DASHBOARD);

  if (!tasksSheet) return;

  // Create Dashboard sheet if missing
  if (!dashSheet) {
    dashSheet = ss.insertSheet(CONFIG.SHEETS.DASHBOARD, 0);
  }

  const tasks = getTasksData(tasksSheet);
  const team = teamSheet ? getTeamData(teamSheet) : [];
  const phases = phasesSheet ? getPhasesData(phasesSheet) : [];

  const today = new Date();
  const totalTasks = tasks.length;
  const completed = tasks.filter(t => t.status === CONFIG.STATUS.COMPLETE).length;
  const inProgress = tasks.filter(t => t.status === CONFIG.STATUS.IN_PROGRESS).length;
  const blocked = tasks.filter(t => t.status === CONFIG.STATUS.BLOCKED).length;
  const notStarted = tasks.filter(t => t.status === CONFIG.STATUS.NOT_STARTED).length;
  const overdue = tasks.filter(t => isOverdue(t));

  // Clear existing content
  dashSheet.clear();
  dashSheet.clearFormats();

  let row = 1;

  // ── TITLE ──
  dashSheet.getRange(row, 1, 1, 6).merge()
    .setValue('POPTOP COMMAND CENTER')
    .setFontSize(18).setFontWeight('bold')
    .setFontColor('#FFFFFF').setBackground('#1a365d')
    .setHorizontalAlignment('center')
    .setVerticalAlignment('middle');
  dashSheet.setRowHeight(row, 50);
  row++;

  dashSheet.getRange(row, 1, 1, 6).merge()
    .setValue('Last Updated: ' + Utilities.formatDate(today, Session.getScriptTimeZone(), 'MMM d, yyyy h:mm a'))
    .setFontSize(9).setFontColor('#718096')
    .setHorizontalAlignment('center').setBackground('#f7fafc');
  row += 2;

  // ── QUICK STATS ──
  dashSheet.getRange(row, 1, 1, 6).merge()
    .setValue('QUICK STATS')
    .setFontSize(12).setFontWeight('bold').setFontColor('#1a365d');
  row++;

  const statLabels = ['Total Tasks', 'Completed', 'In Progress', 'Blocked', 'Not Started', 'Overdue'];
  const statValues = [totalTasks, completed, inProgress, blocked, notStarted, overdue.length];
  const statColors = ['#1a365d', '#38a169', '#3182ce', '#dd6b20', '#718096', '#e53e3e'];

  dashSheet.getRange(row, 1, 1, 6).setValues([statLabels])
    .setFontSize(9).setFontColor('#718096').setHorizontalAlignment('center');
  row++;

  dashSheet.getRange(row, 1, 1, 6).setValues([statValues])
    .setFontSize(22).setFontWeight('bold').setHorizontalAlignment('center');
  for (let c = 0; c < 6; c++) {
    dashSheet.getRange(row, c + 1).setFontColor(statColors[c]);
  }
  dashSheet.getRange(row - 1, 1, 2, 6).setBackground('#f7fafc');
  row += 2;

  // ── PHASE PROGRESS ──
  dashSheet.getRange(row, 1, 1, 6).merge()
    .setValue('PHASE PROGRESS')
    .setFontSize(12).setFontWeight('bold').setFontColor('#1a365d');
  row++;

  dashSheet.getRange(row, 1, 1, 4).setValues([['Phase', 'Progress', '', '% Complete']])
    .setFontSize(9).setFontWeight('bold').setFontColor('#FFFFFF').setBackground('#1a365d');
  row++;

  if (phases.length > 0) {
    phases.forEach((phase, idx) => {
      const phaseName = phase.phase || phase.name || ('Phase ' + (idx + 1));
      const displayName = phase.name ? (phase.phase + ': ' + phase.name) : phaseName;
      const phaseTasks = tasks.filter(t => t.phase && t.phase.toString().includes(phaseName));
      const phaseCompleted = phaseTasks.filter(t => t.status === CONFIG.STATUS.COMPLETE).length;
      const pct = phaseTasks.length > 0 ? Math.round((phaseCompleted / phaseTasks.length) * 100) : 0;

      const barFull = Math.round(pct / 10);
      const barEmpty = 10 - barFull;
      const progressBar = '\u2588'.repeat(barFull) + '\u2591'.repeat(barEmpty);

      dashSheet.getRange(row, 1).setValue(displayName).setFontSize(10);
      dashSheet.getRange(row, 2, 1, 2).merge().setValue(progressBar)
        .setFontSize(10).setFontColor(pct >= 80 ? '#38a169' : (pct >= 40 ? '#d69e2e' : '#718096'));
      dashSheet.getRange(row, 4).setValue(pct + '%').setFontSize(10).setHorizontalAlignment('center');

      if (idx % 2 === 0) {
        dashSheet.getRange(row, 1, 1, 4).setBackground('#f7fafc');
      }
      row++;
    });
  } else {
    dashSheet.getRange(row, 1, 1, 4).merge().setValue('No phases data found').setFontColor('#718096');
    row++;
  }
  row++;

  // ── OVERDUE TASKS ──
  if (overdue.length > 0) {
    dashSheet.getRange(row, 1, 1, 6).merge()
      .setValue('OVERDUE TASKS (' + overdue.length + ')')
      .setFontSize(12).setFontWeight('bold').setFontColor('#e53e3e');
    row++;

    dashSheet.getRange(row, 1, 1, 4).setValues([['Task', 'Owner', 'Due Date', 'Days Overdue']])
      .setFontSize(9).setFontWeight('bold').setFontColor('#FFFFFF').setBackground('#e53e3e');
    row++;

    overdue.sort((a, b) => a.dueDate - b.dueDate).forEach(task => {
      const daysOver = Math.floor((today - task.dueDate) / (1000 * 60 * 60 * 24));
      dashSheet.getRange(row, 1).setValue(task.name).setFontSize(9);
      dashSheet.getRange(row, 2).setValue(task.owner).setFontSize(9);
      dashSheet.getRange(row, 3).setValue(task.dueDate ? Utilities.formatDate(task.dueDate, Session.getScriptTimeZone(), 'MMM d') : '').setFontSize(9);
      dashSheet.getRange(row, 4).setValue(daysOver + ' days').setFontSize(9).setFontColor('#e53e3e').setFontWeight('bold');
      dashSheet.getRange(row, 1, 1, 4).setBackground('#fff5f5');
      row++;
    });
    row++;
  }

  // ── TEAM WORKLOAD ──
  if (team.length > 0) {
    dashSheet.getRange(row, 1, 1, 6).merge()
      .setValue('TEAM WORKLOAD')
      .setFontSize(12).setFontWeight('bold').setFontColor('#1a365d');
    row++;

    dashSheet.getRange(row, 1, 1, 5).setValues([['Team Member', 'Active', 'Completed', 'Total', 'Completion %']])
      .setFontSize(9).setFontWeight('bold').setFontColor('#FFFFFF').setBackground('#1a365d');
    row++;

    team.forEach((member, idx) => {
      const memberTasks = tasks.filter(t => t.owner === member.name);
      const active = memberTasks.filter(t => t.status === CONFIG.STATUS.IN_PROGRESS).length;
      const done = memberTasks.filter(t => t.status === CONFIG.STATUS.COMPLETE).length;
      const total = memberTasks.length;
      const pct = total > 0 ? Math.round((done / total) * 100) + '%' : '--';

      dashSheet.getRange(row, 1).setValue(member.name).setFontSize(10);
      dashSheet.getRange(row, 2).setValue(active).setFontSize(10).setHorizontalAlignment('center');
      dashSheet.getRange(row, 3).setValue(done).setFontSize(10).setHorizontalAlignment('center');
      dashSheet.getRange(row, 4).setValue(total).setFontSize(10).setHorizontalAlignment('center');
      dashSheet.getRange(row, 5).setValue(pct).setFontSize(10).setHorizontalAlignment('center');

      if (idx % 2 === 0) {
        dashSheet.getRange(row, 1, 1, 5).setBackground('#f7fafc');
      }
      row++;
    });
    row++;
  }

  // ── UPCOMING MILESTONES ──
  dashSheet.getRange(row, 1, 1, 6).merge()
    .setValue('KEY MILESTONES')
    .setFontSize(12).setFontWeight('bold').setFontColor('#1a365d');
  row++;

  const milestones = [
    ['Reboot Call', 'Feb 6, 2026'],
    ['Design Freeze', 'Apr 24, 2026'],
    ['CLC Submission', 'May 1, 2026'],
    ['CLC Approval (est.)', 'Jun 12 - Jul 24, 2026'],
    ['Production Auth', 'Jul 31, 2026'],
    ['Soft Launch', 'Aug 21, 2026'],
    ['PUBLIC LAUNCH', 'Sep 1, 2026'],
  ];

  dashSheet.getRange(row, 1, 1, 2).setValues([['Milestone', 'Target Date']])
    .setFontSize(9).setFontWeight('bold').setFontColor('#FFFFFF').setBackground('#1a365d');
  row++;

  milestones.forEach((m, idx) => {
    dashSheet.getRange(row, 1).setValue(m[0]).setFontSize(10);
    dashSheet.getRange(row, 2).setValue(m[1]).setFontSize(10);
    if (m[0] === 'PUBLIC LAUNCH') {
      dashSheet.getRange(row, 1, 1, 2).setFontWeight('bold').setFontColor('#1a365d');
    }
    if (idx % 2 === 0) {
      dashSheet.getRange(row, 1, 1, 2).setBackground('#f7fafc');
    }
    row++;
  });

  // ── COLUMN WIDTHS ──
  dashSheet.setColumnWidth(1, 200);
  dashSheet.setColumnWidth(2, 130);
  dashSheet.setColumnWidth(3, 100);
  dashSheet.setColumnWidth(4, 100);
  dashSheet.setColumnWidth(5, 100);
  dashSheet.setColumnWidth(6, 100);

  // Freeze title row
  dashSheet.setFrozenRows(2);

  Logger.log('Dashboard updated at ' + today);
}

// ============================================
// UTILITY FUNCTIONS
// ============================================

/**
 * Get all tasks from the Tasks sheet
 */
function getTasksData(sheet) {
  const data = sheet.getDataRange().getValues();
  const headers = data[0];
  const tasks = [];

  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    if (!row[2]) continue; // Skip empty rows (no task name)

    tasks.push({
      id: row[0],
      phase: row[1],
      name: row[2],
      owner: row[3],
      status: row[4],
      priority: row[5],
      startDate: row[6] ? new Date(row[6]) : null,
      dueDate: row[7] ? new Date(row[7]) : null,
      completedDate: row[8] ? new Date(row[8]) : null,
      blocker: row[10],
      notes: row[11]
    });
  }

  return tasks;
}

/**
 * Get team data from Team sheet
 */
function getTeamData(sheet) {
  const data = sheet.getDataRange().getValues();
  const team = [];

  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    if (!row[0]) continue;

    team.push({
      name: row[0],
      role: row[1],
      email: row[2],
      phone: row[3],
      area: row[4]
    });
  }

  return team;
}

/**
 * Get phases data
 */
function getPhasesData(sheet) {
  const data = sheet.getDataRange().getValues();
  const phases = [];

  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    if (!row[0]) continue;

    phases.push({
      phase: row[0],
      name: row[1],
      owner: row[2],
      startDate: row[3],
      targetEnd: row[4],
      status: row[5]
    });
  }

  return phases;
}

/**
 * Check if task is overdue
 */
function isOverdue(task) {
  if (!task.dueDate) return false;
  if (task.status === CONFIG.STATUS.COMPLETE) return false;
  return task.dueDate < new Date();
}

/**
 * Check if task is due soon
 */
function isDueSoon(task, days) {
  if (!task.dueDate) return false;
  if (task.status === CONFIG.STATUS.COMPLETE) return false;
  if (isOverdue(task)) return false;

  const today = new Date();
  const diffDays = Math.ceil((task.dueDate - today) / (1000 * 60 * 60 * 24));
  return diffDays <= days && diffDays >= 0;
}

/**
 * Format date as readable string
 */
function formatDate(date) {
  if (!date) return '';
  return Utilities.formatDate(date, Session.getScriptTimeZone(), 'MMM d, yyyy');
}

/**
 * Get action items data from Action Items sheet
 */
function getActionItemsData(sheet) {
  const data = sheet.getDataRange().getValues();
  const items = [];

  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    if (!row[0]) continue;

    items.push({
      arNum: row[0],
      meetingDate: row[1] ? new Date(row[1]) : null,
      owner: row[2],
      action: row[3],
      dueDate: row[4] ? new Date(row[4]) : null,
      status: row[5],
      completedDate: row[6] ? new Date(row[6]) : null,
      notes: row[7]
    });
  }

  return items;
}

/**
 * Get open action items for a specific owner
 */
function getOpenActionItemsForOwner(ownerName) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const arSheet = ss.getSheetByName(CONFIG.SHEETS.ACTION_ITEMS);
  if (!arSheet) return [];

  const items = getActionItemsData(arSheet);
  return items.filter(item =>
    item.owner === ownerName &&
    item.status !== 'Complete' &&
    item.status !== 'Closed'
  );
}

// ============================================
// MANUAL FUNCTIONS (Menu Items)
// ============================================

/**
 * Add custom menu when spreadsheet opens
 */
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('🚀 PopTop')
    .addItem('📊 Refresh Dashboard', 'updateDashboard')
    .addItem('📧 Send Daily Digest Now', 'sendDailyDigest')
    .addItem('📈 Send Weekly Summary Now', 'sendWeeklySummary')
    .addItem('🔔 Check Overdue Tasks', 'checkOverdueTasks')
    .addItem('📝 Send Meeting Notes', 'promptAndSendMeetingNotes')
    .addItem('📋 Review Open Action Items', 'showOpenActionItems')
    .addSeparator()
    .addItem('⚙️ Setup Automation', 'setupTriggers')
    .addItem('🗑️ Remove Automation', 'removeTriggers')
    .addToUi();
}

/**
 * Prompt user for meeting date and send notes
 */
function promptAndSendMeetingNotes() {
  const ui = SpreadsheetApp.getUi();
  const response = ui.prompt(
    'Send Meeting Notes',
    'Enter meeting date (YYYY-MM-DD) or leave blank for today:',
    ui.ButtonSet.OK_CANCEL
  );

  if (response.getSelectedButton() === ui.Button.OK) {
    const dateStr = response.getResponseText().trim();
    const meetingDate = dateStr ? new Date(dateStr) : new Date();
    sendMeetingNotesEmail(meetingDate);
  }
}

/**
 * Send meeting notes email to all team members
 */
function sendMeetingNotesEmail(meetingDate) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const teamSheet = ss.getSheetByName(CONFIG.SHEETS.TEAM);
  const arSheet = ss.getSheetByName(CONFIG.SHEETS.ACTION_ITEMS);
  const meetingsSheet = ss.getSheetByName(CONFIG.SHEETS.MEETINGS);

  if (!teamSheet) {
    SpreadsheetApp.getUi().alert('Team sheet not found!');
    return;
  }

  const team = getTeamData(teamSheet);
  const actionItems = arSheet ? getActionItemsData(arSheet) : [];

  // Filter action items from this meeting
  const meetingDateStr = Utilities.formatDate(meetingDate, Session.getScriptTimeZone(), 'yyyy-MM-dd');
  const meetingItems = actionItems.filter(item => {
    if (!item.meetingDate) return false;
    const itemDateStr = Utilities.formatDate(item.meetingDate, Session.getScriptTimeZone(), 'yyyy-MM-dd');
    return itemDateStr === meetingDateStr;
  });

  const formattedDate = Utilities.formatDate(meetingDate, Session.getScriptTimeZone(), 'EEEE, MMMM d, yyyy');
  const subject = `📝 PopTop Meeting Notes - ${formattedDate}`;

  let body = `
<div style="font-family: Arial, sans-serif; max-width: 700px; margin: 0 auto;">
  <div style="background: #1a365d; color: white; padding: 20px; text-align: center;">
    <h1 style="margin: 0;">Pop<span style="color: #c9a227;">Top</span></h1>
    <p style="margin: 5px 0 0 0;">Meeting Notes - ${formattedDate}</p>
  </div>

  <div style="padding: 20px;">
`;

  // Action Items section
  if (meetingItems.length > 0) {
    body += `
    <h2 style="color: #1a365d; border-bottom: 2px solid #c9a227; padding-bottom: 10px;">
      📋 Action Items (${meetingItems.length})
    </h2>
    <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
      <tr style="background: #1a365d; color: white;">
        <th style="padding: 10px; text-align: left;">AR#</th>
        <th style="padding: 10px; text-align: left;">Owner</th>
        <th style="padding: 10px; text-align: left;">Action</th>
        <th style="padding: 10px; text-align: left;">Due</th>
      </tr>
`;

    meetingItems.forEach((item, idx) => {
      const bgColor = idx % 2 === 0 ? '#f7fafc' : '#ffffff';
      const dueStr = item.dueDate ? Utilities.formatDate(item.dueDate, Session.getScriptTimeZone(), 'MMM d') : 'TBD';
      body += `
      <tr style="background: ${bgColor};">
        <td style="padding: 10px; border-bottom: 1px solid #e2e8f0;">${item.arNum}</td>
        <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; font-weight: bold;">${item.owner}</td>
        <td style="padding: 10px; border-bottom: 1px solid #e2e8f0;">${item.action}</td>
        <td style="padding: 10px; border-bottom: 1px solid #e2e8f0;">${dueStr}</td>
      </tr>
`;
    });
    body += `</table>`;

    // Summary by owner
    const byOwner = {};
    meetingItems.forEach(item => {
      if (!byOwner[item.owner]) byOwner[item.owner] = [];
      byOwner[item.owner].push(item);
    });

    body += `
    <h3 style="color: #1a365d;">Action Items by Owner</h3>
`;
    Object.keys(byOwner).forEach(owner => {
      body += `<p><strong>${owner}:</strong> ${byOwner[owner].length} item(s)</p><ul>`;
      byOwner[owner].forEach(item => {
        body += `<li>${item.action}</li>`;
      });
      body += `</ul>`;
    });
  } else {
    body += `<p style="color: #718096;">No action items recorded for this meeting.</p>`;
  }

  // Footer
  body += `
    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e2e8f0; text-align: center; color: #718096;">
      <p><a href="${ss.getUrl()}" style="color: #3182ce;">Open Command Center</a></p>
      <p style="font-size: 12px;">PopTop Command Center • Meeting Notes</p>
    </div>
  </div>
</div>
`;

  // Send to all team members
  let sentCount = 0;
  team.forEach(member => {
    if (member.email && member.email.includes('@')) {
      try {
        MailApp.sendEmail({
          to: member.email,
          subject: subject,
          htmlBody: body
        });
        sentCount++;
        Logger.log(`Meeting notes sent to ${member.name} (${member.email})`);
      } catch (e) {
        Logger.log(`Failed to send to ${member.email}: ${e.message}`);
      }
    }
  });

  SpreadsheetApp.getUi().alert(`Meeting notes sent to ${sentCount} team members!`);
}

/**
 * Show open action items summary
 */
function showOpenActionItems() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const arSheet = ss.getSheetByName(CONFIG.SHEETS.ACTION_ITEMS);

  if (!arSheet) {
    SpreadsheetApp.getUi().alert('Action Items sheet not found!');
    return;
  }

  const items = getActionItemsData(arSheet);
  const openItems = items.filter(item => item.status === 'Open');

  let summary = `Open Action Items: ${openItems.length}\n\n`;

  // Group by owner
  const byOwner = {};
  openItems.forEach(item => {
    if (!byOwner[item.owner]) byOwner[item.owner] = [];
    byOwner[item.owner].push(item);
  });

  Object.keys(byOwner).sort().forEach(owner => {
    summary += `${owner}: ${byOwner[owner].length}\n`;
    byOwner[owner].forEach(item => {
      const dueStr = item.dueDate ? Utilities.formatDate(item.dueDate, Session.getScriptTimeZone(), 'MMM d') : 'TBD';
      summary += `  • ${item.arNum}: ${item.action} (Due: ${dueStr})\n`;
    });
    summary += '\n';
  });

  SpreadsheetApp.getUi().alert('Open Action Items', summary, SpreadsheetApp.getUi().ButtonSet.OK);
}

/**
 * Test function to verify everything works
 */
function testSetup() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const ui = SpreadsheetApp.getUi();

  let status = '✅ Setup Check Results:\n\n';

  // Check sheets exist
  const requiredSheets = ['Tasks', 'Team', 'Phases', 'Dashboard'];
  requiredSheets.forEach(name => {
    const sheet = ss.getSheetByName(name);
    status += sheet ? `✓ ${name} sheet found\n` : `✗ ${name} sheet MISSING\n`;
  });

  // Check triggers
  const triggers = ScriptApp.getProjectTriggers();
  status += `\nTriggers: ${triggers.length} active\n`;

  // Check email quota
  const remaining = MailApp.getRemainingDailyQuota();
  status += `Email quota remaining: ${remaining}\n`;

  ui.alert('Setup Check', status, ui.ButtonSet.OK);
}
