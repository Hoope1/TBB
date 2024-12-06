from sqlalchemy.orm import Session
from database import Test, Teilnehmer, SessionLocal
from datetime import datetime

class TestManager:
    """
    Diese Klasse verwaltet die Tests der Teilnehmer.
    """

    def __init__(self):
        self.db: Session = SessionLocal()

    def add_test(self, teilnehmer_id, test_datum, erreichte_punkte, max_punkte):
        """
        Fügt einen Test hinzu und berechnet die Prozentwerte.

        Args:
            teilnehmer_id (int): Die ID des Teilnehmers.
            test_datum (str): Das Datum des Tests (YYYY-MM-DD).
            erreichte_punkte (dict): Erreichte Punkte in den Kategorien.
            max_punkte (dict): Maximale Punkte in den Kategorien.
        """
        # Berechnung der Gesamtpunkte
        gesamt_erreichte_punkte = sum(erreichte_punkte.values())
        gesamt_max_punkte = sum(max_punkte.values())

        # Berechnung der Gesamtprozentwerte
        gesamt_prozent = (gesamt_erreichte_punkte / gesamt_max_punkte) * 100

        # Erstellung des neuen Tests
        new_test = Test(
            teilnehmer_id=teilnehmer_id,
            test_datum=datetime.strptime(test_datum, "%Y-%m-%d").date(),
            brueche_erreichte_punkte=erreichte_punkte["Brüche"],
            brueche_max_punkte=max_punkte["Brüche"],
            textaufgaben_erreichte_punkte=erreichte_punkte["Textaufgaben"],
            textaufgaben_max_punkte=max_punkte["Textaufgaben"],
            raumvorstellung_erreichte_punkte=erreichte_punkte["Raumvorstellung"],
            raumvorstellung_max_punkte=max_punkte["Raumvorstellung"],
            gleichungen_erreichte_punkte=erreichte_punkte["Gleichungen"],
            gleichungen_max_punkte=max_punkte["Gleichungen"],
            grundrechenarten_erreichte_punkte=erreichte_punkte["Grundrechenarten"],
            grundrechenarten_max_punkte=max_punkte["Grundrechenarten"],
            zahlenraum_erreichte_punkte=erreichte_punkte["Zahlenraum"],
            zahlenraum_max_punkte=max_punkte["Zahlenraum"],
            gesamt_erreichte_punkte=gesamt_erreichte_punkte,
            gesamt_max_punkte=gesamt_max_punkte,
            gesamt_prozent=gesamt_prozent,
        )
        self.db.add(new_test)
        self.db.commit()

    def get_tests_by_participant(self, teilnehmer_id):
        """
        Ruft alle Tests eines Teilnehmers ab.

        Args:
            teilnehmer_id (int): Die ID des Teilnehmers.

        Returns:
            list: Liste der Tests eines Teilnehmers.
        """
        return self.db.query(Test).filter_by(teilnehmer_id=teilnehmer_id).all()

    def get_test_summary(self, teilnehmer_id):
        """
        Erstellt eine Zusammenfassung der Tests eines Teilnehmers.

        Args:
            teilnehmer_id (int): Die ID des Teilnehmers.

        Returns:
            dict: Zusammenfassung mit Durchschnittswerten.
        """
        tests = self.get_tests_by_participant(teilnehmer_id)
        if not tests:
            return None

        summary = {
            "Anzahl Tests": len(tests),
            "Durchschnitt Gesamtprozent": sum(test.gesamt_prozent for test in tests) / len(tests),
            "Letzter Test": max(test.test_datum for test in tests).strftime("%Y-%m-%d"),
        }
        return summary
      
