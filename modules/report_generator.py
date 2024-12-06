import pandas as pd
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
import openpyxl

class ReportGenerator:
    """
    Diese Klasse erstellt PDF- und Excel-Berichte für Teilnehmer.
    """

    def generate_pdf(self, participant, tests, predictions):
        """
        Erstellt einen PDF-Bericht für einen Teilnehmer.

        Args:
            participant (dict): Teilnehmerdaten.
            tests (pd.DataFrame): Testergebnisse des Teilnehmers.
            predictions (pd.DataFrame): Prognosedaten des Teilnehmers.

        Returns:
            BytesIO: Der PDF-Bericht als Bytes-Objekt.
        """
        buffer = BytesIO()
        pdf = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        # Titel und Teilnehmerdaten
        elements.append(Paragraph(f"<b>Teilnehmerbericht: {participant['name']}</b>", styles["Title"]))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"<b>SV-Nummer:</b> {participant['sv_nummer']}", styles["Normal"]))
        elements.append(Paragraph(f"<b>Status:</b> {participant['status']}", styles["Normal"]))
        elements.append(Spacer(1, 12))

        # Testergebnisse
        if not tests.empty:
            elements.append(Paragraph("<b>Testergebnisse:</b>", styles["Heading2"]))
            table_data = [["Datum", "Gesamtprozent"] + list(tests.columns[3:9])]
            for _, row in tests.iterrows():
                table_data.append([row["test_datum"], f"{row['gesamt_prozent']:.2f}%"] + row[3:9].tolist())

            table = Table(table_data)
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ]))
            elements.append(table)
            elements.append(Spacer(1, 12))

        # Prognose
        if not predictions.empty:
            elements.append(Paragraph("<b>Prognose:</b>", styles["Heading2"]))
            for _, row in predictions.iterrows():
                elements.append(Paragraph(f"Tag {row['Tag']}: {row['Prognose']:.2f}%", styles["Normal"]))

        # PDF speichern
        pdf.build(elements)
        buffer.seek(0)
        return buffer

    def generate_excel(self, participant, tests, predictions):
        """
        Erstellt einen Excel-Bericht für einen Teilnehmer.

        Args:
            participant (dict): Teilnehmerdaten.
            tests (pd.DataFrame): Testergebnisse des Teilnehmers.
            predictions (pd.DataFrame): Prognosedaten des Teilnehmers.

        Returns:
            BytesIO: Der Excel-Bericht als Bytes-Objekt.
        """
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            # Teilnehmerdaten
            participant_df = pd.DataFrame([participant])
            participant_df.to_excel(writer, sheet_name="Teilnehmer", index=False)

            # Testergebnisse
            if not tests.empty:
                tests.to_excel(writer, sheet_name="Testergebnisse", index=False)

            # Prognosen
            if not predictions.empty:
                predictions.to_excel(writer, sheet_name="Prognosen", index=False)

        buffer.seek(0)
        return buffer
      
