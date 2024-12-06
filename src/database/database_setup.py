import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

def initialize_database(db_path="data/database.db"):
    """
    Initialisiert die SQLite-Datenbank und erstellt alle Tabellen.
    :param db_path: Pfad zur SQLite-Datenbankdatei.
    :return: SessionMaker-Objekt für Datenbankoperationen.
    """
    # Sicherstellen, dass das Datenverzeichnis existiert
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Datenbank-Engine erstellen
    engine = create_engine(f"sqlite:///{db_path}")
    
    # Tabellenstruktur erstellen, falls nicht vorhanden
    Base.metadata.create_all(engine)

    # SessionMaker für den Zugriff auf die Datenbank konfigurieren
    Session = sessionmaker(bind=engine)
    return Session

# Beispiel für eine Datenbankinitialisierung
if __name__ == "__main__":
    session = initialize_database()()
    print("Datenbank wurde initialisiert.")
  
