import streamlit as st

def setup_layout():
    """
    Initialisiert das Layout der Benutzeroberfläche.
    """
    # Seitenkonfiguration
    st.set_page_config(
        page_title="Mathematik Kursverwaltung",
        page_icon="📊",
        layout="wide",
    )

    # Titel und Untertitel
    st.title("📊 Mathematik Kursverwaltung")
    st.markdown("Verwalte Teilnehmer, Testergebnisse und KI-Prognosen.")

    # Layout-Aufteilung
    with st.sidebar:
        st.header("Navigation")
        st.radio("Menü:", ["Teilnehmer", "Testergebnisse", "Prognosen", "Berichte"])

    # Hauptcontainer
    st.container()

def display_table(data, title="Tabelle"):
    """
    Zeigt eine Tabelle in der Benutzeroberfläche an.
    :param data: DataFrame oder Liste von Dictionaries.
    :param title: Titel der Tabelle.
    """
    st.subheader(title)
    st.dataframe(data, use_container_width=True)

def display_buttons(buttons):
    """
    Zeigt eine Reihe von Buttons an.
    :param buttons: Liste von Button-Beschriftungen.
    :return: Der Name des geklickten Buttons oder None.
    """
    st.write("### Aktionen")
    col1, col2, col3, col4 = st.columns(4)
    actions = [None]
    for i, button in enumerate(buttons):
        with [col1, col2, col3, col4][i % 4]:
            if st.button(button):
                actions.append(button)
    return next((action for action in actions if action), None)
