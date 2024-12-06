from sqlalchemy.orm import Session
from database import Teilnehmer, SessionLocal
from datetime import datetime

class DataManager:
    def __init__(self):
        self.db = SessionLocal()

    def get_participants(self, show_inactive=False):
        """
        Gibt eine Liste von Teilnehmern zurück. Optional können auch inaktive Teilnehmer angezeigt werden.
        """
        if show_inactive:
            return self.db.query(Teilnehmer).all()
        return self.db.query(Teilnehmer).filter_by(status="Aktiv").all()

    def add_participant(self, name, sv_nummer, geburtsdatum, geschlecht, eintrittsdatum):
        """
        Fügt einen neuen Teilnehmer hinzu.
        """
        alter = datetime.now().year - geburtsdatum.year
        new_participant = Teilnehmer(
            name=name,
            sv_nummer=sv_nummer,
            geburtsdatum=geburtsdatum,
            geschlecht=geschlecht,
            eintrittsdatum=eintrittsdatum,
            alter=alter,
            status="Aktiv"
        )
        self.db.add(new_participant)
        self.db.commit()

    def delete_participant(self, teilnehmer_id):
        """
        Löscht einen Teilnehmer anhand seiner ID.
        """
        participant = self.db.query(Teilnehmer).filter_by(teilnehmer_id=teilnehmer_id).first()
        if participant:
            self.db.delete(participant)
            self.db.commit()

    def update_participant_status(self):
        """
        Aktualisiert den Status aller Teilnehmer basierend auf ihrem Austrittsdatum.
        """
        participants = self.db.query(Teilnehmer).all()
        for participant in participants:
            participant.berechne_status()
        self.db.commit()
