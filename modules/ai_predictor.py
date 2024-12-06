import pandas as pd
from flaml import AutoML
from sqlalchemy.orm import Session
from database import Prognose, Test, Teilnehmer, SessionLocal
from datetime import datetime, timedelta

class AIPredictor:
    """
    Diese Klasse erstellt KI-basierte Prognosen für die Testergebnisse der Teilnehmer.
    """

    def __init__(self):
        self.db: Session = SessionLocal()
        self.models = {}  # Speichert trainierte Modelle für jeden Teilnehmer

    def train_model(self, teilnehmer_id):
        """
        Trainiert ein Modell für einen Teilnehmer basierend auf dessen Testergebnissen.

        Args:
            teilnehmer_id (int): Die ID des Teilnehmers.
        """
        tests = self.db.query(Test).filter_by(teilnehmer_id=teilnehmer_id).all()
        if not tests or len(tests) < 2:
            # Nicht genug Daten, um ein Modell zu trainieren
            return None

        # Vorbereitung der Trainingsdaten
        data = pd.DataFrame([{
            "Tag": (test.test_datum - datetime.now().date()).days,
            "Gesamt": test.gesamt_prozent,
        } for test in tests])

        X = data[["Tag"]]
        y = data["Gesamt"]

        # Modell mit FLAML trainieren
        automl = AutoML()
        automl.fit(X_train=X, y_train=y, task="regression", time_budget=10)
        self.models[teilnehmer_id] = automl

    def predict(self, teilnehmer_id):
        """
        Erstellt eine Prognose für die nächsten 60 Tage (-30 bis +30).

        Args:
            teilnehmer_id (int): Die ID des Teilnehmers.

        Returns:
            list: Liste der Prognosen (einen Eintrag pro Tag).
        """
        if teilnehmer_id not in self.models:
            self.train_model(teilnehmer_id)

        model = self.models.get(teilnehmer_id)
        if not model:
            return None

        # Prognosezeitraum: -30 bis +30 Tage
        future_days = pd.DataFrame({"Tag": range(-30, 31)})
        predictions = model.predict(future_days)

        # Prognosen speichern
        for idx, day in future_days.iterrows():
            new_prognose = Prognose(
                teilnehmer_id=teilnehmer_id,
                prognose_datum=datetime.now().date(),
                tag=day["Tag"],
                gesamt_prognose=predictions[idx],
            )
            self.db.add(new_prognose)

        self.db.commit()

        # Rückgabe der Prognose als DataFrame
        return pd.DataFrame({
            "Tag": future_days["Tag"],
            "Prognose": predictions
        })

    def get_predictions(self, teilnehmer_id):
        """
        Ruft gespeicherte Prognosen für einen Teilnehmer ab.

        Args:
            teilnehmer_id (int): Die ID des Teilnehmers.

        Returns:
            pd.DataFrame: DataFrame mit den gespeicherten Prognosen.
        """
        prognosen = self.db.query(Prognose).filter_by(teilnehmer_id=teilnehmer_id).all()
        return pd.DataFrame([{
            "Tag": prognose.tag,
            "Prognose": prognose.gesamt_prognose,
        } for prognose in prognosen])
      
