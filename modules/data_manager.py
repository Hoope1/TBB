from sqlalchemy.orm import Session
from database import Teilnehmer, SessionLocal
from datetime import datetime

class DataManager:
    """
    Diese Klasse verwaltet Teilnehmerdaten in der Datenbank.
    """

    def __init__(self):
        self.db: Session = SessionLocal()

    def add_participant(self, name, sv_nummer, geschlecht, eintrittsdatum, austrittsdatum=None):
        """
        Fügt einen neuen Teilnehmer zur Datenbank hinzu.

        Args:
            name (str): Name des Teilnehmers.
            sv_nummer (str): Sozialversicherungsnummer (Format: XXXXDDMMYY).
            geschlecht (str): Geschlecht des Teilnehmers.
            eintrittsdatum (str): Eintrittsdatum (YYYY-MM-DD).
            austrittsdatum (str, optional): Austrittsdatum (YYYY-MM-DD).
        """
        geburtsdatum = self._extract_birthdate_from_sv(sv_nummer)
        alter = self._calculate_age(geburtsdatum)
        status = "Aktiv" if not austrittsdatum or datetime.strptime(austrittsdatum, "%Y-%m-%d").date() > datetime.now().date() else "Inaktiv"

        new_participant = Teilnehmer(
            name=name,
            sv_nummer=sv_nummer,
            geburtsdatum=geburtsdatum,
            geschlecht=geschlecht,
            eintrittsdatum=datetime.strptime(eintrittsdatum, "%Y-%m-%d").date(),
            austrittsdatum=datetime.strptime(austrittsdatum, "%Y-%m-%d").date() if austrittsdatum else None,
            alter=alter,
            status=status,
        )
        self.db.add(new_participant)
        self.db.commit()

    def update_austrittsdatum(self, teilnehmer_id, neues_austrittsdatum):
        """
        Aktualisiert das Austrittsdatum eines Teilnehmers.

        Args:
            teilnehmer_id (int): Die ID des Teilnehmers.
            neues_austrittsdatum (str): Das neue Austrittsdatum (YYYY-MM-DD).
        """
        participant = self.db.query(Teilnehmer).filter_by(teilnehmer_id=teilnehmer_id).first()
        if participant:
            participant.austrittsdatum = datetime.strptime(neues_austrittsdatum, "%Y-%m-%d").date()
            participant.berechne_status()
            self.db.commit()

    def get_participants(self, show_inactive=False):
        """
        Ruft die Teilnehmerliste ab.

        Args:
            show_inactive (bool): Wenn True, werden auch inaktive Teilnehmer angezeigt.

        Returns:
            list: Liste der Teilnehmer.
        """
        if show_inactive:
            return self.db.query(Teilnehmer).all()
        return self.db.query(Teilnehmer).filter_by(status="Aktiv").all()

    def delete_participant(self, teilnehmer_id):
        """
        Löscht einen Teilnehmer aus der Datenbank.

        Args:
            teilnehmer_id (int): Die ID des Teilnehmers.
        """
        participant = self.db.query(Teilnehmer).filter_by(teilnehmer_id=teilnehmer_id).first()
        if participant:
            self.db.delete(participant)
            self.db.commit()

    @staticmethod
    def _extract_birthdate_from_sv(sv_nummer):
        """
        Extrahiert das Geburtsdatum aus der Sozialversicherungsnummer.

        Args:
            sv_nummer (str): Sozialversicherungsnummer (Format: XXXXDDMMYY).

        Returns:
            datetime.date: Geburtsdatum.
        """
        dd = int(sv_nummer[4:6])
        mm = int(sv_nummer[6:8])
        yy = int(sv_nummer[8:10])
        yy += 2000 if yy <= datetime.now().year % 100 else 1900  # Berücksichtige Jahrhundertwechsel
        return datetime(yy, mm, dd).date()

    @staticmethod
    def _calculate_age(geburtsdatum):
        """
        Berechnet das Alter basierend auf dem Geburtsdatum.

        Args:
            geburtsdatum (datetime.date): Geburtsdatum.

        Returns:
            int: Alter in Jahren.
        """
        today = datetime.now().date()
        return today.year - geburtsdatum.year - ((today.month, today.day) < (geburtsdatum.month, geburtsdatum.day))
      
