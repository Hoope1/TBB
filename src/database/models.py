from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Participant(Base):
    """
    Tabelle für Teilnehmer.
    """
    __tablename__ = "teilnehmer"
    teilnehmer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    sv_nummer = Column(String, nullable=False)
    geburtsdatum = Column(Date)
    geschlecht = Column(String, nullable=False)
    eintrittsdatum = Column(Date, nullable=False)
    austrittsdatum = Column(Date, nullable=True)
    status = Column(String)

    tests = relationship("Test", back_populates="participant")
    prognosen = relationship("Prediction", back_populates="participant")


class Test(Base):
    """
    Tabelle für Testergebnisse.
    """
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
    gesamt_prozent = Column(Float)

    participant = relationship("Participant", back_populates="tests")


class Prediction(Base):
    """
    Tabelle für KI-Prognosen.
    """
    __tablename__ = "prognosen"
    prognose_id = Column(Integer, primary_key=True, autoincrement=True)
    teilnehmer_id = Column(Integer, ForeignKey("teilnehmer.teilnehmer_id"), nullable=False)
    prognose_datum = Column(Date, nullable=False)
    brueche_prognose = Column(Float, nullable=False)
    textaufgaben_prognose = Column(Float, nullable=False)
    raumvorstellung_prognose = Column(Float, nullable=False)
    gleichungen_prognose = Column(Float, nullable=False)
    grundrechenarten_prognose = Column(Float, nullable=False)
    zahlenraum_prognose = Column(Float, nullable=False)
    gesamt_prognose = Column(Float, nullable=False)

    participant = relationship("Participant", back_populates="prognosen")
  
