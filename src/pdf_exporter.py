from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib  import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Spacer,
    Paragraph,
    ListFlowable,
    ListItem
)

from src.parser import split_sections

def safe_text(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def resume_to_pdf(resume_text: str) -> bytes:
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    header_style = ParagraphStyle(
        name="Header",
        parent=styles["Title"],
        fontSize=16,
        leading=20,
        alignment= TA_CENTER,
        textColor=colors.black,
        spaceAfter=10
    )

    section_style = ParagraphStyle(
        name="Section",
        parent=styles["Heading2"],
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#222222"),
        spaceBefore=8,
        spaceAfter=6,
        alignment=TA_LEFT,
    )

    body_style = ParagraphStyle(
        name="Body",
        parent=styles["BodyText"],
        fontSize=10.5,
        leading=14,
        alignment=TA_LEFT,
        spaceAfter=4,
    )

    bullet_style = ParagraphStyle(
        name="bullet",
        parent=body_style,
        leftIndent=8,
    )

    sections = split_sections(resume_text)
    story = []

    first_real_line = None
    for sec in sections.values():
        if sec:
            first_real_line = sec[0]
            break
    
    story.append(Paragraph(safe_text(first_real_line or "Optimized Resume"), header_style))
    story.append(Spacer(1,6))

    for section_name in [
        "Professional Summary",
        "Skills",
        "Experience",
        "Projects",
        "Education",
        "Other",
    ]:
        content = sections.get(section_name, [])
        if not content:
            continue

        if section_name != "Other":
            story.append(Paragraph(section_name, section_style))

        bullets = []
        normal_lines = []

        for line in content:
            stripped = line.strip()
            if stripped.startswith("- "):
                bullets.append(stripped[2:].strip())
            else:
                normal_lines.append(stripped)

        for line in normal_lines:
            story.append(Paragraph(safe_text(line), body_style))

        if bullets:
            bullet_items = [
                ListItem(Paragraph(safe_text(item), bullet_style))
                for item in bullets
            ]
            story.append(ListFlowable(bullet_items, bulletType="bullet", leftIndent=18))
            story.append(Spacer(1, 4))

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes