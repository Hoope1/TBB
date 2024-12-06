from sqlalchemy.orm import Session
from database import Teilnehmer, Test, Prognose, SessionLocal
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime


class ReportGenerator:
    def __init__(self):
        self.db = SessionLocal()

    def generate_participant_report(self, teilnehmer_id):
        """
        Erstellt einen PDF-Bericht für einen Teilnehmer.
        """
        teilnehmer = self.db.query(Teilnehmer).filter_by(teilnehmer_id=teilnehmer_id).first()
        if not teilnehmer:
            raise ValueError("Teilnehmer nicht gefunden.")

        tests = self.db.query(Test).filter_by(teilnehmer_id=teilnehmer_id).all()
        prognosen = self.db.query(Prognose).filter_by(teilnehmer_id=teilnehmer_id).all()

        report_filename = f"Teilnehmerbericht_{teilnehmer.name}_{datetime.now().strftime('%Y%m%d')}.pdf"
        pdf = canvas.Canvas(report_filename, pagesize=letter)

        # Header
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, 750, f"Teilnehmerbericht: {teilnehmer.name}")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, 730, f"SV-Nummer: {teilnehmer.sv_nummer}")
        pdf.drawString(50, 710, f"Geburtsdatum: {teilnehmer.geburtsdatum.strftime('%d.%m.%Y')}")
        pdf.drawString(50, 690, f"Status: {teilnehmer.status}")

        # Tests
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, 650, "Testergebnisse:")
        pdf.setFont("Helvetica", 12)
        y_position = 630
        if tests:
            for test in tests:
                pdf.drawString(50, y_position, f"Test am {test.test_datum.strftime('%d.%m.%Y')}:")
                pdf.drawString(70, y_position - 15, f"- Brüche: {test.brueche_erreichte_punkte}/{test.brueche_max_punkte}")
                pdf.drawString(70, y_position - 30, f"- Textaufgaben: {test.textaufgaben_erreichte_punkte}/{test.textaufgaben_max_punkte}")
                pdf.drawString(70, y_position - 45, f"- Raumvorstellung: {test.raumvorstellung_erreichte_punkte}/{test.raumvorstellung_max_punkte}")
                pdf.drawString(70, y_position - 60, f"- Gleichungen: {test.gleichungen_erreichte_punkte}/{test.gleichungen_max_punkte}")
                pdf.drawString(70, y_position - 75, f"- Grundrechenarten: {test.grundrechenarten_erreichte_punkte}/{test.grundrechenarten_max_punkte}")
                pdf.drawString(70, y_position - 90, f"- Zahlenraum: {test.zahlenraum_erreichte_punkte}/{test.zahlenraum_max_punkte}")
                y_position -= 120
                if y_position < 100:
                    pdf.showPage()
                    y_position = 750
        else:
            pdf.drawString(50, y_position, "Keine Testergebnisse verfügbar.")

        # Prognosen
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, y_position - 20, "Prognosen:")
        pdf.setFont("Helvetica", 12)
        y_position -= 40
        if prognosen:
            for prognose in prognosen:
                pdf.drawString(50, y_position, f"Prognose für den {prognose.prognose_datum.strftime('%d.%m.%Y')}:")
                pdf.drawString(70, y_position - 15, f"- Brüche: {prognose.brueche_prognose:.2f}")
                pdf.drawString(70, y_position - 30, f"- Textaufgaben: {prognose.textaufgaben_prognose:.2f}")
                pdf.drawString(70, y_position - 45, f"- Raumvorstellung: {prognose.raumvorstellung_prognose:.2f}")
                pdf.drawString(70, y_position - 60, f"- Gleichungen: {prognose.gleichungen_prognose:.2f}")
                pdf.drawString(70, y_position - 75, f"- Grundrechenarten: {prognose.grundrechenarten_prognose:.2f}")
                pdf.drawString(70, y_position - 90, f"- Zahlenraum: {prognose.zahlenraum_prognose:.2f}")
                pdf.drawString(70, y_position - 105, f"- Gesamtprognose: {prognose.gesamt_prognose:.2f}")
                y_position -= 130
                if y_position < 100:
                    pdf.showPage()
                    y_position = 750
        else:
            pdf.drawString(50, y_position, "Keine Prognosen verfügbar.")

        # Abschluss
        pdf.save()
        return report_filename
