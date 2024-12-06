from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import Teilnehmer, Test, Prognose, SessionLocal
import pandas as pd
from flaml import AutoML

class AIPredictor:
    def __init__(self):
        self.db = SessionLocal()

    def generate_forecasts(self, teilnehmer_id, tage_in_zukunft):
        """
        Generiert Prognosen für einen Teilnehmer basierend auf seinen bisherigen Tests.
        """
        tests = self.db.query(Test).filter_by(teilnehmer_id=teilnehmer_id).all()
        if not tests:
            raise ValueError("Keine Tests für diesen Teilnehmer gefunden.")

        # Daten vorbereiten
        data = []
        for test in tests:
            data.append({
                "datum": test.test_datum,
                "brueche": test.brueche_erreichte_punkte,
                "textaufgaben": test.textaufgaben_erreichte_punkte,
                "raumvorstellung": test.raumvorstellung_erreichte_punkte,
                "gleichungen": test.gleichungen_erreichte_punkte,
                "grundrechenarten": test.grundrechenarten_erreichte_punkte,
                "zahlenraum": test.zahlenraum_erreichte_punkte
            })

        df = pd.DataFrame(data)
        df["datum"] = pd.to_datetime(df["datum"])
        df = df.sort_values("datum").reset_index(drop=True)

        forecasts = []
        for column in ["brueche", "textaufgaben", "raumvorstellung", "gleichungen", "grundrechenarten", "zahlenraum"]:
            if len(df) < 2:
                raise ValueError(f"Nicht genügend Daten für Prognosen für {column}.")
            
            # Prognosemodell trainieren
            automl = AutoML()
            train_data = df[["datum", column]].dropna()
            train_data["tage"] = (train_data["datum"] - train_data["datum"].min()).dt.days
            X_train = train_data[["tage"]]
            y_train = train_data[column]
            automl.fit(X_train, y_train, task="regression", time_budget=5)

            # Prognose generieren
            max_tage = train_data["tage"].max()
            future_tage = [max_tage + i for i in range(1, tage_in_zukunft + 1)]
            y_pred = automl.predict(pd.DataFrame(future_tage, columns=["tage"]))

            forecasts.append((column, y_pred))

        # Prognosen in der Datenbank speichern
        for i, tag in enumerate(range(1, tage_in_zukunft + 1)):
            prognose_datum = datetime.now().date() + timedelta(days=tag)
            new_prognose = Prognose(
                teilnehmer_id=teilnehmer_id,
                prognose_datum=prognose_datum,
                tag=tag,
                brueche_prognose=forecasts[0][1][i],
                textaufgaben_prognose=forecasts[1][1][i],
                raumvorstellung_prognose=forecasts[2][1][i],
                gleichungen_prognose=forecasts[3][1][i],
                grundrechenarten_prognose=forecasts[4][1][i],
                zahlenraum_prognose=forecasts[5][1][i],
                gesamt_prognose=sum([f[1][i] for f in forecasts])
            )
            self.db.add(new_prognose)

        self.db.commit()

    def get_forecasts_for_participant(self, teilnehmer_id):
        """
        Gibt alle Prognosen eines Teilnehmers zurück.
        """
        return self.db.query(Prognose).filter_by(teilnehmer_id=teilnehmer_id).all()
