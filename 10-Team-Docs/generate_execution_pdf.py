#!/usr/bin/env python3
"""
PopTop Execution Plan PDF Generator
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

def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(TEXT_LIGHT)
    canvas.drawCentredString(letter[0]/2, 0.5*inch, str(doc.page))
    canvas.restoreState()

def create_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name='DocTitle',
        fontName='Helvetica-Bold',
        fontSize=28,
        textColor=PRIMARY,
        alignment=TA_CENTER,
        spaceBefore=0,
        spaceAfter=15,
        leading=34,
    ))

    styles.add(ParagraphStyle(
        name='DocSubtitle',
        fontName='Helvetica',
        fontSize=14,
        textColor=TEXT_LIGHT,
        alignment=TA_CENTER,
        spaceBefore=10,
        spaceAfter=25,
        leading=18,
    ))

    styles.add(ParagraphStyle(
        name='SectionHeader',
        fontName='Helvetica-Bold',
        fontSize=16,
        textColor=PRIMARY,
        spaceBefore=20,
        spaceAfter=10,
    ))

    styles.add(ParagraphStyle(
        name='SubSection',
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=SECONDARY,
        spaceBefore=15,
        spaceAfter=8,
    ))

    styles.add(ParagraphStyle(
        name='Body',
        fontName='Helvetica',
        fontSize=10,
        textColor=TEXT,
        spaceBefore=4,
        spaceAfter=4,
        leading=14,
    ))

    styles.add(ParagraphStyle(
        name='BulletItem',
        fontName='Helvetica',
        fontSize=10,
        textColor=TEXT,
        leftIndent=20,
        spaceBefore=2,
        spaceAfter=2,
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

def build_document():
    output_path = '/Users/paulgiarrizzo/Projects/poptop/10-Team-Docs/PopTop-Execution-Plan-v1.pdf'

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    styles = create_styles()
    story = []

    # Title
    story.append(Paragraph("PopTop Execution Plan", styles['DocTitle']))
    story.append(Paragraph("NPI to RTM: Comprehensive Roadmap", styles['DocSubtitle']))

    # Meta info
    meta = [
        ["Version: 1.0", "Date: January 2025"],
        ["Target RTM: Summer 2025", "Document Owner: Paul Giarrizzo"]
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
        ["Name", "Role", "Primary Responsibilities"],
        [
            ["Alex Munn", "Co-Founder / Equity", "Strategic decisions, capital allocation"],
            ["Ross Munn", "Co-Founder / Equity", "Manufacturing sourcing, supplier relationships"],
            ["Paul Giarrizzo", "Business Lead", "Execution driver, biz dev, licensing, GTM"],
            ["Brian Williams", "Engineer", "SolidWorks CAD, prototyping, 3D printing, DFM"],
            ["Nathan Childress", "Operations", "Task execution, support across workstreams"],
        ],
        [1.5*inch, 1.5*inch, 3.5*inch]
    ))

    story.append(Spacer(1, 15))
    story.append(create_highlight_box(
        "<b>Critical Path:</b> Design Freeze → Prototype Validation → Licensing Approval → Production → Launch",
        styles
    ))

    story.append(PageBreak())

    # Phase 1
    story.append(Paragraph("Phase 1: Design & Prototyping (Weeks 1-8)", styles['SectionHeader']))
    story.append(Paragraph("<b>Owners:</b> Brian Williams + Paul Giarrizzo", styles['Body']))

    story.append(Paragraph("1.1 CAD Design Completion", styles['SubSection']))
    story.append(create_table(
        ["Task", "Owner", "Target"],
        [
            ["Finalize V1 dimensions & capacity", "Brian", "Week 2"],
            ["Complete SolidWorks assembly", "Brian", "Week 3"],
            ["Design dispensing mechanism", "Brian", "Week 4"],
            ["Design modular branding panels", "Brian", "Week 5"],
            ["DFM review", "Brian + Ross", "Week 6"],
            ["Create technical drawings package", "Brian", "Week 7"],
        ],
        [3.5*inch, 1.5*inch, 1.5*inch]
    ))

    story.append(Paragraph("1.2 Prototyping", styles['SubSection']))
    story.append(create_table(
        ["Task", "Owner", "Target"],
        [
            ["Print prototype V1 (4x4' printer)", "Brian", "Week 4"],
            ["Functional testing", "Brian + Paul", "Week 5"],
            ["Iterate based on testing", "Brian", "Week 6"],
            ["Print prototype V2 (refined)", "Brian", "Week 7"],
            ["Final validation testing", "Team", "Week 8"],
        ],
        [3.5*inch, 1.5*inch, 1.5*inch]
    ))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Phase 1 Gate:</b> Design freeze approval by all stakeholders", styles['Body']))

    story.append(PageBreak())

    # Phase 2
    story.append(Paragraph("Phase 2: Brand Identity & IP (Weeks 2-10)", styles['SectionHeader']))
    story.append(Paragraph("<b>Owner:</b> Paul Giarrizzo", styles['Body']))

    story.append(Paragraph("2.1 Trademark & Brand", styles['SubSection']))
    story.append(create_table(
        ["Task", "Owner", "Target"],
        [
            ["Finalize 'PopTop' name decision", "Team", "Week 2"],
            ["Trademark search (USPTO)", "Paul", "Week 3"],
            ["File trademark application", "Paul / Jeff Johnson", "Week 4"],
            ["Logo design (3 concepts)", "Paul", "Week 4"],
            ["Logo selection & refinement", "Team", "Week 5"],
            ["Brand style guide creation", "Paul", "Week 6"],
            ["Register domain", "Paul", "Week 3"],
            ["Secure social media handles", "Paul", "Week 3"],
        ],
        [3.5*inch, 1.5*inch, 1.5*inch]
    ))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Phase 2 Gate:</b> Trademark filed, logo approved, brand guide complete", styles['Body']))

    # Phase 3
    story.append(Paragraph("Phase 3: Manufacturing & Supply Chain (Weeks 6-16)", styles['SectionHeader']))
    story.append(Paragraph("<b>Owners:</b> Ross Munn + Brian Williams", styles['Body']))

    story.append(Paragraph("3.1 Supplier & Production", styles['SubSection']))
    story.append(create_table(
        ["Task", "Owner", "Target"],
        [
            ["Identify 3-5 potential manufacturers", "Ross", "Week 6"],
            ["Send RFQ with tech drawings", "Ross + Brian", "Week 8"],
            ["Evaluate quotes & capabilities", "Ross + Paul", "Week 10"],
            ["Select primary manufacturer", "Team", "Week 11"],
            ["Tooling deposit & kick-off", "Paul", "Week 12"],
            ["First article inspection (T1)", "Brian + Ross", "Week 16"],
            ["T1 approval / modifications", "Brian", "Week 17"],
        ],
        [3.5*inch, 1.5*inch, 1.5*inch]
    ))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Phase 3 Gate:</b> T1 samples approved, production order confirmed", styles['Body']))

    story.append(PageBreak())

    # Phase 4
    story.append(Paragraph("Phase 4: Licensing (Weeks 4-20)", styles['SectionHeader']))
    story.append(Paragraph("<b>Owner:</b> Paul Giarrizzo", styles['Body']))

    story.append(Paragraph("4.1 CLC / Fanatics Engagement", styles['SubSection']))
    story.append(create_table(
        ["Task", "Owner", "Target"],
        [
            ["Research CLC application process", "Paul", "Week 4"],
            ["Prepare licensee application", "Paul", "Week 6"],
            ["Submit CLC application", "Paul", "Week 8"],
            ["Follow-up & provide samples", "Paul", "Week 10-14"],
            ["Receive approval (est.)", "Paul", "Week 16-18"],
        ],
        [3.5*inch, 1.5*inch, 1.5*inch]
    ))

    story.append(Paragraph("4.2 School Selection Strategy", styles['SubSection']))
    story.append(create_table(
        ["Priority", "Schools", "Rationale"],
        [
            ["Tier 1", "Indiana, Purdue, Notre Dame", "Home state, network access"],
            ["Tier 2", "Ohio State, Michigan, Alabama", "Large fanbases, tailgate culture"],
            ["Tier 3", "SEC schools (LSU, Georgia)", "Premium tailgate market"],
        ],
        [1*inch, 2.75*inch, 2.75*inch]
    ))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Phase 4 Gate:</b> CLC approval + at least 3 school licenses secured", styles['Body']))

    # Phase 5
    story.append(Paragraph("Phase 5: Go-To-Market Prep (Weeks 14-22)", styles['SectionHeader']))
    story.append(Paragraph("<b>Owners:</b> Paul Giarrizzo + Nathan Childress", styles['Body']))

    story.append(create_table(
        ["Task", "Owner", "Target"],
        [
            ["Shopify store setup", "Paul", "Week 14"],
            ["Email capture / waitlist", "Paul", "Week 14"],
            ["Payment processing (Stripe)", "Paul", "Week 16"],
            ["Social media content calendar", "Paul + Nathan", "Week 16"],
            ["Product photography", "Paul", "Week 18"],
            ["Launch campaign strategy", "Paul", "Week 18"],
            ["Pre-launch email sequence", "Paul", "Week 20"],
        ],
        [3.5*inch, 1.5*inch, 1.5*inch]
    ))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Phase 5 Gate:</b> Store live (pre-launch mode), marketing assets ready", styles['Body']))

    story.append(PageBreak())

    # Phase 6
    story.append(Paragraph("Phase 6: Launch & Operations (Weeks 20-26)", styles['SectionHeader']))
    story.append(Paragraph("<b>Owner:</b> Full Team", styles['Body']))

    story.append(create_table(
        ["Task", "Owner", "Target"],
        [
            ["Inventory received at 3PL", "Ross + Paul", "Week 20"],
            ["Final QC on first units", "Brian", "Week 20"],
            ["Soft launch (friends/family)", "Paul", "Week 21"],
            ["Public launch announcement", "Paul", "Week 22"],
            ["Social media push", "Nathan + Paul", "Week 22-24"],
            ["Customer service setup", "Nathan", "Week 22"],
            ["Weekly sales reporting", "Paul", "Ongoing"],
        ],
        [3.5*inch, 1.5*inch, 1.5*inch]
    ))

    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>Phase 6 Gate:</b> Successful launch, positive feedback, reorder trigger hit", styles['Body']))

    # Brian's Section
    story.append(Spacer(1, 20))
    story.append(Paragraph("Brian Williams: Engineering Scope Summary", styles['SectionHeader']))

    story.append(Paragraph("<b>Your Role:</b> Critical path owner for product development through RTM+6 months", styles['Body']))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Key Deliverables:", styles['SubSection']))
    deliverables = [
        "Complete SolidWorks CAD package",
        "Functional prototypes (V1, V2)",
        "Technical drawings for manufacturing",
        "DFM collaboration with manufacturer",
        "T1 sample validation",
        "Production quality support",
    ]
    for d in deliverables:
        story.append(Paragraph(f"• {d}", styles['BulletItem']))

    story.append(Spacer(1, 10))
    story.append(Paragraph("Compensation (per Agreement):", styles['SubSection']))
    story.append(Paragraph("• Option A: 5% of net revenue for 5 years", styles['BulletItem']))
    story.append(Paragraph("• Option B: 5% of net revenue capped at $175,000", styles['BulletItem']))

    story.append(PageBreak())

    # Budget
    story.append(Paragraph("Budget Estimates (High-Level)", styles['SectionHeader']))
    story.append(create_table(
        ["Category", "Estimate", "Notes"],
        [
            ["Tooling", "$15,000 - $40,000", "Depends on complexity"],
            ["First Production (500 units)", "$35,000 - $50,000", "~$70-100/unit"],
            ["Trademark Filing", "$1,500 - $3,000", "With attorney"],
            ["Licensing Fees", "$5,000 - $15,000", "CLC + school fees"],
            ["Marketing Launch", "$5,000 - $10,000", "Initial campaign"],
            ["E-commerce Setup", "$500 - $1,000", "Shopify + apps"],
            ["TOTAL ESTIMATED", "$62,000 - $119,000", "Phase 1-6"],
        ],
        [2*inch, 1.75*inch, 2.75*inch]
    ))

    # Success Metrics
    story.append(Spacer(1, 20))
    story.append(Paragraph("Success Metrics", styles['SectionHeader']))
    story.append(create_table(
        ["Metric", "Target", "Measurement"],
        [
            ["RTM Date", "Before August 2025", "Calendar"],
            ["Launch Inventory", "500+ units", "Inventory count"],
            ["School Licenses", "3-5 at launch", "License count"],
            ["Pre-launch Waitlist", "1,000+ signups", "Email list"],
            ["Launch Week Sales", "50+ units", "Shopify"],
            ["Customer Satisfaction", "4.5+ stars", "Reviews"],
        ],
        [2*inch, 2.25*inch, 2.25*inch]
    ))

    # Immediate Next Steps
    story.append(Spacer(1, 20))
    story.append(Paragraph("Immediate Next Steps (Next 2 Weeks)", styles['SectionHeader']))

    next_steps = [
        ("<b>Paul:</b>", ["Finalize execution plan", "Set up project dashboard", "Schedule weekly sync", "Begin trademark search"]),
        ("<b>Brian:</b>", ["Review engineering timeline", "Begin/continue SolidWorks", "Identify design questions"]),
        ("<b>Ross:</b>", ["Begin manufacturer research", "Identify supplier contacts"]),
        ("<b>Nathan:</b>", ["Review assigned tasks", "Set up communication channels"]),
    ]

    for owner, tasks in next_steps:
        story.append(Paragraph(owner, styles['Body']))
        for task in tasks:
            story.append(Paragraph(f"  • {task}", styles['BulletItem']))
        story.append(Spacer(1, 5))

    # Footer
    story.append(Spacer(1, 30))
    story.append(create_highlight_box(
        "<i>\"The best time to plant a tree was 20 years ago. The second best time is now.\"</i><br/><br/><b>Let's build something great.</b>",
        styles
    ))

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"PDF created: {output_path}")

if __name__ == "__main__":
    build_document()
