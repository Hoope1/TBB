import streamlit as st
from modules.data_manager import DataManager
from modules.test_manager import TestManager
from modules.ai_predictor import AIPredictor
from modules.report_generator import ReportGenerator
import pandas as pd

# Initialisiere Module
data_manager = DataManager()
test_manager = TestManager()
ai_predictor = AIPredictor()
report_generator = ReportGenerator()

# Streamlit-Einstellungen
st.set_page_config(page_title="Mathematik-Kursverwaltung", layout="wide")
st.title("Mathematik-Kursverwaltung")

# Teilnehmerverwaltung
st.header("Teilnehmerverwaltung")
show_inactive = st.checkbox("Inaktive Teilnehmer anzeigen")
participants = data_manager.get_participants(show_inactive)
participants_df = pd.DataFrame([{
    "ID": p.teilnehmer_id,
    "Name": p.name,
    "SV-Nummer": p.sv_nummer,
    "Status": p.status,
    "Alter": p.alter,
    "Eintrittsdatum": p.eintrittsdatum,
    "Austrittsdatum": p.austrittsdatum,
} for p in participants])

st.dataframe(participants_df)

# Teilnehmer hinzufügen
with st.expander("Neuen Teilnehmer hinzufügen"):
    name = st.text_input("Name")
    sv_nummer = st.text_input("SV-Nummer (XXXXDDMMYY)")
    geschlecht = st.selectbox("Geschlecht", ["Männlich", "Weiblich", "Divers"])
    eintrittsdatum = st.date_input("Eintrittsdatum")
    austrittsdatum = st.date_input("Austrittsdatum", value=None)
    if st.button("Teilnehmer hinzufügen"):
        data_manager.add_participant(name, sv_nummer, geschlecht, str(eintrittsdatum), str(austrittsdatum))
        st.success("Teilnehmer hinzugefügt!")

# Tests verwalten
st.header("Testverwaltung")
selected_participant = st.selectbox("Teilnehmer auswählen", participants_df["ID"] if not participants_df.empty else [])
if selected_participant:
    tests = test_manager.get_tests_by_participant(selected_participant)
    tests_df = pd.DataFrame([{
        "Datum": t.test_datum,
        "Gesamt (%)": t.gesamt_prozent,
        "Brüche (%)": t.brueche_erreichte_punkte / t.brueche_max_punkte * 100,
        "Textaufgaben (%)": t.textaufgaben_erreichte_punkte / t.textaufgaben_max_punkte * 100,
        "Raumvorstellung (%)": t.raumvorstellung_erreichte_punkte / t.raumvorstellung_max_punkte * 100,
        "Gleichungen (%)": t.gleichungen_erreichte_punkte / t.gleichungen_max_punkte * 100,
        "Grundrechenarten (%)": t.grundrechenarten_erreichte_punkte / t.grundrechenarten_max_punkte * 100,
        "Zahlenraum (%)": t.zahlenraum_erreichte_punkte / t.zahlenraum_max_punkte * 100,
    } for t in tests])
    st.dataframe(tests_df)

    with st.expander("Neuen Test hinzufügen"):
        test_datum = st.date_input("Testdatum")
        erreichte_punkte = {}
        max_punkte = {}
        for kategorie in ["Brüche", "Textaufgaben", "Raumvorstellung", "Gleichungen", "Grundrechenarten", "Zahlenraum"]:
            erreichte_punkte[kategorie] = st.number_input(f"Erreichte Punkte ({kategorie})", min_value=0, max_value=100, value=0)
            max_punkte[kategorie] = st.number_input(f"Maximale Punkte ({kategorie})", min_value=1, max_value=100, value=100)
        if st.button("Test hinzufügen"):
            test_manager.add_test(selected_participant, str(test_datum), erreichte_punkte, max_punkte)
            st.success("Test hinzugefügt!")

# Prognose anzeigen
st.header("Prognose")
if selected_participant:
    ai_predictor.train_model(selected_participant)
    predictions = ai_predictor.predict(selected_participant)
    if predictions is not None:
        st.line_chart(predictions.set_index("Tag"))

# Bericht erstellen
st.header("Bericht erstellen")
if selected_participant:
    if st.button("Bericht generieren"):
        participant = participants_df[participants_df["ID"] == selected_participant].iloc[0].to_dict()
        tests = pd.DataFrame(test_manager.get_tests_by_participant(selected_participant))
        predictions = ai_predictor.get_predictions(selected_participant)

        pdf_report = report_generator.generate_pdf(participant, tests, predictions)
        st.download_button("PDF-Bericht herunterladen", data=pdf_report, file_name=f"{participant['Name']}-Bericht.pdf")

        excel_report = report_generator.generate_excel(participant, tests, predictions)
        st.download_button("Excel-Bericht herunterladen", data=excel_report, file_name=f"{participant['Name']}-Bericht.xlsx")
      
