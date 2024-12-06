import unittest
from modules.test_manager import TestManager
from modules.data_manager import DataManager

class TestTestManager(unittest.TestCase):
    def setUp(self):
        self.test_manager = TestManager()
        self.data_manager = DataManager()

        # Teilnehmer für Tests hinzufügen
        self.data_manager.add_participant(
            name="Max Mustermann",
            sv_nummer="1234010190",
            geschlecht="Männlich",
            eintrittsdatum="2023-01-01"
        )
        self.participant = self.data_manager.get_participants()[0]

    def test_add_test(self):
        erreichte_punkte = {
            "Brüche": 20,
            "Textaufgaben": 15,
            "Raumvorstellung": 10,
            "Gleichungen": 25,
            "Grundrechenarten": 15,
            "Zahlenraum": 15,
        }
        max_punkte = {k: 20 for k in erreichte_punkte}

        self.test_manager.add_test(
            teilnehmer_id=self.participant.teilnehmer_id,
            test_datum="2023-12-01",
            erreichte_punkte=erreichte_punkte,
            max_punkte=max_punkte,
        )
        tests = self.test_manager.get_tests_by_participant(self.participant.teilnehmer_id)
        self.assertEqual(len(tests), 1)
        test = tests[0]
        self.assertAlmostEqual(test.gesamt_prozent, 75.0)

if __name__ == "__main__":
    unittest.main()
  
