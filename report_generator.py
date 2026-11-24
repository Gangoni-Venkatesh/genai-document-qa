
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable
)
from reportlab.lib import colors
from xml.sax.saxutils import escape


def generate_chat_report(document_names, chat_history):

    buffer = BytesIO()

    pdf = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "AI Document Q&amp;A Chatbot",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            "Chat Conversation Report",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph("Uploaded Documents", styles["Heading2"])
    )

    for name in document_names:
        story.append(
            Paragraph(f"- {escape(name)}", styles["Normal"])
        )

    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", color=colors.grey))
    story.append(Spacer(1, 15))

    story.append(
        Paragraph("Conversation History", styles["Heading2"])
    )

    for message in chat_history:

        role = message.get("role", "").capitalize()
        content = escape(str(message.get("content", "")))

        story.append(
            Paragraph(role, styles["Heading3"])
        )

        story.append(
            Paragraph(content.replace("\n", "<br/>"), styles["BodyText"])
        )

        if role == "Assistant":

            sources = message.get("sources", [])

            if sources:

                story.append(
                    Paragraph("Source References:", styles["Heading4"])
                )

                for source in sources:

                    source_name = escape(str(source.get("source", "Unknown")))
                    page = escape(str(source.get("page", "Unknown")))

                    story.append(
                        Paragraph(
                            f"Document: {source_name} | Page: {page}",
                            styles["Normal"]
                        )
                    )

        story.append(Spacer(1, 15))

    pdf.build(story)

    buffer.seek(0)

    return buffer
