from sqlalchemy.orm import Session
from database import Test, SessionLocal
from datetime import datetime

class TestManager:
    def __init__(self):
        self.db = SessionLocal()

    def add_test(self, teilnehmer_id, test_datum, brueche_erreichte_punkte, brueche_max_punkte,
                 textaufgaben_erreichte_punkte, textaufgaben_max_punkte, raumvorstellung_erreichte_punkte,
                 raumvorstellung_max_punkte, gleichungen_erreichte_punkte, gleichungen_max_punkte,
                 grundrechenarten_erreichte_punkte, grundrechenarten_max_punkte, zahlenraum_erreichte_punkte,
                 zahlenraum_max_punkte):
        """
        Fügt einen neuen Test für einen Teilnehmer hinzu und berechnet die Gesamtpunktzahl und den Prozentsatz.
        """
        new_test = Test(
            teilnehmer_id=teilnehmer_id,
            test_datum=test_datum,
            brueche_erreichte_punkte=brueche_erreichte_punkte,
            brueche_max_punkte=brueche_max_punkte,
            textaufgaben_erreichte_punkte=textaufgaben_erreichte_punkte,
            textaufgaben_max_punkte=textaufgaben_max_punkte,
            raumvorstellung_erreichte_punkte=raumvorstellung_erreichte_punkte,
            raumvorstellung_max_punkte=raumvorstellung_max_punkte,
            gleichungen_erreichte_punkte=gleichungen_erreichte_punkte,
            gleichungen_max_punkte=gleichungen_max_punkte,
            grundrechenarten_erreichte_punkte=grundrechenarten_erreichte_punkte,
            grundrechenarten_max_punkte=grundrechenarten_max_punkte,
            zahlenraum_erreichte_punkte=zahlenraum_erreichte_punkte,
            zahlenraum_max_punkte=zahlenraum_max_punkte
        )
        new_test.berechne_prozentwerte()
        self.db.add(new_test)
        self.db.commit()

    def get_tests_for_participant(self, teilnehmer_id):
        """
        Gibt alle Tests eines Teilnehmers zurück.
        """
        return self.db.query(Test).filter_by(teilnehmer_id=teilnehmer_id).all()

    def delete_test(self, test_id):
        """
        Löscht einen Test anhand seiner ID.
        """
        test = self.db.query(Test).filter_by(test_id=test_id).first()
        if test:
            self.db.delete(test)
            self.db.commit()
