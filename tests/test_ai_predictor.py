import unittest
from modules.ai_predictor import AIPredictor
from modules.test_manager import TestManager
from modules.data_manager import DataManager

class TestAIPredictor(unittest.TestCase):
    def setUp(self):
        self.predictor = AIPredictor()
        self.test_manager = TestManager()
        self.data_manager = DataManager()

        # Teilnehmer für Tests hinzufügen
        self.data_manager.add_participant(
            name="Anna Beispiel",
            sv_nummer="1234010191",
            geschlecht="Weiblich",
            eintrittsdatum="2023-01-01"
        )
        self.participant = self.data_manager.get_participants()[0]

        # Tests hinzufügen
        self.test_manager.add_test(
            teilnehmer_id=self.participant.teilnehmer_id,
            test_datum="2023-11-01",
            erreichte_punkte={"Brüche": 20, "Textaufgaben": 15, "Raumvorstellung": 10,
                              "Gleichungen": 25, "Grundrechenarten": 15, "Zahlenraum": 15},
            max_punkte={k: 20 for k in ["Brüche", "Textaufgaben", "Raumvorstellung", "Gleichungen", "Grundrechenarten", "Zahlenraum"]}
        )
        self.test_manager.add_test(
            teilnehmer_id=self.participant.teilnehmer_id,
            test_datum="2023-12-01",
            erreichte_punkte={"Brüche": 15, "Textaufgaben": 20, "Raumvorstellung": 15,
                              "Gleichungen": 25, "Grundrechenarten": 10, "Zahlenraum": 15},
            max_punkte={k: 20 for k in ["Brüche", "Textaufgaben", "Raumvorstellung", "Gleichungen", "Grundrechenarten", "Zahlenraum"]}
        )

    def test_train_model(self):
        self.predictor.train_model(self.participant.teilnehmer_id)
        self.assertIn(self.participant.teilnehmer_id, self.predictor.models)

    def test_predict(self):
        self.predictor.train_model(self.participant.teilnehmer_id)
        predictions = self.predictor.predict(self.participant.teilnehmer_id)
        self.assertIsNotNone(predictions)
        self.assertEqual(len(predictions), 61)  # -30 bis +30 Tage

if __name__ == "__main__":
    unittest.main()
  
