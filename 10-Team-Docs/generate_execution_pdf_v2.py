#!/usr/bin/env python3
"""
PopTop Execution Plan v2.1 PDF Generator
Aggressive reset roadmap targeting Fall 2026 (Sep 1, 2026)
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfgen import canvas

# Colors
PRIMARY = HexColor('#1a365d')
SECONDARY = HexColor('#c9a227')
TEXT = HexColor('#2d3748')
TEXT_LIGHT = HexColor('#718096')
LIGHT = HexColor('#f7fafc')
SUCCESS = HexColor('#38a169')
WARNING = HexColor('#d69e2e')
DANGER = HexColor('#e53e3e')

def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(TEXT_LIGHT)
    canvas.drawCentredString(letter[0]/2, 0.5*inch, str(doc.page))
    canvas.restoreState()

def create_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name='DocTitle', fontName='Helvetica-Bold', fontSize=28,
        textColor=PRIMARY, alignment=TA_CENTER, spaceBefore=0, spaceAfter=15, leading=34,
    ))
    styles.add(ParagraphStyle(
        name='DocSubtitle', fontName='Helvetica', fontSize=14,
        textColor=TEXT_LIGHT, alignment=TA_CENTER, spaceBefore=10, spaceAfter=25, leading=18,
    ))
    styles.add(ParagraphStyle(
        name='SectionHeader', fontName='Helvetica-Bold', fontSize=16,
        textColor=PRIMARY, spaceBefore=20, spaceAfter=10,
    ))
    styles.add(ParagraphStyle(
        name='SubSection', fontName='Helvetica-Bold', fontSize=12,
        textColor=SECONDARY, spaceBefore=15, spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        name='Body', fontName='Helvetica', fontSize=10,
        textColor=TEXT, spaceBefore=4, spaceAfter=4, leading=14,
    ))
    styles.add(ParagraphStyle(
        name='BodySmall', fontName='Helvetica', fontSize=9,
        textColor=TEXT, spaceBefore=2, spaceAfter=2, leading=12,
    ))
    styles.add(ParagraphStyle(
        name='BulletItem', fontName='Helvetica', fontSize=10,
        textColor=TEXT, leftIndent=20, spaceBefore=2, spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        name='AlertText', fontName='Helvetica-Bold', fontSize=10,
        textColor=DANGER, spaceBefore=4, spaceAfter=4, leading=14,
    ))
    return styles

def create_table(headers, rows, col_widths=None):
    data = [headers] + rows
    if col_widths is None:
        col_widths = [6.5*inch / len(headers)] * len(headers)
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TEXTCOLOR', (0, 1), (-1, -1), TEXT),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT]),
        ('LINEBELOW', (0, 0), (-1, -2), 0.5, HexColor('#e2e8f0')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    return t

def create_highlight_box(content, styles):
    data = [[Paragraph(content, ParagraphStyle('BoxText', parent=styles['Body'], textColor=white))]]
    t = Table(data, colWidths=[6.5*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), PRIMARY),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
    ]))
    return t

def create_warning_box(content, styles):
    data = [[Paragraph(content, ParagraphStyle('WarnText', parent=styles['Body'], textColor=TEXT))]]
    t = Table(data, colWidths=[6.5*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor('#FFFBEB')),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
        ('BOX', (0, 0), (-1, -1), 1, WARNING),
    ]))
    return t

def build_document():
    output_path = '/Users/paulgiarrizzo/Projects/poptop/10-Team-Docs/PopTop-Execution-Plan-v2.pdf'

    doc = SimpleDocTemplate(
        output_path, pagesize=letter,
        rightMargin=0.75*inch, leftMargin=0.75*inch,
        topMargin=0.75*inch, bottomMargin=0.75*inch
    )

    styles = create_styles()
    story = []

    # ─── TITLE PAGE ───
    story.append(Paragraph("PopTop Execution Plan", styles['DocTitle']))
    story.append(Paragraph("NPI to RTM: Aggressive Reset Roadmap v2.1", styles['DocSubtitle']))

    meta = [
        ["Version: 2.1", "Date: February 2026"],
        ["Target RTM: Sep 1, 2026 (Football Season)", "Document Owner: Paul Giarrizzo"],
        ["Context: Aggressive 7-month timeline", "Previous: v2.0 (Feb 2025), v1.0 (Jan 2025)"]
    ]
    meta_table = Table(meta, colWidths=[3.25*inch, 3.25*inch])
    meta_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), TEXT_LIGHT),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 20))

    # Team Roster
    story.append(Paragraph("Team Roster & Responsibilities", styles['SectionHeader']))
    story.append(create_table(
        ["Name", "Role", "Primary Responsibilities", "Commitment"],
        [
            ["Paul Giarrizzo", "Business Lead", "Execution driver, biz dev, licensing, GTM", "Lead"],
            ["Alex Munn", "Co-Founder / Equity", "Strategic decisions, capital, TM/domain", "Advisory"],
            ["Ross Munn", "Co-Founder / Equity", "Manufacturing sourcing, suppliers", "Part-time"],
            ["Brian Williams", "Engineer", "SolidWorks CAD, prototyping, DFM", "NPI to RTM+6mo"],
            ["Nathan Childress", "Operations", "Task execution, social media", "As assigned"],
        ],
        [1.3*inch, 1.3*inch, 2.5*inch, 1.4*inch]
    ))

    story.append(Spacer(1, 15))
    story.append(create_highlight_box(
        "<b>Critical Path:</b> Team Alignment (Feb 6) -> Design Freeze (Apr 24) -> CLC Submission (May 1) -> "
        "CLC Approval (6-12 wks) -> Production (Jul) -> Inventory (Aug 14) -> LAUNCH (Sep 1, 2026)",
        styles
    ))

    # Key Dates
    story.append(Spacer(1, 15))
    story.append(Paragraph("Key Milestones", styles['SectionHeader']))
    story.append(create_table(
        ["Milestone", "Date"],
        [
            ["Reboot Call", "Feb 6, 2026"],
            ["Design Freeze", "Apr 24, 2026"],
            ["CLC Submission", "May 1, 2026"],
            ["CLC Approval (est.)", "Jun 12 - Jul 24, 2026"],
            ["Production Run Auth", "Jul 31, 2026"],
            ["Inventory at 3PL", "Aug 14, 2026"],
            ["Soft Launch", "Aug 21, 2026"],
            ["PUBLIC LAUNCH", "Sep 1, 2026"],
        ],
        [3.25*inch, 3.25*inch]
    ))

    # Timeline Overview
    story.append(Spacer(1, 15))
    story.append(Paragraph("Timeline Overview", styles['SectionHeader']))
    story.append(create_table(
        ["Phase", "Focus", "Start", "End", "Duration"],
        [
            ["Phase 0", "Reboot & Foundation", "Feb 4", "Feb 14", "2 weeks"],
            ["Phase 1", "Design & Prototyping", "Feb 9", "Apr 24", "10 weeks"],
            ["Phase 2", "Brand Identity & IP", "Feb 6", "Apr 3", "8 wks (parallel)"],
            ["Phase 3", "Manufacturing & Supply", "Apr 24", "Jul 31", "14 weeks"],
            ["Phase 4", "Licensing (CLC)", "Feb 13", "Aug 7", "6-12 wks post-freeze"],
            ["Phase 5", "Go-To-Market Prep", "Jun 19", "Aug 28", "10 weeks"],
            ["Phase 6", "Launch & Operations", "Aug 7", "Nov 30", "Football season"],
        ],
        [0.8*inch, 1.6*inch, 1.1*inch, 1.1*inch, 1.3*inch]
    ))

    story.append(PageBreak())

    # ─── PHASE 0 ───
    story.append(Paragraph("Phase 0: Reboot & Foundation (Feb 4 - 14, 2026)", styles['SectionHeader']))
    story.append(Paragraph("<b>Owner:</b> Paul Giarrizzo | <b>Goal:</b> Team re-aligned, infrastructure live, trademark path clear", styles['Body']))

    story.append(Paragraph("0.1 Team Realignment", styles['SubSection']))
    story.append(create_table(
        ["Task", "Owner", "Target"],
        [
            ["Thursday standing call (reboot)", "Paul", "Feb 6"],
            ["Confirm team commitment", "Paul", "Feb 13"],
            ["Brian: sign royalty agreement", "Paul + Brian", "Feb 13"],
            ["Alex: confirm capital for Phase 1-2", "Paul + Alex", "Feb 13"],
            ["Contact Ross -- update & re-engage", "Paul", "Feb 8"],
            ["Set up team communication channel", "Nathan / Paul", "Feb 13"],
        ],
        [3.5*inch, 1.5*inch, 1.5*inch]
    ))

    story.append(Paragraph("0.2 Project Infrastructure", styles['SubSection']))
    story.append(create_table(
        ["Task", "Owner", "Status", "Target"],
        [
            ["Deploy Google Sheets Command Center", "Paul", "COMPLETE", "Feb 4"],
            ["Share dashboard + docs with team", "Paul", "Pending", "Feb 8"],
        ],
        [2.5*inch, 1*inch, 1.2*inch, 1.2*inch]
    ))

    story.append(Paragraph("0.3 Brand Protection", styles['SubSection']))
    story.append(create_table(
        ["Task", "Owner", "Status", "Target"],
        [
            ["USPTO trademark search", "Paul", "COMPLETE", "Feb 3"],
            ["Domain availability check", "Paul", "COMPLETE", "Feb 3"],
            ["Attorney trademark search", "Jeff Johnson", "COMPLETE", "Apr 2025"],
            ["Attorney recommendation: proceed", "Jeff Johnson", "COMPLETE", "Apr 2025"],
            ["Authorize Jeff to file TM ($1,300)", "Paul + Alex", "DECISION NEEDED", "Feb 6 call"],
            ["Register domain", "Alex", "Pending", "Feb 10"],
            ["Secure social media handles", "Nathan", "Pending", "Feb 17"],
        ],
        [2.5*inch, 1*inch, 1.2*inch, 1.2*inch]
    ))

    # Trademark warning box
    story.append(Spacer(1, 10))
    story.append(create_warning_box(
        "<b>TRADEMARK UPDATE:</b> Jeff Johnson (IP Law USA) completed a professional federal search in April 2025. "
        "Found two potentially relevant marks ('Pop Top' Class 21 water bottles, 'Top Pop' Class 32 soft drinks) but "
        "<b>recommends proceeding</b> -- neither is a showstopper for beverage dispensers. "
        "Filing cost: <b>$1,300</b> (1 class). Jeff's firm has been waiting for authorization since June 2025. "
        "<b>Decision needed on Feb 6 call.</b>",
        styles
    ))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Phase 0 Gate:</b> Team committed, dashboard live, standing call running, trademark path clear", styles['Body']))

    story.append(PageBreak())

    # ─── PHASE 1 ───
    story.append(Paragraph("Phase 1: Design & Prototyping (Feb 9 - Apr 24, 2026)", styles['SectionHeader']))
    story.append(Paragraph("<b>Owners:</b> Brian Williams + Paul Giarrizzo | <b>Goal:</b> Design freeze with validated, manufacturable prototype", styles['Body']))

    story.append(Paragraph("1.1 CAD Design Completion", styles['SubSection']))
    story.append(create_table(
        ["Task", "Owner", "Target"],
        [
            ["Review existing CAD files", "Brian", "Feb 13"],
            ["Finalize V1 dimensions & capacity", "Brian", "Feb 27"],
            ["Complete SolidWorks assembly", "Brian", "Mar 13"],
            ["Design dispensing mechanism", "Brian", "Mar 20"],
            ["Design modular branding panels", "Brian", "Mar 27"],
            ["DFM review with Ross", "Brian + Ross", "Apr 3"],
            ["Create technical drawings package", "Brian", "Apr 10"],
        ],
        [3.5*inch, 1.5*inch, 1.5*inch]
    ))

    story.append(Paragraph("1.2 Prototyping", styles['SubSection']))
    story.append(create_table(
        ["Task", "Owner", "Target"],
        [
            ["Print prototype V1 (3D printer)", "Brian", "Mar 20"],
            ["Functional testing (pour, seal, clean)", "Brian + Paul", "Mar 27"],
            ["Iterate based on testing", "Brian", "Apr 3"],
            ["Print prototype V2 (refined)", "Brian", "Apr 10"],
            ["Final validation testing", "Team", "Apr 17"],
        ],
        [3.5*inch, 1.5*inch, 1.5*inch]
    ))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Phase 1 Gate:</b> Design freeze approval by all stakeholders -- <b>April 24, 2026</b>", styles['Body']))

    # ─── PHASE 2 ───
    story.append(Paragraph("Phase 2: Brand Identity & IP (Feb 6 - Apr 3, 2026)", styles['SectionHeader']))
    story.append(Paragraph("<b>Owner:</b> Paul Giarrizzo | <b>Goal:</b> Trademark filed, brand locked, digital presence secured", styles['Body']))

    story.append(Paragraph("2.1 Trademark & Brand (REQUIRES ATTORNEY REVIEW)", styles['SubSection']))
    story.append(create_table(
        ["Task", "Owner", "Target"],
        [
            ["Attorney search completed", "Jeff Johnson", "COMPLETE (Apr 2025)"],
            ["Attorney recommendation: proceed", "Jeff Johnson", "COMPLETE"],
            ["Authorize Jeff to file TM ($1,300)", "Paul + Alex", "Feb 6 call"],
            ["Trademark application filed", "Jeff Johnson", "Upon authorization"],
            ["Register domain", "Alex", "Feb 10"],
            ["Secure social media handles", "Nathan", "Feb 17"],
            ["Logo design (3 concepts)", "Paul", "Mar 13"],
            ["Logo selection & refinement", "Team", "Mar 20"],
            ["Brand style guide", "Paul", "Mar 27"],
        ],
        [3.5*inch, 1.5*inch, 1.5*inch]
    ))

    story.append(Paragraph("2.2 Legal Foundation", styles['SubSection']))
    story.append(create_table(
        ["Task", "Owner", "Target"],
        [
            ["Brian royalty agreement signed", "Paul + Brian", "Feb 13"],
            ["Entity formation (LLC)", "Paul + Alex", "Feb 27"],
            ["Operating agreement", "Paul + Alex", "Mar 6"],
            ["Patent strategy discussion", "Paul + Attorney", "Mar 13"],
            ["Provisional patent decision", "Team", "Mar 20"],
        ],
        [3.5*inch, 1.5*inch, 1.5*inch]
    ))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Phase 2 Gate:</b> Trademark filed, logo approved, brand guide complete, domain + socials live", styles['Body']))

    story.append(PageBreak())

    # ─── PHASE 3 ───
    story.append(Paragraph("Phase 3: Manufacturing & Supply Chain (Apr 24 - Jul 31, 2026)", styles['SectionHeader']))
    story.append(Paragraph("<b>Owners:</b> Ross Munn + Brian Williams | <b>Goal:</b> Manufacturer selected, T1 samples approved, production authorized", styles['Body']))

    story.append(create_table(
        ["Task", "Owner", "Target"],
        [
            ["Identify 3-5 manufacturers", "Ross", "May 8"],
            ["Send RFQ with tech drawings", "Ross + Brian", "May 15"],
            ["Evaluate quotes & capabilities", "Ross + Paul", "May 29"],
            ["Select primary manufacturer", "Team", "Jun 5"],
            ["Negotiate terms & MOQ", "Ross + Paul", "Jun 12"],
            ["Tooling deposit & kick-off", "Paul (finance)", "Jun 12"],
            ["T1 samples (first article)", "Brian + Ross", "Jul 17"],
            ["T1 approval / modifications", "Brian", "Jul 24"],
            ["Production run authorization", "Team", "Jul 31"],
            ["Packaging design + supplier", "Paul + Ross", "Jun 26 - Jul 10"],
            ["3PL evaluation & contract", "Paul", "Jul 10 - Jul 17"],
        ],
        [3.5*inch, 1.5*inch, 1.5*inch]
    ))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Phase 3 Gate:</b> T1 samples approved, production order confirmed -- <b>July 31, 2026</b>", styles['Body']))

    # ─── PHASE 4 ───
    story.append(Spacer(1, 10))
    story.append(Paragraph("Phase 4: Licensing / CLC / Fanatics (Feb 13 - Aug 7, 2026)", styles['SectionHeader']))
    story.append(Paragraph("<b>Owner:</b> Paul Giarrizzo | <b>CLC approval: 6-12 weeks after submission with final design + working prototype</b>", styles['Body']))

    story.append(create_table(
        ["Task", "Owner", "Target"],
        [
            ["Research CLC application process", "Paul", "Mar 6"],
            ["Prepare application materials", "Paul", "Apr 3"],
            ["Submit CLC application (w/ proto + DFM)", "Paul", "May 1"],
            ["CLC approval (6-12 wks from submission)", "Paul", "Jun 12 - Jul 24"],
            ["Negotiate school licenses (3-5)", "Paul", "Jun 19 - Aug 7"],
        ],
        [3.5*inch, 1.5*inch, 1.5*inch]
    ))

    story.append(Paragraph("School Selection Strategy", styles['SubSection']))
    story.append(create_table(
        ["Priority", "Schools", "Rationale"],
        [
            ["Tier 1", "Indiana, Purdue, Notre Dame", "Home state, network access"],
            ["Tier 2", "Ohio State, Michigan, Alabama", "Large fanbases, tailgate culture"],
            ["Tier 3", "SEC (LSU, Georgia, etc.)", "Premium tailgate market"],
        ],
        [1*inch, 2.75*inch, 2.75*inch]
    ))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Phase 4 Gate:</b> CLC approval + at least 3 school licenses secured (target: Jul-Aug 2026)", styles['Body']))

    story.append(PageBreak())

    # ─── PHASE 5 ───
    story.append(Paragraph("Phase 5: Go-To-Market Prep (Jun 19 - Aug 28, 2026)", styles['SectionHeader']))
    story.append(Paragraph("<b>Owners:</b> Paul Giarrizzo + Nathan Childress", styles['Body']))

    story.append(create_table(
        ["Task", "Owner", "Target"],
        [
            ["Shopify store setup", "Paul", "Jun 26"],
            ["Email capture / waitlist page", "Paul", "Jun 26"],
            ["Payment processing (Stripe)", "Paul", "Jul 3"],
            ["Product photography", "Paul", "Jul 24"],
            ["Product copy & descriptions", "Paul", "Jul 31"],
            ["Social media content calendar", "Paul + Nathan", "Jul 31"],
            ["Launch campaign strategy", "Paul", "Jul 31"],
            ["Influencer outreach list", "Nathan", "Jul 31"],
            ["PR / media list", "Paul", "Aug 7"],
            ["Pre-launch email sequence", "Paul", "Aug 14"],
            ["Waitlist goal: 1,000+ signups", "Paul + Nathan", "Aug 28"],
        ],
        [3.5*inch, 1.5*inch, 1.5*inch]
    ))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Phase 5 Gate:</b> Store live (pre-launch mode), marketing assets ready, waitlist building", styles['Body']))

    # ─── PHASE 6 ───
    story.append(Paragraph("Phase 6: Launch & Operations (Aug 7 - Nov 30, 2026)", styles['SectionHeader']))
    story.append(Paragraph("<b>Owner:</b> Full Team | <b>Goal:</b> Successful launch for 2026 College Football season", styles['Body']))

    story.append(create_table(
        ["Task", "Owner", "Target"],
        [
            ["Inventory received at 3PL", "Ross + Paul", "Aug 14"],
            ["Final QC on first units", "Brian", "Aug 18"],
            ["Soft launch (friends/family)", "Paul", "Aug 21"],
            ["Collect feedback + fix issues", "Team", "Aug 25 - 28"],
            ["Customer service setup", "Nathan", "Sep 1"],
            ["PUBLIC LAUNCH", "Paul", "SEP 1, 2026"],
            ["Social media launch push", "Nathan + Paul", "Sep 2026"],
            ["Tailgate season marketing", "Paul + Nathan", "Sep - Nov 2026"],
            ["Weekly sales reporting", "Paul", "Ongoing"],
            ["V2 feature roadmap", "Brian + Paul", "Nov 2026"],
        ],
        [3.5*inch, 1.5*inch, 1.5*inch]
    ))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Phase 6 Gate:</b> Successful launch, positive feedback, reorder trigger hit", styles['Body']))

    story.append(PageBreak())

    # ─── BRIAN'S SECTION ───
    story.append(Paragraph("Brian Williams: Engineering Scope Summary", styles['SectionHeader']))
    story.append(Paragraph("<b>Your Role:</b> Critical path owner for product development through RTM+6 months", styles['Body']))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Key Deliverables:", styles['SubSection']))
    for d in [
        "Complete SolidWorks CAD package (by Mar 13)",
        "Functional prototypes V1 + V2 (Mar 20 - Apr 10)",
        "Technical drawings for manufacturing (Apr 10)",
        "DFM collaboration with Ross (Apr 3)",
        "T1 sample validation (Jul 17-24)",
        "Production quality support",
        "Design iteration support post-launch",
    ]:
        story.append(Paragraph(f"  {d}", styles['BulletItem']))

    story.append(Spacer(1, 10))
    story.append(Paragraph("Compensation (per Product Development & Royalty Agreement):", styles['SubSection']))
    story.append(Paragraph("  Option A: 5% of net revenue for 5 years", styles['BulletItem']))
    story.append(Paragraph("  Option B: 5% of net revenue capped at $175,000", styles['BulletItem']))

    # ─── RISKS ───
    story.append(Spacer(1, 15))
    story.append(Paragraph("Critical Risks", styles['SectionHeader']))
    story.append(create_table(
        ["Risk", "Probability", "Impact", "Mitigation"],
        [
            ["Team disengagement", "Medium", "Critical", "Weekly calls, dashboard, clear ownership"],
            ["CLC approval delays (>12 wks)", "Low", "High", "Submit May 1 with complete package"],
            ["Trademark conflict", "Low-Med", "Medium", "Attorney reviewed, recommends proceeding"],
            ["Tooling delays", "Medium", "High", "Start RFQ at design freeze, buffer built in"],
            ["Capital constraints", "Medium", "Medium", "Phased spending, pre-orders"],
            ["Design iteration overruns", "Medium", "Medium", "Hard freeze Apr 24, rapid prototyping"],
            ["Aggressive timeline slip", "Medium", "High", "Weekly tracking, early escalation"],
        ],
        [1.8*inch, 0.9*inch, 0.8*inch, 3*inch]
    ))

    # ─── BUDGET ───
    story.append(Spacer(1, 15))
    story.append(Paragraph("Budget Estimates", styles['SectionHeader']))
    story.append(create_table(
        ["Category", "Estimate", "Phase"],
        [
            ["Trademark + Legal", "$4,000 - $10,000", "Phase 2"],
            ["Tooling", "$15,000 - $40,000", "Phase 3"],
            ["First Production (500 units)", "$35,000 - $50,000", "Phase 3"],
            ["Licensing Fees (CLC + schools)", "$5,000 - $15,000", "Phase 4"],
            ["E-commerce + Marketing", "$6,000 - $11,000", "Phase 5-6"],
            ["TOTAL ESTIMATED", "$65,000 - $126,000", "Phases 0-6"],
        ],
        [2.5*inch, 2*inch, 2*inch]
    ))

    story.append(Spacer(1, 10))
    story.append(Paragraph("Phased Capital Needs:", styles['SubSection']))
    story.append(create_table(
        ["Period", "Amount", "Purpose"],
        [
            ["Feb - Apr 2026", "$4K - $10K", "Trademark, legal, brand, patent"],
            ["Apr - Jul 2026", "$50K - $90K", "Tooling, first production run"],
            ["Jun - Aug 2026", "$5K - $15K", "Licensing fees"],
            ["Jun - Sep 2026", "$6K - $11K", "E-commerce, marketing"],
        ],
        [1.5*inch, 1.5*inch, 3.5*inch]
    ))

    story.append(PageBreak())

    # ─── SUCCESS METRICS ───
    story.append(Paragraph("Success Metrics", styles['SectionHeader']))
    story.append(create_table(
        ["Metric", "Target", "Measurement"],
        [
            ["RTM Date", "Before Sep 1, 2026", "Calendar"],
            ["Launch Inventory", "500+ units", "Inventory count"],
            ["School Licenses", "3-5 at launch", "License count"],
            ["Pre-launch Waitlist", "1,000+ signups", "Email list"],
            ["Launch Month Sales", "100+ units", "Shopify"],
            ["Customer Satisfaction", "4.5+ stars", "Reviews"],
            ["Football Season Sales", "500+ units (Sep-Nov)", "Shopify"],
        ],
        [2*inch, 2.25*inch, 2.25*inch]
    ))

    # ─── NEXT STEPS ───
    story.append(Spacer(1, 20))
    story.append(Paragraph("Immediate Next Steps (Next 2 Weeks)", styles['SectionHeader']))

    next_steps = [
        ("<b>Paul:</b>", [
            "Authorize Jeff Johnson to file trademark ($1,300) -- if agreed on call",
            "Share dashboard + execution plan with team",
            "Schedule recurring Wednesday call (starting Feb 11)",
            "Contact Ross separately by Feb 8",
            "Begin CLC application research",
        ]),
        ("<b>Brian:</b>", [
            "Review existing CAD files by Feb 13",
            "Confirm engineering timeline for Apr 24 design freeze",
            "Sign Product Development & Royalty Agreement",
        ]),
        ("<b>Alex:</b>", [
            "Register best available domain (drinkpoptop.com / getpoptop.com)",
            "Confirm capital availability for Phases 1-2",
        ]),
        ("<b>Ross:</b>", [
            "Begin manufacturer research (to be ready at design freeze)",
            "Identify supplier network contacts",
        ]),
        ("<b>Nathan:</b>", [
            "Set up team communication channel",
            "Secure social media handles",
        ]),
    ]

    for owner, tasks in next_steps:
        story.append(Paragraph(owner, styles['Body']))
        for task in tasks:
            story.append(Paragraph(f"  {task}", styles['BulletItem']))
        story.append(Spacer(1, 5))

    # Footer
    story.append(Spacer(1, 20))
    story.append(create_highlight_box(
        "<b>Document Status:</b> v2.1 ACTIVE | <b>Next Review:</b> Feb 6, 2026 (kickoff) then Wednesdays<br/><br/>"
        "<i>Version History:</i><br/>"
        "v1.0 (Jan 2025): Original plan, Summer 2025 target<br/>"
        "v2.0 (Feb 2025): Reset with Summer 2026 target, added Phase 0, 44-week CLC timeline<br/>"
        "v2.1 (Feb 2026): Aggressive reset -- all 2026 dates, CLC 6-12 wks post-design freeze, Sep 1 launch",
        styles
    ))

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"PDF created: {output_path}")

if __name__ == "__main__":
    build_document()
