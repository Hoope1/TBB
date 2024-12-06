import unittest
from modules.data_manager import DataManager
from datetime import datetime

class TestDataManager(unittest.TestCase):
    def setUp(self):
        self.manager = DataManager()

    def test_add_participant(self):
        self.manager.add_participant(
            name="Max Mustermann",
            sv_nummer="1234010190",
            geschlecht="Männlich",
            eintrittsdatum="2023-01-01",
            austrittsdatum="2024-01-01"
        )
        participants = self.manager.get_participants()
        self.assertEqual(len(participants), 1)
        participant = participants[0]
        self.assertEqual(participant.name, "Max Mustermann")
        self.assertEqual(participant.status, "Aktiv")

    def test_update_austrittsdatum(self):
        self.manager.add_participant(
            name="Anna Musterfrau",
            sv_nummer="1234010191",
            geschlecht="Weiblich",
            eintrittsdatum="2023-01-01",
            austrittsdatum="2023-06-01"
        )
        participant = self.manager.get_participants()[0]
        self.manager.update_austrittsdatum(participant.teilnehmer_id, "2024-01-01")
        updated_participant = self.manager.get_participants()[0]
        self.assertEqual(updated_participant.austrittsdatum.strftime("%Y-%m-%d"), "2024-01-01")
        self.assertEqual(updated_participant.status, "Aktiv")

if __name__ == "__main__":
    unittest.main()
