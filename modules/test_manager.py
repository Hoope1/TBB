from sqlalchemy.orm import Session
from database import Test, Teilnehmer, SessionLocal
from datetime import datetime


class TestManager:
    def __init__(self):
        """Initialisiert eine neue Datenbank-Sitzung."""
        self.db: Session = SessionLocal()

    def add_test(self, participant_id: int, test_date: datetime, scores: dict):
        """
        Fügt einen neuen Test für einen Teilnehmer hinzu.

        Args:
            participant_id (int): Die ID des Teilnehmers.
            test_date (datetime): Datum des Tests.
            scores (dict): Erreichte und maximale Punkte für jede Kategorie.

        Beispiel für `scores`:
        {
            "brueche_erreichte_punkte": 10,
            "brueche_max_punkte": 15,
            "textaufgaben_erreichte_punkte": 8,
            "textaufgaben_max_punkte": 10,
            ...
        }
        """
        new_test = Test(
            teilnehmer_id=participant_id,
            test_datum=test_date,
            **scores
        )
        new_test.berechne_prozentwerte()
        self.db.add(new_test)
        self.db.commit()

    def get_tests_by_participant(self, participant_id: int):
        """
        Holt alle Tests eines Teilnehmers.

        Args:
            participant_id (int): Die ID des Teilnehmers.

        Returns:
            List[Test]: Liste aller Tests.
        """
        return self.db.query(Test).filter(Test.teilnehmer_id == participant_id).all()

    def update_test(self, test_id: int, updated_scores: dict):
        """
        Aktualisiert einen bestehenden Test.

        Args:
            test_id (int): Die ID des Tests.
            updated_scores (dict): Aktualisierte Punkte für jede Kategorie.

        Beispiel für `updated_scores`:
        {
            "brueche_erreichte_punkte": 12,
            "textaufgaben_erreichte_punkte": 9,
            ...
        }
        """
        test = self.db.query(Test).filter(Test.test_id == test_id).first()
        if test:
            for key, value in updated_scores.items():
                setattr(test, key, value)
            test.berechne_prozentwerte()
            self.db.commit()

    def delete_test(self, test_id: int):
        """
        Löscht einen Test basierend auf der Test-ID.

        Args:
            test_id (int): Die ID des Tests.
        """
        test = self.db.query(Test).filter(Test.test_id == test_id).first()
        if test:
            self.db.delete(test)
            self.db.commit()

    def get_test_statistics(self, participant_id: int):
        """
        Berechnet die Statistik der Testergebnisse eines Teilnehmers.

        Args:
            participant_id (int): Die ID des Teilnehmers.

        Returns:
            dict: Durchschnittliche Prozentwerte pro Kategorie und gesamt.
        """
        tests = self.get_tests_by_participant(participant_id)
        if not tests:
            return {}

        stats = {
            "brueche_prozent": [],
            "textaufgaben_prozent": [],
            "raumvorstellung_prozent": [],
            "gleichungen_prozent": [],
            "grundrechenarten_prozent": [],
            "zahlenraum_prozent": [],
            "gesamt_prozent": []
        }

        for test in tests:
            for key in stats.keys():
                value = getattr(test, key, None)
                if value is not None:
                    stats[key].append(value)

        # Berechnung der Durchschnittswerte
        averages = {key: sum(values) / len(values) if values else 0 for key, values in stats.items()}
        return averages
