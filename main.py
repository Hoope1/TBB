import streamlit as st
import pandas as pd
from modules.data_manager import DataManager
from modules.test_manager import TestManager
from modules.ai_predictor import AIPredictor
from modules.report_generator import ReportGenerator

# Datenbank-Manager initialisieren
data_manager = DataManager()
test_manager = TestManager()
ai_predictor = AIPredictor()
report_generator = ReportGenerator()

# Seitenleiste
st.sidebar.title("Navigation")
page = st.sidebar.radio("Seite auswählen", ["Teilnehmer", "Tests", "Prognosen", "Berichte"])

# Teilnehmerverwaltung
if page == "Teilnehmer":
    st.header("Teilnehmerverwaltung")
    show_inactive = st.checkbox("Inaktive Teilnehmer anzeigen")
    participants = data_manager.get_participants(show_inactive)
    participants_df = pd.DataFrame([{
        "ID": p.teilnehmer_id,
        "Name": p.name,
        "Status": p.status
    } for p in participants])
    st.write(participants_df)

    with st.form("add_participant_form"):
        st.subheader("Neuen Teilnehmer hinzufügen")
        name = st.text_input("Name")
        sv_nummer = st.text_input("Sozialversicherungsnummer")
        geburtsdatum = st.date_input("Geburtsdatum")
        geschlecht = st.selectbox("Geschlecht", ["Männlich", "Weiblich", "Divers"])
        eintrittsdatum = st.date_input("Eintrittsdatum")
        if st.form_submit_button("Hinzufügen"):
            data_manager.add_participant(name, sv_nummer, geburtsdatum, geschlecht, eintrittsdatum)
            st.success("Teilnehmer erfolgreich hinzugefügt!")

# Testverwaltung
elif page == "Tests":
    st.header("Testverwaltung")
    teilnehmer_id = st.number_input("Teilnehmer-ID", min_value=1, step=1)
    tests = test_manager.get_tests_for_participant(teilnehmer_id)
    tests_df = pd.DataFrame([{
        "Datum": t.test_datum,
        "Gesamtpunkte": t.gesamt_erreichte_punkte,
        "Prozent": t.gesamt_prozent
    } for t in tests])
    st.write(tests_df)

    with st.form("add_test_form"):
        st.subheader("Neuen Test hinzufügen")
        test_datum = st.date_input("Testdatum")
        results = {
            "brueche_erreichte_punkte": st.number_input("Brüche (erreichte Punkte)", min_value=0, step=1),
            "brueche_max_punkte": st.number_input("Brüche (max Punkte)", min_value=0, step=1),
            "textaufgaben_erreichte_punkte": st.number_input("Textaufgaben (erreichte Punkte)", min_value=0, step=1),
            "textaufgaben_max_punkte": st.number_input("Textaufgaben (max Punkte)", min_value=0, step=1),
            "raumvorstellung_erreichte_punkte": st.number_input("Raumvorstellung (erreichte Punkte)", min_value=0, step=1),
            "raumvorstellung_max_punkte": st.number_input("Raumvorstellung (max Punkte)", min_value=0, step=1),
            "gleichungen_erreichte_punkte": st.number_input("Gleichungen (erreichte Punkte)", min_value=0, step=1),
            "gleichungen_max_punkte": st.number_input("Gleichungen (max Punkte)", min_value=0, step=1),
            "grundrechenarten_erreichte_punkte": st.number_input("Grundrechenarten (erreichte Punkte)", min_value=0, step=1),
            "grundrechenarten_max_punkte": st.number_input("Grundrechenarten (max Punkte)", min_value=0, step=1),
            "zahlenraum_erreichte_punkte": st.number_input("Zahlenraum (erreichte Punkte)", min_value=0, step=1),
            "zahlenraum_max_punkte": st.number_input("Zahlenraum (max Punkte)", min_value=0, step=1)
        }
        if st.form_submit_button("Hinzufügen"):
            test_manager.add_test(teilnehmer_id, test_datum, results)
            st.success("Test erfolgreich hinzugefügt!")

# Prognoseverwaltung
elif page == "Prognosen":
    st.header("Prognoseverwaltung")
    teilnehmer_id = st.number_input("Teilnehmer-ID", min_value=1, step=1)
    predictions = ai_predictor.get_predictions_for_participant(teilnehmer_id)
    predictions_df = pd.DataFrame([{
        "Tag": p.tag,
        "Prognose Gesamt": p.gesamt_prognose
    } for p in predictions])
    st.write(predictions_df)

# Berichtsgenerierung
elif page == "Berichte":
    st.header("Berichtsgenerierung")
    teilnehmer_id = st.number_input("Teilnehmer-ID", min_value=1, step=1)
    report = report_generator.generate_report(teilnehmer_id)
    if report:
        st.subheader("Bericht")
        st.write("Name:", report["Name"])
        st.write("Tests:", report["Tests"])
        st.write("Prognosen:", report["Prognosen"])
    else:
        st.warning("Kein Bericht für diesen Teilnehmer gefunden!")
