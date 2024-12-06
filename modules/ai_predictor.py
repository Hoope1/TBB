from flaml import AutoML
from sqlalchemy.orm import Session
from database import Test, Prognose, SessionLocal
from datetime import datetime, timedelta
import pandas as pd


class AIPredictor:
    def __init__(self):
        """Initialisiert eine neue Datenbank-Sitzung."""
        self.db: Session = SessionLocal()
        self.model = AutoML()

    def train_model(self):
        """
        Trainiert das Modell basierend auf den vorhandenen Testergebnissen.
        """
        # Daten aus der Datenbank abrufen
        tests = self.db.query(Test).all()

        if not tests:
            print("Keine Tests vorhanden. Training nicht möglich.")
            return

        # Daten vorbereiten
        data = []
        for test in tests:
            data.append({
                "tag": (test.test_datum - test.teilnehmer.eintrittsdatum).days,
                "brueche_erreichte_punkte": test.brueche_erreichte_punkte,
                "textaufgaben_erreichte_punkte": test.textaufgaben_erreichte_punkte,
                "raumvorstellung_erreichte_punkte": test.raumvorstellung_erreichte_punkte,
                "gleichungen_erreichte_punkte": test.gleichungen_erreichte_punkte,
                "grundrechenarten_erreichte_punkte": test.grundrechenarten_erreichte_punkte,
                "zahlenraum_erreichte_punkte": test.zahlenraum_erreichte_punkte,
                "gesamt_prozent": test.gesamt_prozent
            })

        df = pd.DataFrame(data)
        X = df.drop(columns=["gesamt_prozent"])
        y = df["gesamt_prozent"]

        # Modell trainieren
        self.model.fit(X_train=X, y_train=y, task="regression")
        print("Modelltraining abgeschlossen.")

    def predict_progress(self, participant_id: int, days_ahead: int = 30):
        """
        Gibt Prognosen für einen Teilnehmer basierend auf einem zukünftigen Datum zurück.

        Args:
            participant_id (int): Die ID des Teilnehmers.
            days_ahead (int): Anzahl der Tage in der Zukunft für die Prognose.

        Returns:
            dict: Prognosen für jede Kategorie und gesamt.
        """
        # Teilnehmerdaten abrufen
        participant = self.db.query(Test).filter(Test.teilnehmer_id == participant_id).all()
        if not participant:
            print(f"Keine Tests für Teilnehmer-ID {participant_id} gefunden.")
            return {}

        last_test = max(participant, key=lambda t: t.test_datum)
        future_date = last_test.test_datum + timedelta(days=days_ahead)
        features = {
            "tag": (future_date - last_test.teilnehmer.eintrittsdatum).days,
            "brueche_erreichte_punkte": last_test.brueche_erreichte_punkte,
            "textaufgaben_erreichte_punkte": last_test.textaufgaben_erreichte_punkte,
            "raumvorstellung_erreichte_punkte": last_test.raumvorstellung_erreichte_punkte,
            "gleichungen_erreichte_punkte": last_test.gleichungen_erreichte_punkte,
            "grundrechenarten_erreichte_punkte": last_test.grundrechenarten_erreichte_punkte,
            "zahlenraum_erreichte_punkte": last_test.zahlenraum_erreichte_punkte
        }

        # Prognose berechnen
        df_features = pd.DataFrame([features])
        prediction = self.model.predict(df_features)

        # Prognose speichern
        new_prognose = Prognose(
            teilnehmer_id=participant_id,
            prognose_datum=future_date,
            tag=features["tag"],
            brueche_prognose=features["brueche_erreichte_punkte"],
            textaufgaben_prognose=features["textaufgaben_erreichte_punkte"],
            raumvorstellung_prognose=features["raumvorstellung_erreichte_punkte"],
            gleichungen_prognose=features["gleichungen_erreichte_punkte"],
            grundrechenarten_prognose=features["grundrechenarten_erreichte_punkte"],
            zahlenraum_prognose=features["zahlenraum_erreichte_punkte"],
            gesamt_prognose=prediction[0]
        )
        self.db.add(new_prognose)
        self.db.commit()

        return {
            "gesamt_prognose": prediction[0],
            "details": features
        }

    def evaluate_model(self):
        """
        Bewertet das Modell basierend auf den Trainingsdaten.
        """
        if not self.model.best_config:
            print("Modell ist noch nicht trainiert.")
            return

        print(f"Bestes Modell: {self.model.best_config}")
        print(f"Beste Punktzahl: {self.model.best_loss}")


if __name__ == "__main__":
    ai_predictor = AIPredictor()
    ai_predictor.train_model()
    print(ai_predictor.predict_progress(participant_id=1, days_ahead=30))
