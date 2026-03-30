from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime

from models import Session, User, Progress


class ReportGenerator:
    def __init__(self, user_id):
        self.user_id = user_id

    def generate_pdf(self):
        db = Session()

        # Load user details
        user = db.query(User).get(self.user_id)

        # Get all progress records for the user
        progress = db.query(Progress).filter(
            Progress.UserID == self.user_id
        ).all()

        total = len(progress)
        completed = sum(1 for p in progress if p.CompletionPercent == 100)
        in_progress = sum(1 for p in progress if 0 < p.CompletionPercent < 100)
        not_started = total - completed - in_progress

        overall = (
            sum(p.CompletionPercent for p in progress) / total
            if total > 0 else 0
        )

        timestamp = datetime.now().strftime("%d %B %Y %H:%M")
        db.close()

        filename = f"report_user_{self.user_id}.pdf"

        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # Title
        elements.append(
            Paragraph("<b>ReviseWise Study Report</b>", styles["Title"])
        )
        elements.append(Spacer(1, 12))

        # User info section
        user_info = f"""
        <b>User ID:</b> {user.UserID}<br/>
        <b>Email:</b> {user.Email}<br/>
        <b>Learning Style:</b> {user.Style}<br/>
        <b>Date Generated:</b> {timestamp}<br/><br/>
        """
        elements.append(Paragraph(user_info, styles["Normal"]))
        elements.append(Spacer(1, 12))

        # Summary section
        summary = f"""
        <b>Progress Summary</b><br/>
        Total Resources: {total}<br/>
        Completed: {completed}<br/>
        In Progress: {in_progress}<br/>
        Not Started: {not_started}<br/>
        Overall Completion: {round(overall, 1)}%<br/><br/>
        """
        elements.append(Paragraph(summary, styles["Normal"]))
        elements.append(Spacer(1, 12))

        # Table of resources
        table_data = [["Resource", "Type", "Style", "Completion"]]

        for p in progress:
            table_data.append([
                p.resource.Title,
                p.resource.Type,
                p.resource.StyleMatch,
                f"{p.CompletionPercent}%"
            ])

        table = Table(table_data, colWidths=[180, 80, 80, 80])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ]))

        elements.append(table)

        doc.build(elements)
        return filename
