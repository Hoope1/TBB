import streamlit as st
from src.database.database_setup import initialize_database
from src.database.models import Participant, Test
from src.logic.calculations import calculate_percentage, update_participant_status
from src.logic.predictions import train_model, generate_predictions
from src.ui.layout import setup_layout, display_table, display_buttons
from src.ui.forms import participant_form, test_form

# Initialisierung der Datenbank
Session = initialize_database()
session = Session()

# Layout der Anwendung konfigurieren
setup_layout()

# Navigation
menu = st.sidebar.radio("Navigation", ["Teilnehmer", "Testergebnisse", "Prognosen", "Berichte"])

if menu == "Teilnehmer":
    st.header("Teilnehmerverwaltung")

    # Teilnehmerliste anzeigen
    participants = session.query(Participant).all()
    participant_data = [
        {
            "Name": p.name,
            "SV-Nummer": p.sv_nummer,
            "Geschlecht": p.geschlecht,
            "Eintritt": p.eintrittsdatum,
            "Austritt": p.austrittsdatum,
            "Status": update_participant_status(p.austrittsdatum),
        }
        for p in participants
    ]
    display_table(participant_data, title="Teilnehmer")

    # Teilnehmer-Formular
    def on_participant_submit(data):
        new_participant = Participant(
            name=data["name"],
            sv_nummer=data["sv_nummer"],
            geschlecht=data["geschlecht"],
            eintrittsdatum=data["eintrittsdatum"],
            austrittsdatum=data["austrittsdatum"],
        )
        session.add(new_participant)
        session.commit()
        st.success("Teilnehmer erfolgreich hinzugefügt!")

    participant_form(on_submit=on_participant_submit)

elif menu == "Testergebnisse":
    st.header("Testergebnisse")

    # Testergebnisse-Formular
    def on_test_submit(data):
        test = Test(
            teilnehmer_id=1,  # Beispielhafte Zuordnung
            test_datum=data["test_datum"],
            brueche_erreichte_punkte=data["results"]["Brüche"][0],
            brueche_max_punkte=data["results"]["Brüche"][1],
            # (weitere Kategorien hier hinzufügen)
        )
        session.add(test)
        session.commit()
        st.success("Testergebnisse erfolgreich hinzugefügt!")

    test_form(on_submit=on_test_submit)

elif menu == "Prognosen":
    st.header("Prognosen")

    # Beispielhafte Prognosen-Logik
    st.write("Hier könnten die Prognosen angezeigt und aktualisiert werden.")

elif menu == "Berichte":
    st.header("Berichte")

    # Beispielhafter Bericht-Generierungsbereich
    st.write("Hier könnten PDF-Berichte generiert werden.")
  
