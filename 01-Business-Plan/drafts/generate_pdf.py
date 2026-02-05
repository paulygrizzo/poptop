#!/usr/bin/env python3
"""
PopTop Business Plan PDF Generator
Generates a professionally styled PDF business plan using ReportLab
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, ListFlowable, ListItem, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.platypus.flowables import Flowable
import os

# Color scheme
PRIMARY = HexColor('#1a365d')
SECONDARY = HexColor('#c9a227')
ACCENT = HexColor('#2d3748')
LIGHT = HexColor('#f7fafc')
TEXT = HexColor('#2d3748')
TEXT_LIGHT = HexColor('#718096')

class ColoredBox(Flowable):
    """A colored box with text inside"""
    def __init__(self, width, height, color, text="", text_color=white):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.text_color = text_color

    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.roundRect(0, 0, self.width, self.height, 5, fill=1, stroke=0)

class MetricCard(Flowable):
    """A metric card with value and label"""
    def __init__(self, value, label, width=1.5*inch, height=0.8*inch):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.value = value
        self.label = label

    def draw(self):
        # Background
        self.canv.setFillColor(LIGHT)
        self.canv.roundRect(0, 0, self.width, self.height, 3, fill=1, stroke=0)
        # Left border
        self.canv.setFillColor(SECONDARY)
        self.canv.rect(0, 0, 3, self.height, fill=1, stroke=0)
        # Value
        self.canv.setFillColor(PRIMARY)
        self.canv.setFont("Helvetica-Bold", 14)
        self.canv.drawCentredString(self.width/2, self.height - 25, self.value)
        # Label
        self.canv.setFillColor(TEXT_LIGHT)
        self.canv.setFont("Helvetica", 7)
        self.canv.drawCentredString(self.width/2, 8, self.label.upper())

def create_cover_page(canvas, doc):
    """Draw the cover page"""
    canvas.saveState()

    # Blue gradient background
    canvas.setFillColor(PRIMARY)
    canvas.rect(0, 0, letter[0], letter[1], fill=1, stroke=0)

    # Logo - draw "Pop" and "Top" side by side, properly spaced
    canvas.setFont("Helvetica-Bold", 60)
    # Calculate widths to center the full "PopTop" text
    pop_width = canvas.stringWidth("Pop", "Helvetica-Bold", 60)
    top_width = canvas.stringWidth("Top", "Helvetica-Bold", 60)
    total_width = pop_width + top_width
    start_x = (letter[0] - total_width) / 2

    canvas.setFillColor(white)
    canvas.drawString(start_x, letter[1] - 3*inch, "Pop")
    canvas.setFillColor(SECONDARY)
    canvas.drawString(start_x + pop_width, letter[1] - 3*inch, "Top")

    # Subtitle
    canvas.setFillColor(white)
    canvas.setFont("Helvetica", 12)
    canvas.drawCentredString(letter[0]/2, letter[1] - 3.5*inch, "BUSINESS PLAN")

    # Tagline
    canvas.setFillColor(SECONDARY)
    canvas.setFont("Helvetica-Oblique", 16)
    canvas.drawCentredString(letter[0]/2, letter[1] - 4.5*inch, '"The Centerpiece of Your Tailgate"')

    # Meta info
    canvas.setFillColor(white)
    canvas.setFont("Helvetica", 10)
    y_pos = 3.5*inch
    meta = [
        "Company: PopTop, LLC (a Munn Family Holdings company)",
        "Jurisdiction: Indiana LLC",
        "Stage: Prototype → Pre-Launch",
        "Target RTM: Summer 2025",
        "Version: 1.0 | January 2025"
    ]
    for line in meta:
        canvas.drawCentredString(letter[0]/2, y_pos, line)
        y_pos -= 20

    canvas.restoreState()

def add_page_number(canvas, doc):
    """Add page number to each page"""
    if doc.page > 1:  # Skip cover page
        canvas.saveState()
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(TEXT_LIGHT)
        canvas.drawCentredString(letter[0]/2, 0.5*inch, str(doc.page - 1))
        canvas.restoreState()

def create_styles():
    """Create custom paragraph styles"""
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name='SectionTitle',
        fontName='Helvetica-Bold',
        fontSize=24,
        textColor=PRIMARY,
        spaceBefore=20,
        spaceAfter=12,
        borderPadding=(0, 0, 5, 0),
    ))

    styles.add(ParagraphStyle(
        name='SubsectionTitle',
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=PRIMARY,
        spaceBefore=15,
        spaceAfter=8,
        textTransform='uppercase',
    ))

    styles.add(ParagraphStyle(
        name='CustomBody',
        fontName='Helvetica',
        fontSize=10,
        textColor=TEXT,
        spaceBefore=6,
        spaceAfter=6,
        leading=14,
        alignment=TA_JUSTIFY,
    ))

    # Override default BodyText
    styles['BodyText'].fontName = 'Helvetica'
    styles['BodyText'].fontSize = 10
    styles['BodyText'].textColor = TEXT
    styles['BodyText'].leading = 14

    styles.add(ParagraphStyle(
        name='HighlightTitle',
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=SECONDARY,
        spaceBefore=0,
        spaceAfter=8,
    ))

    styles.add(ParagraphStyle(
        name='HighlightBody',
        fontName='Helvetica',
        fontSize=10,
        textColor=white,
        leading=14,
    ))

    styles.add(ParagraphStyle(
        name='BulletText',
        fontName='Helvetica',
        fontSize=10,
        textColor=TEXT,
        leftIndent=20,
        spaceBefore=3,
        spaceAfter=3,
    ))

    styles.add(ParagraphStyle(
        name='TableHeader',
        fontName='Helvetica-Bold',
        fontSize=9,
        textColor=white,
    ))

    styles.add(ParagraphStyle(
        name='TableCell',
        fontName='Helvetica',
        fontSize=9,
        textColor=TEXT,
    ))

    styles.add(ParagraphStyle(
        name='CenteredQuote',
        fontName='Helvetica-Oblique',
        fontSize=14,
        textColor=PRIMARY,
        alignment=TA_CENTER,
        spaceBefore=10,
        spaceAfter=10,
    ))

    return styles

def create_highlight_box(title, content, styles):
    """Create a highlighted box with title and content"""
    data = [[
        Paragraph(f'<font color="#{SECONDARY.hexval()[2:]}">{title}</font>', styles['HighlightTitle']),
    ], [
        Paragraph(content, styles['HighlightBody'])
    ]]

    t = Table(data, colWidths=[6.5*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), PRIMARY),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
        ('ROUNDEDCORNERS', [5, 5, 5, 5]),
    ]))
    return t

def create_metrics_row(metrics, styles):
    """Create a row of metric cards"""
    data = [[]]
    for value, label in metrics:
        cell_content = f'''<para align="center">
            <font size="16" color="#{PRIMARY.hexval()[2:]}"><b>{value}</b></font><br/>
            <font size="7" color="#{TEXT_LIGHT.hexval()[2:]}">{label.upper()}</font>
        </para>'''
        data[0].append(Paragraph(cell_content, styles['BodyText']))

    t = Table(data, colWidths=[1.625*inch] * len(metrics))
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('LINEBEFORESTARTPADDING', (0, 0), (-1, -1), 0),
        ('LINEBEFORE', (0, 0), (0, -1), 3, SECONDARY),
        ('LINEBEFORE', (1, 0), (1, -1), 3, SECONDARY),
        ('LINEBEFORE', (2, 0), (2, -1), 3, SECONDARY),
        ('LINEBEFORE', (3, 0), (3, -1), 3, SECONDARY),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return t

def create_data_table(headers, rows, col_widths=None):
    """Create a styled data table"""
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
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT]),
        ('LINEBELOW', (0, 0), (-1, -2), 0.5, HexColor('#e2e8f0')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    return t

def build_document():
    """Build the complete PDF document"""
    output_path = '/Users/paulgiarrizzo/Projects/poptop/01-Business-Plan/final/PopTop-Business-Plan-v1.pdf'

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

    # Cover page placeholder (handled separately)
    story.append(PageBreak())

    # ========== EXECUTIVE SUMMARY ==========
    story.append(Paragraph("01 Executive Summary", styles['SectionTitle']))
    story.append(Spacer(1, 5))

    # Gold line under title
    line_data = [['']]
    line_table = Table(line_data, colWidths=[6.5*inch], rowHeights=[3])
    line_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), SECONDARY)]))
    story.append(line_table)
    story.append(Spacer(1, 15))

    story.append(Paragraph(
        "PopTop is a consumer products company building a <b>premium, category-defining beverage "
        "dispensing platform</b> engineered specifically for collegiate sports tailgating and "
        "fan-centered social experiences.",
        styles['BodyText']
    ))

    story.append(Spacer(1, 15))
    story.append(create_metrics_row([
        ("$375", "Target MSRP"),
        ("60-65%", "Gross Margin"),
        ("$10-20M", "Initial SOM"),
        ("$500M+", "Total TAM"),
    ], styles))
    story.append(Spacer(1, 15))

    story.append(Paragraph(
        "The Company's flagship product is a high-capacity, portable, and visually distinctive "
        "drink dispenser designed to serve as the functional and social centerpiece of tailgates, "
        "watch parties, and outdoor fan gatherings. Unlike generic beverage dispensers, PopTop "
        "products are purpose-built for licensed collegiate branding, durability, and repeat use "
        "in demanding outdoor environments.",
        styles['BodyText']
    ))

    story.append(Spacer(1, 15))
    story.append(create_highlight_box(
        "Strategic Vision",
        "PopTop is designed from inception as a <b>brand and platform company</b>, not a single-SKU "
        "novelty product. The long-term objective is to become the dominant and trusted name in "
        "premium beverage dispensing for social and fan-driven environments.",
        styles
    ))

    story.append(Spacer(1, 15))
    story.append(Paragraph("GO-TO-MARKET STRATEGY", styles['SubsectionTitle']))
    story.append(Paragraph(
        "Establish a strong beachhead in collegiate athletics through direct-to-consumer sales "
        "and strategic licensing partnerships (CLC and Fanatics), then expand into additional "
        "product variants and adjacent markets including professional sports, outdoor lifestyle, "
        "hospitality, and events.",
        styles['BodyText']
    ))

    story.append(PageBreak())

    # ========== PROBLEM & OPPORTUNITY ==========
    story.append(Paragraph("02 Problem & Opportunity", styles['SectionTitle']))
    story.append(Spacer(1, 5))
    line_table = Table([['']], colWidths=[6.5*inch], rowHeights=[3])
    line_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), SECONDARY)]))
    story.append(line_table)
    story.append(Spacer(1, 15))

    story.append(Paragraph("THE PROBLEM", styles['SubsectionTitle']))
    story.append(Paragraph(
        "Despite significant consumer spending on tailgating and fan gear, the beverage dispensing "
        "category remains fragmented, commoditized, and underserved. Existing options fall into "
        "three categories:",
        styles['BodyText']
    ))

    bullets = [
        "<b>Low-cost plastic dispensers</b> lacking durability, aesthetic appeal, and temperature performance",
        "<b>Novelty/keg-style products</b> difficult to transport, clean, or brand consistently",
        "<b>Improvised solutions</b> (coolers, tubs, cans) that don't scale for group use",
    ]
    for bullet in bullets:
        story.append(Paragraph(f"• {bullet}", styles['BulletText']))

    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "None of these solutions are designed with <b>collegiate fandom</b>, <b>licensed branding</b>, "
        "or <b>premium ownership experience</b> as core design requirements. There is no dominant brand "
        "in beverage dispensing analogous to YETI's position in coolers.",
        styles['BodyText']
    ))

    story.append(Spacer(1, 10))
    story.append(Paragraph("THE OPPORTUNITY", styles['SubsectionTitle']))
    story.append(Paragraph(
        "Collegiate sports fandom represents one of the most passionate and ritual-driven consumer "
        "segments in the United States. Tailgating is central to the experience and often represents "
        "a multi-decade tradition for alumni and fans.",
        styles['BodyText']
    ))

    story.append(Spacer(1, 15))
    story.append(create_metrics_row([
        ("130+", "FBS Programs"),
        ("Millions", "Engaged Fans"),
        ("Premium", "Spending Trend"),
        ("High", "Brand Loyalty"),
    ], styles))

    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "PopTop addresses this gap by offering a premium, licensed, and extensible beverage "
        "dispensing solution that elevates the social experience while reinforcing fan identity.",
        styles['BodyText']
    ))

    story.append(PageBreak())

    # ========== PRODUCT OVERVIEW ==========
    story.append(Paragraph("03 Product Overview", styles['SectionTitle']))
    story.append(Spacer(1, 5))
    line_table = Table([['']], colWidths=[6.5*inch], rowHeights=[3])
    line_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), SECONDARY)]))
    story.append(line_table)
    story.append(Spacer(1, 15))

    story.append(Paragraph("FLAGSHIP PRODUCT (V1)", styles['SubsectionTitle']))
    story.append(Paragraph(
        "A rugged, tabletop/portable drink dispenser designed specifically for tailgates and group events.",
        styles['BodyText']
    ))

    story.append(Paragraph("Core Features:", styles['SubsectionTitle']))
    features = [
        "Durable, food-grade materials",
        "High-capacity reservoir (optimized for group use)",
        "Controlled pour / tap-style dispensing",
        "Modular branding surfaces (team logos, colors)",
        "Designed for ice compatibility",
        "Portable, easy-clean construction",
    ]
    for f in features:
        story.append(Paragraph(f"• {f}", styles['BulletText']))

    story.append(Spacer(1, 15))
    story.append(Paragraph("Target Economics:", styles['SubsectionTitle']))
    story.append(create_data_table(
        ["Metric", "Value"],
        [
            ["MSRP", "$350 - $400"],
            ["Target ASP", "$375"],
            ["Est. COGS", "~$140/unit"],
            ["Gross Margin", "60 - 65%"],
        ],
        [3.25*inch, 3.25*inch]
    ))

    story.append(Spacer(1, 15))
    story.append(Paragraph("PRODUCT ROADMAP", styles['SubsectionTitle']))
    story.append(create_data_table(
        ["Version", "Description", "Key Features"],
        [
            ["V1", "Flagship Launch", "Core dispenser with ice compatibility"],
            ["V2", "Insulated/Refrigerated", "Enhanced temperature retention"],
            ["V3", "Electric-Powered", "AC outlet powered cooling"],
            ["V4", "Battery-Powered", "Portable cooling system"],
            ["V5", "Smart Dispensing", "Volume tracking, app integration"],
            ["V6", "Commercial/Hospitality", "High-volume, venue-grade"],
        ],
        [0.8*inch, 1.8*inch, 3.9*inch]
    ))

    story.append(Spacer(1, 15))
    story.append(create_highlight_box(
        "Platform Philosophy",
        "PopTop is intentionally engineered as a <b>platform</b>, not a one-off product. Each "
        "version builds on core IP while expanding addressable markets and use cases.",
        styles
    ))

    story.append(PageBreak())

    # ========== MARKET ANALYSIS ==========
    story.append(Paragraph("04 Market Analysis", styles['SectionTitle']))
    story.append(Spacer(1, 5))
    line_table = Table([['']], colWidths=[6.5*inch], rowHeights=[3])
    line_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), SECONDARY)]))
    story.append(line_table)
    story.append(Spacer(1, 15))

    story.append(Paragraph("TARGET CUSTOMER PROFILE", styles['SubsectionTitle']))

    # Two column table for demographics
    demo_data = [
        [Paragraph("<b>Primary Demographics</b>", styles['BodyText']),
         Paragraph("<b>Psychographics</b>", styles['BodyText'])],
        [Paragraph("• Collegiate sports fans and alumni<br/>• Tailgaters and watch-party hosts<br/>• Booster clubs and alumni associations<br/>• Age range: 25-60<br/>• Middle to upper-middle income", styles['BulletText']),
         Paragraph("• Value quality and durability<br/>• Strong brand/team alignment<br/>• Social signaling conscious<br/>• Repeat purchasers of premium fan gear<br/>• Multi-generational traditions", styles['BulletText'])]
    ]
    demo_table = Table(demo_data, colWidths=[3.25*inch, 3.25*inch])
    demo_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(demo_table)

    story.append(Spacer(1, 15))
    story.append(Paragraph("PRIMARY MARKET: COLLEGIATE ATHLETICS", styles['SubsectionTitle']))
    story.append(Paragraph(
        "Initial focus on U.S. collegiate athletics, beginning with flagship programs and conferences "
        "where tailgating culture and discretionary spending are highest:",
        styles['BodyText']
    ))
    for item in ["Power 5 conferences (SEC, Big Ten, Big 12, ACC, Pac-12)",
                 "Major football and basketball programs",
                 "Schools with strong licensing ecosystems"]:
        story.append(Paragraph(f"• {item}", styles['BulletText']))

    story.append(Spacer(1, 15))
    story.append(Paragraph("SECONDARY & EXPANSION MARKETS", styles['SubsectionTitle']))
    story.append(create_data_table(
        ["Market", "Opportunity", "Timeline"],
        [
            ["Professional Sports", "NFL, MLB, NBA, NHL fanbases", "Year 2-3"],
            ["Outdoor/Lifestyle", "Camping, RV, overlanding", "Year 2-3"],
            ["Corporate Events", "Branded hospitality", "Year 3+"],
            ["Venue/Hospitality", "Event rentals, stadiums", "Year 3+"],
        ],
        [2*inch, 2.75*inch, 1.75*inch]
    ))

    story.append(Spacer(1, 15))
    story.append(Paragraph("MARKET SIZING", styles['SubsectionTitle']))
    story.append(create_metrics_row([
        ("~130", "FBS Programs"),
        ("0.25%", "Initial Penetration"),
        ("$10-20M", "Initial SOM"),
        ("$500M+", "Total TAM"),
    ], styles))

    story.append(PageBreak())

    # ========== COMPETITIVE LANDSCAPE ==========
    story.append(Paragraph("05 Competitive Landscape", styles['SectionTitle']))
    story.append(Spacer(1, 5))
    line_table = Table([['']], colWidths=[6.5*inch], rowHeights=[3])
    line_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), SECONDARY)]))
    story.append(line_table)
    story.append(Spacer(1, 15))

    comp_data = [
        [Paragraph("<b>Direct Competitors</b>", styles['BodyText']),
         Paragraph("<b>Competitive Advantages</b>", styles['BodyText'])],
        [Paragraph("• Generic drink dispensers (Amazon, big-box)<br/>• Keg-style novelty products<br/>• Basic plastic dispensers<br/><br/><b>Indirect Competitors</b><br/>• Premium coolers (YETI, Igloo)<br/>• Party beverage tubs<br/>• DIY/improvised solutions", styles['BulletText']),
         Paragraph("• <b>Purpose-built</b> for tailgating use case<br/>• <b>Premium design</b> & materials<br/>• <b>Licensed collegiate branding</b><br/>• <b>Platform extensibility</b><br/>• <b>Strong brand narrative</b><br/>• <b>First-mover</b> in category", styles['BulletText'])]
    ]
    comp_table = Table(comp_data, colWidths=[3.25*inch, 3.25*inch])
    comp_table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP')]))
    story.append(comp_table)

    story.append(Spacer(1, 15))
    story.append(create_highlight_box(
        "Strategic Position",
        "<b>No incumbent brand owns this category.</b> PopTop has the opportunity to establish "
        "category leadership similar to how YETI defined premium coolers. The combination of "
        "licensed branding + premium construction + tailgate-specific design creates a defensible moat.",
        styles
    ))

    story.append(Spacer(1, 15))
    story.append(Paragraph("COMPETITIVE MATRIX", styles['SubsectionTitle']))
    story.append(create_data_table(
        ["Factor", "Generic", "Novelty", "YETI/Coolers", "PopTop"],
        [
            ["Build Quality", "Low", "Low-Med", "High", "High"],
            ["Collegiate Licensing", "None", "Limited", "Some", "Core"],
            ["Tailgate-Specific", "No", "Partial", "No", "Yes"],
            ["Price Point", "$20-50", "$50-150", "$200-400", "$350-400"],
            ["Brand Premium", "None", "Low", "High", "High"],
        ],
        [1.5*inch, 1.1*inch, 1.1*inch, 1.4*inch, 1.4*inch]
    ))

    story.append(PageBreak())

    # ========== LICENSING & PARTNERSHIPS ==========
    story.append(Paragraph("06 Licensing & Partnerships", styles['SectionTitle']))
    story.append(Spacer(1, 5))
    line_table = Table([['']], colWidths=[6.5*inch], rowHeights=[3])
    line_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), SECONDARY)]))
    story.append(line_table)
    story.append(Spacer(1, 15))

    story.append(Paragraph("LICENSING STRATEGY", styles['SubsectionTitle']))
    story.append(Paragraph(
        "Collegiate licensing is central to PopTop's value proposition and competitive moat. "
        "Licensed products command premium pricing and create emotional connection with consumers.",
        styles['BodyText']
    ))

    story.append(Spacer(1, 10))
    phase_data = [
        [Paragraph("<b>Phase 1: Foundation</b>", styles['BodyText']),
         Paragraph("<b>Phase 2: Expansion</b>", styles['BodyText']),
         Paragraph("<b>Phase 3: Scale</b>", styles['BodyText'])],
        [Paragraph("• Establish CLC relationship<br/>• Fanatics partnership<br/>• 3-5 flagship programs", styles['BulletText']),
         Paragraph("• Power 5 conferences<br/>• Top 25 programs<br/>• Regional expansion", styles['BulletText']),
         Paragraph("• Full FBS coverage<br/>• Pro sports leagues<br/>• International", styles['BulletText'])]
    ]
    phase_table = Table(phase_data, colWidths=[2.17*inch, 2.17*inch, 2.17*inch])
    phase_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(phase_table)

    story.append(Spacer(1, 15))
    story.append(Paragraph("STRATEGIC PARTNERS (TARGET)", styles['SubsectionTitle']))
    story.append(create_data_table(
        ["Partner", "Type", "Value"],
        [
            ["Fanatics", "Distribution & Licensing", "Access to 300M+ customers, licensing infrastructure"],
            ["CLC", "Licensing Agent", "200+ university relationships"],
            ["Campus Bookstores", "Retail Channel", "Direct access to students/alumni"],
            ["Stadium Operators", "Retail/Events", "High-traffic game day exposure"],
        ],
        [1.5*inch, 1.75*inch, 3.25*inch]
    ))

    story.append(Spacer(1, 15))
    story.append(create_highlight_box(
        "Licensing as a Moat",
        "Licensing is a <b>moat, not a tax</b>. PopTop becomes a preferred platform partner rather "
        "than a one-off licensed item. Deep licensing relationships create barriers to entry for "
        "competitors and drive recurring revenue through new school additions.",
        styles
    ))

    story.append(PageBreak())

    # ========== GO-TO-MARKET STRATEGY ==========
    story.append(Paragraph("07 Go-To-Market Strategy", styles['SectionTitle']))
    story.append(Spacer(1, 5))
    line_table = Table([['']], colWidths=[6.5*inch], rowHeights=[3])
    line_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), SECONDARY)]))
    story.append(line_table)
    story.append(Spacer(1, 15))

    story.append(Paragraph("PHASED APPROACH", styles['SubsectionTitle']))
    gtm_data = [
        [Paragraph("<b>Phase 1: D2C</b>", styles['BodyText']),
         Paragraph("<b>Phase 2: Wholesale</b>", styles['BodyText']),
         Paragraph("<b>Phase 3: Enterprise</b>", styles['BodyText'])],
        [Paragraph("• PopTop.com launch<br/>• Limited school drops<br/>• Pre-orders / waitlists<br/>• Scarcity-driven launches", styles['BulletText']),
         Paragraph("• Fanatics integration<br/>• Campus bookstores<br/>• Sporting goods retailers<br/>• Regional chains", styles['BulletText']),
         Paragraph("• Alumni associations<br/>• Corporate tailgates<br/>• Event rentals<br/>• Venue partnerships", styles['BulletText'])]
    ]
    gtm_table = Table(gtm_data, colWidths=[2.17*inch, 2.17*inch, 2.17*inch])
    gtm_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(gtm_table)

    story.append(Spacer(1, 15))
    story.append(Paragraph("MARKETING STRATEGY", styles['SubsectionTitle']))
    story.append(Paragraph(
        "Marketing is <b>visual, experiential, and social-first</b>. The product should photograph "
        "exceptionally well and feel iconic when present at the tailgate.",
        styles['BodyText']
    ))

    mkt_data = [
        [Paragraph("<b>Channels</b>", styles['BodyText']),
         Paragraph("<b>Tactics</b>", styles['BodyText'])],
        [Paragraph("• Instagram / TikTok (lifestyle content)<br/>• Game day photography<br/>• Influencer partnerships<br/>• Alumni network activations<br/>• Stadium/event presence", styles['BulletText']),
         Paragraph("• Limited edition drops by school<br/>• Early access for alumni groups<br/>• User-generated content campaigns<br/>• Rivalry week promotions<br/>• Championship tie-ins", styles['BulletText'])]
    ]
    mkt_table = Table(mkt_data, colWidths=[3.25*inch, 3.25*inch])
    mkt_table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP')]))
    story.append(mkt_table)

    story.append(Spacer(1, 15))
    story.append(Paragraph("LAUNCH TIMELINE", styles['SubsectionTitle']))
    story.append(create_data_table(
        ["Milestone", "Target", "Focus"],
        [
            ["Prototype Complete", "Q1 2025", "Engineering validation"],
            ["Licensing Secured", "Q2 2025", "Initial school agreements"],
            ["Production Run", "Q2-Q3 2025", "Manufacturing at scale"],
            ["RTM Launch", "Summer 2025", "Pre-football season"],
        ],
        [2.17*inch, 2.17*inch, 2.17*inch]
    ))

    story.append(PageBreak())

    # ========== BRAND & POSITIONING ==========
    story.append(Paragraph("08 Brand & Positioning", styles['SectionTitle']))
    story.append(Spacer(1, 5))
    line_table = Table([['']], colWidths=[6.5*inch], rowHeights=[3])
    line_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), SECONDARY)]))
    story.append(line_table)
    story.append(Spacer(1, 15))

    story.append(Paragraph("BRAND ATTRIBUTES", styles['SubsectionTitle']))
    story.append(create_metrics_row([
        ("Bold", "Commanding Presence"),
        ("Premium", "Quality & Craft"),
        ("Social", "Community Focused"),
        ("Tradition", "Built to Last"),
    ], styles))

    story.append(Spacer(1, 20))
    story.append(create_highlight_box(
        "Brand Positioning",
        '<para align="center"><font size="16"><i>"The Centerpiece of Your Tailgate"</i></font></para>',
        styles
    ))

    story.append(Spacer(1, 15))
    story.append(Paragraph("BRAND PROMISE", styles['SubsectionTitle']))
    story.append(Paragraph(
        "PopTop products are designed to be the functional and social centerpiece of every tailgate. "
        "When you show up with a PopTop, you're not just bringing drinks - you're bringing the party. "
        "The product should photograph exceptionally well and feel iconic when present for the big game.",
        styles['BodyText']
    ))

    story.append(Spacer(1, 15))
    brand_data = [
        [Paragraph("<b>Design Principles</b>", styles['BodyText']),
         Paragraph("<b>Brand Voice</b>", styles['BodyText'])],
        [Paragraph("• Clean, modern aesthetics<br/>• Premium material finishes<br/>• Bold, visible branding<br/>• Modular customization<br/>• Instagram-worthy design", styles['BulletText']),
         Paragraph("• Confident but not arrogant<br/>• Fun but not frivolous<br/>• Premium but accessible<br/>• Tradition-honoring<br/>• Community-building", styles['BulletText'])]
    ]
    brand_table = Table(brand_data, colWidths=[3.25*inch, 3.25*inch])
    brand_table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP')]))
    story.append(brand_table)

    story.append(PageBreak())

    # ========== OPERATIONS & MANUFACTURING ==========
    story.append(Paragraph("09 Operations & Manufacturing", styles['SectionTitle']))
    story.append(Spacer(1, 5))
    line_table = Table([['']], colWidths=[6.5*inch], rowHeights=[3])
    line_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), SECONDARY)]))
    story.append(line_table)
    story.append(Spacer(1, 15))

    story.append(Paragraph("PRODUCT DEVELOPMENT STATUS", styles['SubsectionTitle']))
    for item in ["Initial concept and product requirements defined",
                 "CAD design and engineering underway (SolidWorks)",
                 "Prototyping utilizing in-house 4'x4' 3D printing capability"]:
        story.append(Paragraph(f"• {item}", styles['BulletText']))
    story.append(Paragraph(
        "Design philosophy emphasizes <b>durability, manufacturability, modularity, and licensing compliance</b>.",
        styles['BodyText']
    ))

    story.append(Spacer(1, 15))
    story.append(Paragraph("MANUFACTURING STRATEGY", styles['SubsectionTitle']))
    mfg_data = [
        [Paragraph("<b>Phase 1: Pilot</b>", styles['BodyText']),
         Paragraph("<b>Phase 2: Scaled</b>", styles['BodyText']),
         Paragraph("<b>Phase 3: Full Scale</b>", styles['BodyText'])],
        [Paragraph("• Low-volume runs<br/>• Domestic/near-shore mfg<br/>• Rapid iteration<br/>• Field testing", styles['BulletText']),
         Paragraph("• Overseas partners<br/>• US-based QC<br/>• Tooling investment<br/>• Volume pricing", styles['BulletText']),
         Paragraph("• Multiple SKUs<br/>• Regional distribution<br/>• Inventory optimization<br/>• JIT fulfillment", styles['BulletText'])]
    ]
    mfg_table = Table(mfg_data, colWidths=[2.17*inch, 2.17*inch, 2.17*inch])
    mfg_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(mfg_table)

    story.append(Spacer(1, 15))
    story.append(Paragraph("SUPPLY CHAIN & RISKS", styles['SubsectionTitle']))
    story.append(create_data_table(
        ["Area", "Approach / Mitigation"],
        [
            ["Materials", "Food-grade sourcing with supplier redundancy"],
            ["Packaging", "Designed for eCommerce shipping, premium unboxing"],
            ["Inventory", "Aligned with seasonal demand (football season)"],
            ["Tooling Delays", "Early engagement, parallel development"],
            ["Licensing Delays", "Multiple school pipeline, early submission"],
        ],
        [2*inch, 4.5*inch]
    ))

    story.append(PageBreak())

    # ========== TEAM & ADVISORS ==========
    story.append(Paragraph("10 Team & Advisors", styles['SectionTitle']))
    story.append(Spacer(1, 5))
    line_table = Table([['']], colWidths=[6.5*inch], rowHeights=[3])
    line_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), SECONDARY)]))
    story.append(line_table)
    story.append(Spacer(1, 15))

    story.append(Paragraph("CORE TEAM", styles['SubsectionTitle']))
    story.append(create_data_table(
        ["Role", "Name", "Responsibility"],
        [
            ["Founders / Equity Holders", "Alex Munn, Ross Munn", "LLC ownership, strategic direction"],
            ["Business Lead", "Paul Giarrizzo", "Business plan, execution strategy, operations"],
            ["Engineering", "Brian Williams", "SolidWorks CAD, 3D printing, prototyping"],
            ["Operations", "Nathan Childress", "Team member, execution support"],
        ],
        [1.75*inch, 1.75*inch, 3*inch]
    ))

    story.append(Spacer(1, 15))
    story.append(Paragraph("EXTERNAL PARTNERS", styles['SubsectionTitle']))
    story.append(create_data_table(
        ["Function", "Partner"],
        [
            ["Legal / IP", "Jeff Johnson (IP Law USA)"],
        ],
        [2*inch, 4.5*inch]
    ))

    story.append(Spacer(1, 15))
    story.append(Paragraph("TARGET ADVISORS", styles['SubsectionTitle']))
    for item in ["eCommerce distribution executive",
                 "Licensing specialist (collegiate/pro sports)",
                 "Consumer hardware scaling operator"]:
        story.append(Paragraph(f"• {item}", styles['BulletText']))

    story.append(Spacer(1, 15))
    story.append(create_highlight_box(
        "Team Strengths",
        "The team combines <b>entrepreneurial drive</b> with <b>engineering capability</b> and "
        "<b>business acumen</b>. In-house 3D printing capability (4'x4' printer) enables rapid "
        "prototyping and iteration without external dependencies.",
        styles
    ))

    story.append(PageBreak())

    # ========== FINANCIAL PROJECTIONS ==========
    story.append(Paragraph("11 Financial Projections", styles['SectionTitle']))
    story.append(Spacer(1, 5))
    line_table = Table([['']], colWidths=[6.5*inch], rowHeights=[3])
    line_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), SECONDARY)]))
    story.append(line_table)
    story.append(Spacer(1, 15))

    story.append(Paragraph("CORE ASSUMPTIONS", styles['SubsectionTitle']))
    story.append(create_metrics_row([
        ("$375", "Average Selling Price"),
        ("$140", "Est. COGS/Unit"),
        ("62%", "Gross Margin"),
        ("$235", "Gross Profit/Unit"),
    ], styles))

    story.append(Spacer(1, 20))
    story.append(Paragraph("THREE-YEAR PROJECTIONS", styles['SubsectionTitle']))
    story.append(create_data_table(
        ["Metric", "Year 1 (Launch)", "Year 2", "Year 3"],
        [
            ["Units Sold", "2,500", "7,500", "20,000"],
            ["Revenue", "$937,500", "$2,812,500", "$7,500,000"],
            ["Gross Profit", "$587,500", "$1,762,500", "$4,700,000"],
            ["Gross Margin", "62.7%", "62.7%", "62.7%"],
        ],
        [1.625*inch, 1.625*inch, 1.625*inch, 1.625*inch]
    ))

    story.append(Spacer(1, 15))
    story.append(Paragraph("YEAR 1 EXPENSE CATEGORIES", styles['SubsectionTitle']))
    for item in ["Tooling & manufacturing setup",
                 "Licensing fees and royalties",
                 "Initial inventory investment",
                 "Marketing launch campaign",
                 "Operations & fulfillment"]:
        story.append(Paragraph(f"• {item}", styles['BulletText']))

    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "<i>Projections exclude potential upside from additional product lines, international "
        "expansion, or enterprise/B2B sales.</i>",
        styles['BodyText']
    ))

    story.append(PageBreak())

    # ========== CAPITAL & GROWTH STRATEGY ==========
    story.append(Paragraph("12 Capital & Growth Strategy", styles['SectionTitle']))
    story.append(Spacer(1, 5))
    line_table = Table([['']], colWidths=[6.5*inch], rowHeights=[3])
    line_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), SECONDARY)]))
    story.append(line_table)
    story.append(Spacer(1, 15))

    story.append(Paragraph("INITIAL CAPITAL NEEDS", styles['SubsectionTitle']))
    story.append(create_data_table(
        ["Category", "Use of Funds"],
        [
            ["Tooling & Manufacturing", "Mold development, production setup"],
            ["Licensing Fees", "CLC/school licensing agreements"],
            ["Inventory", "Initial production run"],
            ["Marketing Launch", "Brand development, campaign execution"],
        ],
        [2.5*inch, 4*inch]
    ))

    story.append(Spacer(1, 15))
    story.append(create_highlight_box(
        "Target Raise (Optional)",
        '<para align="center"><font size="20"><b>$500K - $1.5M</b></font></para>'
        '<para align="center">Strategic investors preferred. Ideal partner brings <b>distribution</b>, '
        '<b>licensing leverage</b>, or <b>eComm scale</b>.</para>',
        styles
    ))

    story.append(Spacer(1, 15))
    story.append(Paragraph("EXIT VISION", styles['SubsectionTitle']))
    exit_data = [
        [Paragraph("<b>Strategic Acquirers</b>", styles['BodyText']),
         Paragraph("<b>Exit Criteria</b>", styles['BodyText'])],
        [Paragraph("• Fanatics<br/>• YETI<br/>• Private equity roll-up<br/>• Consumer products conglomerate", styles['BulletText']),
         Paragraph("• Established brand leadership<br/>• Proven unit economics<br/>• Scalable licensing model<br/>• Platform extensibility demonstrated", styles['BulletText'])]
    ]
    exit_table = Table(exit_data, colWidths=[3.25*inch, 3.25*inch])
    exit_table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP')]))
    story.append(exit_table)

    story.append(Spacer(1, 20))
    story.append(create_highlight_box(
        "Long-Term Vision",
        "PopTop aims to be the <b>default beverage system for fans</b>. Brand scales across "
        "beverage platforms and becomes synonymous with premium tailgate experiences.",
        styles
    ))

    # Confidential footer
    story.append(Spacer(1, 40))
    story.append(Paragraph(
        "<i>This document is confidential and intended for strategic discussion purposes only.</i>",
        ParagraphStyle('Footer', parent=styles['BodyText'], alignment=TA_CENTER, textColor=TEXT_LIGHT, fontSize=9)
    ))
    story.append(Paragraph(
        "PopTop, LLC | A Munn Family Holdings Company | Indiana",
        ParagraphStyle('Footer2', parent=styles['BodyText'], alignment=TA_CENTER, textColor=TEXT_LIGHT, fontSize=9)
    ))

    # Build with cover page
    def first_page(canvas, doc):
        create_cover_page(canvas, doc)

    def later_pages(canvas, doc):
        add_page_number(canvas, doc)

    doc.build(story, onFirstPage=first_page, onLaterPages=later_pages)
    print(f"PDF created successfully: {output_path}")

if __name__ == "__main__":
    build_document()
