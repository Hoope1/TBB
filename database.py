from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Basis-Klasse für ORM-Modelle
Base = declarative_base()

# Tabelle: Teilnehmer
class Teilnehmer(Base):
    __tablename__ = "teilnehmer"

    teilnehmer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    sv_nummer = Column(String, unique=True, nullable=False)
    geburtsdatum = Column(Date, nullable=False)
    geschlecht = Column(String, nullable=False)
    eintrittsdatum = Column(Date, nullable=False)
    austrittsdatum = Column(Date)
    alter = Column(Integer, nullable=False)
    status = Column(String, nullable=False)

    # Beziehungen zu anderen Tabellen
    tests = relationship("Test", back_populates="teilnehmer")
    prognosen = relationship("Prognose", back_populates="teilnehmer")

    def berechne_status(self):
        """Status (Aktiv/Inaktiv) basierend auf dem Austrittsdatum berechnen."""
        self.status = "Aktiv" if not self.austrittsdatum or self.austrittsdatum > datetime.now().date() else "Inaktiv"


# Tabelle: Tests
class Test(Base):
    __tablename__ = "tests"

    test_id = Column(Integer, primary_key=True, autoincrement=True)
    teilnehmer_id = Column(Integer, ForeignKey("teilnehmer.teilnehmer_id"), nullable=False)
    test_datum = Column(Date, nullable=False)

    brueche_erreichte_punkte = Column(Integer, nullable=False)
    brueche_max_punkte = Column(Integer, nullable=False)
    textaufgaben_erreichte_punkte = Column(Integer, nullable=False)
    textaufgaben_max_punkte = Column(Integer, nullable=False)
    raumvorstellung_erreichte_punkte = Column(Integer, nullable=False)
    raumvorstellung_max_punkte = Column(Integer, nullable=False)
    gleichungen_erreichte_punkte = Column(Integer, nullable=False)
    gleichungen_max_punkte = Column(Integer, nullable=False)
    grundrechenarten_erreichte_punkte = Column(Integer, nullable=False)
    grundrechenarten_max_punkte = Column(Integer, nullable=False)
    zahlenraum_erreichte_punkte = Column(Integer, nullable=False)
    zahlenraum_max_punkte = Column(Integer, nullable=False)

    gesamt_erreichte_punkte = Column(Integer)
    gesamt_max_punkte = Column(Integer, default=100)
    gesamt_prozent = Column(Float)

    teilnehmer = relationship("Teilnehmer", back_populates="tests")

    def berechne_prozentwerte(self):
        """Prozentwerte für jede Kategorie und insgesamt berechnen."""
        self.gesamt_erreichte_punkte = (
            self.brueche_erreichte_punkte +
            self.textaufgaben_erreichte_punkte +
            self.raumvorstellung_erreichte_punkte +
            self.gleichungen_erreichte_punkte +
            self.grundrechenarten_erreichte_punkte +
            self.zahlenraum_erreichte_punkte
        )
        self.gesamt_prozent = (self.gesamt_erreichte_punkte / self.gesamt_max_punkte) * 100


# Tabelle: Prognosen
class Prognose(Base):
    __tablename__ = "prognosen"

    prognose_id = Column(Integer, primary_key=True, autoincrement=True)
    teilnehmer_id = Column(Integer, ForeignKey("teilnehmer.teilnehmer_id"), nullable=False)
    prognose_datum = Column(Date, nullable=False)
    tag = Column(Integer, nullable=False)

    brueche_prognose = Column(Float)
    textaufgaben_prognose = Column(Float)
    raumvorstellung_prognose = Column(Float)
    gleichungen_prognose = Column(Float)
    grundrechenarten_prognose = Column(Float)
    zahlenraum_prognose = Column(Float)
    gesamt_prognose = Column(Float)

    teilnehmer = relationship("Teilnehmer", back_populates="prognosen")


# Datenbank-Setup
DATABASE_URL = "sqlite:///math_course.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialisiert die Datenbank und erstellt alle Tabellen."""
    Base.metadata.create_all(bind=engine)


# Beispiel, um die Datenbank zu initialisieren
if __name__ == "__main__":
    init_db()
    print("Datenbank wurde erfolgreich initialisiert.")
