import streamlit as st
from modules.data_manager import DataManager
from modules.test_manager import TestManager
from modules.ai_predictor import AIPredictor
from modules.report_generator import ReportGenerator
from database import init_db
import plotly.graph_objs as go

# Initialisiere die Datenbank
init_db()

# Module initialisieren
data_manager = DataManager()
test_manager = TestManager()
ai_predictor = AIPredictor()
report_generator = ReportGenerator()

# Seiten-Layout
st.set_page_config(page_title="Mathematik Kursverwaltung", layout="wide")

# Header
st.title("Mathematik Kursverwaltung")
st.write("Verwalte Teilnehmer, Tests und Prognosen mit interaktiven Visualisierungen und Berichten.")

# Optionen
show_inactive = st.sidebar.checkbox("Inaktive Teilnehmer anzeigen", value=False)
selected_action = st.sidebar.selectbox(
    "Aktion auswählen", 
    ["Teilnehmer hinzufügen", "Teilnehmer bearbeiten", "Testergebnisse eingeben", "Test korrigieren", "KI-Lernen starten", "Bericht generieren"]
)

# Teilnehmer-Tabelle
st.subheader("Teilnehmerübersicht")
participants = data_manager.get_participants(show_inactive)

if participants:
    selected_participant = st.selectbox(
        "Teilnehmer auswählen", 
        options=[f"{p.name} ({p.status})" for p in participants]
    )
    selected_participant_id = participants[[f"{p.name} ({p.status})" for p in participants].index(selected_participant)].teilnehmer_id

    # Aktion basierend auf Auswahl
    if selected_action == "Teilnehmer hinzufügen":
        with st.form("add_participant"):
            name = st.text_input("Name")
            sv_nummer = st.text_input("Sozialversicherungsnummer")
            gender = st.selectbox("Geschlecht", ["Männlich", "Weiblich", "Divers"])
            entry_date = st.date_input("Eintrittsdatum")
            submit = st.form_submit_button("Hinzufügen")
            if submit:
                data_manager.add_participant(name, sv_nummer, gender, entry_date)
                st.success("Teilnehmer erfolgreich hinzugefügt.")
    
    elif selected_action == "Teilnehmer bearbeiten":
        participant = data_manager.get_participant_by_id(selected_participant_id)
        with st.form("edit_participant"):
            name = st.text_input("Name", value=participant.name)
            exit_date = st.date_input("Austrittsdatum", value=participant.austrittsdatum)
            submit = st.form_submit_button("Änderungen speichern")
            if submit:
                data_manager.update_participant(selected_participant_id, name, exit_date)
                st.success("Änderungen erfolgreich gespeichert.")

    elif selected_action == "Testergebnisse eingeben":
        with st.form("add_test"):
            test_date = st.date_input("Testdatum")
            scores = {cat: st.number_input(f"Punkte für {cat}", min_value=0) for cat in ["Brüche", "Textaufgaben", "Raumvorstellung", "Gleichungen", "Grundrechenarten", "Zahlenraum"]}
            submit = st.form_submit_button("Test speichern")
            if submit:
                test_manager.add_test(selected_participant_id, test_date, scores)
                st.success("Test erfolgreich gespeichert.")
    
    elif selected_action == "Test korrigieren":
        test = test_manager.get_latest_test(selected_participant_id)
        with st.form("edit_test"):
            for cat, score in test.items():
                test[cat] = st.number_input(f"Punkte für {cat}", value=score)
            submit = st.form_submit_button("Änderungen speichern")
            if submit:
                test_manager.update_test(test)
                st.success("Testdaten erfolgreich aktualisiert.")
    
    elif selected_action == "KI-Lernen starten":
        ai_predictor.train()
        st.success("KI erfolgreich trainiert.")
    
    elif selected_action == "Bericht generieren":
        report_path = report_generator.generate_report(selected_participant_id)
        st.success(f"Bericht erstellt: [Download]({report_path})")

# Diagramm
st.subheader("Leistungsübersicht")
performance_data = data_manager.get_performance_data(selected_participant_id)
fig = go.Figure()
for category, values in performance_data.items():
    fig.add_trace(go.Scatter(x=values["dates"], y=values["scores"], mode='lines', name=category))
st.plotly_chart(fig)
