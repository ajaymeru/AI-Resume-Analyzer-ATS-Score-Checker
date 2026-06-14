import io
from datetime import datetime
from typing import Dict, Any, List
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def generate_pdf_report(analysis_results: Dict[str, Any], filename_prefix: str = "ATS_Analysis_Report") -> bytes:
    """
    Generates a professional PDF report containing the ATS score, skill analysis, 
    statistics, and recommendations using ReportLab flowables.
    
    Args:
        analysis_results: The dictionary output of analyze_resume().
        filename_prefix: Prefix for document reference.
        
    Returns:
        Bytes representing the PDF document.
    """
    # Create an in-memory byte buffer to write the generated PDF into
    buffer = io.BytesIO()
    
    # Initialize the SimpleDocTemplate with page layout settings
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    # Retrieve the default stylesheet from ReportLab sample styles
    styles = getSampleStyleSheet()
    
    # Define a premium color scheme matching the web dashboard aesthetics
    primary_color = colors.HexColor("#1A365D")    # Dark Navy
    secondary_color = colors.HexColor("#2B6CB0")  # Royal Blue
    accent_color = colors.HexColor("#319795")     # Teal
    text_color = colors.HexColor("#2D3748")       # Charcoal grey
    muted_color = colors.HexColor("#718096")      # Slate grey
    bg_light = colors.HexColor("#F7FAFC")         # Off-white/light grey background
    
    # ----------------------------------------------------
    # Custom Paragraph Styles for Layout Typography
    # ----------------------------------------------------
    
    # Main Report Title
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        spaceAfter=6
    )
    
    # Document Metadata (Generated date/time)
    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=muted_color,
        spaceAfter=15
    )
    
    # Section Header Titles
    section_title = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )
    
    # Generic Body Text
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=text_color,
        spaceAfter=6
    )
    
    # Bolded Body Text
    bold_body_style = ParagraphStyle(
        'DocBodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    
    # Custom Bullet Points Style
    bullet_style = ParagraphStyle(
        'DocBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=text_color,
        leftIndent=15,
        firstLineIndent=-8,
        spaceAfter=4
    )
    
    # Text inside standard tables
    table_text = ParagraphStyle(
        'TableText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=text_color
    )
    
    # Text inside table header rows
    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.whitesmoke
    )

    # List of Flowables to build the report sequence
    story = []
    
    # ====================================================
    # 1. Header Section
    # ====================================================
    story.append(Paragraph("AI Resume Analyzer & ATS Score Report", title_style))
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    story.append(Paragraph(f"Generated on: {current_date} | Evaluation Report", meta_style))
    story.append(Spacer(1, 10))
    
    # ====================================================
    # 2. Executive Summary Box (A styled ReportLab Table)
    # ====================================================
    score = analysis_results["ats_score"]
    strength = analysis_results["strength_level"]
    
    # Map score status level to corresponding color indicators
    if strength == "Excellent":
        score_color = colors.HexColor("#2F855A")  # Green
    elif strength == "Good":
        score_color = colors.HexColor("#2B6CB0")  # Blue
    elif strength == "Average":
        score_color = colors.HexColor("#D69E2E")  # Orange/Yellow
    else:
        score_color = colors.HexColor("#C53030")  # Red
        
    # Table layout for metric headers and actual values
    summary_data = [
        [
            Paragraph("<b>Overall ATS Match Score</b>", bold_body_style),
            Paragraph("<b>Strength Rating</b>", bold_body_style),
            Paragraph("<b>Word Count</b>", bold_body_style),
            Paragraph("<b>Reading Est.</b>", bold_body_style)
        ],
        [
            Paragraph(f"<font color='{score_color.hexval()}'><b>{score}%</b></font>", ParagraphStyle('ScoreVal', parent=body_style, fontSize=18, leading=22)),
            Paragraph(f"<font color='{score_color.hexval()}'><b>{strength}</b></font>", ParagraphStyle('StrengthVal', parent=body_style, fontSize=14, leading=18)),
            Paragraph(str(analysis_results["word_count"]), body_style),
            Paragraph(f"{analysis_results['reading_time']} min", body_style)
        ]
    ]
    
    # Construct the executive summary table
    summary_table = Table(summary_data, colWidths=[130, 130, 130, 130])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg_light),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 1, muted_color),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    
    story.append(summary_table)
    story.append(Spacer(1, 15))
    
    # ====================================================
    # 3. Contact Information Check Results Table
    # ====================================================
    story.append(Paragraph("Contact Information Scan", section_title))
    contact = analysis_results["contact_info"]
    
    # Simple utility to format boolean status into HTML-colored strings
    def get_status_str(found: bool) -> str:
        return "<font color='#2F855A'><b>Found</b></font>" if found else "<font color='#C53030'><b>Missing</b></font>"
        
    contact_data = [
        [
            Paragraph("<b>Email</b>", table_text), Paragraph(get_status_str(contact["email"]), table_text),
            Paragraph("<b>Phone</b>", table_text), Paragraph(get_status_str(contact["phone"]), table_text)
        ],
        [
            Paragraph("<b>LinkedIn Profile</b>", table_text), Paragraph(get_status_str(contact["linkedin"]), table_text),
            Paragraph("<b>GitHub Link</b>", table_text), Paragraph(get_status_str(contact["github"]), table_text)
        ]
    ]
    
    # Construct contact information table
    contact_table = Table(contact_data, colWidths=[130, 130, 130, 130])
    contact_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg_light),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(contact_table)
    story.append(Spacer(1, 15))
    
    # ====================================================
    # 4. Skill Gap Analysis Table
    # ====================================================
    story.append(Paragraph("Skill Analysis & Gap Mapping", section_title))
    
    # Join lists of skills into comma-separated text blocks
    matching_skills_str = ", ".join(analysis_results["matching_skills"]) if analysis_results["matching_skills"] else "None identified"
    missing_skills_str = ", ".join(analysis_results["missing_skills"]) if analysis_results["missing_skills"] else "None identified"
    additional_skills_str = ", ".join(analysis_results["additional_skills"]) if analysis_results["additional_skills"] else "None identified"
    
    skills_data = [
        [Paragraph("<b>Status</b>", table_header), Paragraph("<b>Identified Skills</b>", table_header)],
        [Paragraph("<b>Matching Skills</b>", table_text), Paragraph(matching_skills_str, table_text)],
        [Paragraph("<b>Missing Required Skills</b>", table_text), Paragraph(f"<font color='#C53030'><b>{missing_skills_str}</b></font>", table_text)],
        [Paragraph("<b>Other Skills Found</b>", table_text), Paragraph(additional_skills_str, table_text)]
    ]
    
    # Construct details skills breakdown table
    skills_table = Table(skills_data, colWidths=[150, 370])
    skills_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), secondary_color),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, bg_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(skills_table)
    story.append(Spacer(1, 15))
    
    # ====================================================
    # 5. Missing Keywords
    # ====================================================
    if analysis_results["missing_keywords"]:
        story.append(Paragraph("Important Keywords to Add", section_title))
        story.append(Paragraph("The following words were highly prioritized in the job description but are absent or infrequent in your resume:", body_style))
        story.append(Spacer(1, 4))
        keywords_str = ", ".join(analysis_results["missing_keywords"])
        story.append(Paragraph(f"<b>Missing Keywords:</b> {keywords_str}", ParagraphStyle('KeywordsBlock', parent=body_style, textColor=accent_color)))
        story.append(Spacer(1, 15))
        
    # ====================================================
    # 6. Tips & Recommendations List
    # ====================================================
    story.append(Paragraph("Key Improvement Recommendations", section_title))
    for tip in analysis_results["tips"]:
        story.append(Paragraph(f"• {tip}", bullet_style))
        
    # ====================================================
    # Build Document PDF Compilation
    # ====================================================
    doc.build(story)
    
    # Return the binary data from the memory buffer
    return buffer.getvalue()

