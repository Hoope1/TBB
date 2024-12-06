import streamlit as st
from datetime import datetime

def participant_form(on_submit):
    """
    Formular zur Eingabe oder Bearbeitung von Teilnehmerdaten.
    :param on_submit: Callback-Funktion, die mit den eingegebenen Daten aufgerufen wird.
    """
    st.write("### Teilnehmer hinzufügen/bearbeiten")
    name = st.text_input("Name", placeholder="Vor- und Nachname")
    sv_nummer = st.text_input("Sozialversicherungsnummer", placeholder="XXXXXXXXDDMMYY")
    geschlecht = st.selectbox("Geschlecht", ["Männlich", "Weiblich", "Divers"])
    eintrittsdatum = st.date_input("Eintrittsdatum", value=datetime.today())
    austrittsdatum = st.date_input("Austrittsdatum", value=None, key="austrittsdatum")
    
    if st.button("Speichern"):
        if not name or not sv_nummer:
            st.error("Name und Sozialversicherungsnummer sind Pflichtfelder!")
        else:
            on_submit({
                "name": name,
                "sv_nummer": sv_nummer,
                "geschlecht": geschlecht,
                "eintrittsdatum": eintrittsdatum,
                "austrittsdatum": austrittsdatum if austrittsdatum else None,
            })

def test_form(on_submit):
    """
    Formular zur Eingabe von Testergebnissen.
    :param on_submit: Callback-Funktion, die mit den eingegebenen Daten aufgerufen wird.
    """
    st.write("### Testergebnisse eingeben")
    test_datum = st.date_input("Testdatum", value=datetime.today())
    categories = [
        "Brüche", "Textaufgaben", "Raumvorstellung", 
        "Gleichungen", "Grundrechenarten", "Zahlenraum"
    ]

    results = {}
    for category in categories:
        col1, col2 = st.columns(2)
        with col1:
            erreichte_punkte = st.number_input(
                f"{category} - Erreichte Punkte", min_value=0, value=0, step=1, key=f"{category}_erreicht"
            )
        with col2:
            max_punkte = st.number_input(
                f"{category} - Maximale Punkte", min_value=0, value=0, step=1, key=f"{category}_max"
            )
        results[category] = (erreichte_punkte, max_punkte)

    if st.button("Speichern"):
        if sum([max_p for _, max_p in results.values()]) != 100:
            st.error("Die Summe der maximalen Punkte muss 100 betragen!")
        else:
            on_submit({
                "test_datum": test_datum,
                "results": results,
            })
          
