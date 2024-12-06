def calculate_percentage(points_obtained, max_points):
    """
    Berechnet den Prozentsatz basierend auf erreichten und maximalen Punkten.
    :param points_obtained: Erreichte Punkte.
    :param max_points: Maximale Punkte.
    :return: Prozentwert als Float oder None, wenn max_points = 0.
    """
    if max_points == 0:
        return None
    return round((points_obtained / max_points) * 100, 2)


def validate_test_scores(test_data):
    """
    Validiert die Testdaten und prüft, ob die maximalen Punkte insgesamt 100 ergeben.
    :param test_data: Dictionary mit 'max_points' für jede Kategorie.
    :return: True, wenn gültig; andernfalls wird eine ValueError ausgelöst.
    """
    total_max_points = sum(test_data.values())
    if total_max_points != 100:
        raise ValueError(f"Die maximalen Punkte aller Kategorien müssen 100 betragen (aktuell: {total_max_points}).")
    return True


def update_participant_status(austrittsdatum):
    """
    Aktualisiert den Status eines Teilnehmers basierend auf seinem Austrittsdatum.
    :param austrittsdatum: Datum des Austritts (YYYY-MM-DD) oder None.
    :return: "Aktiv" oder "Inaktiv".
    """
    from datetime import datetime

    if not austrittsdatum:
        return "Aktiv"
    
    today = datetime.today().date()
    austrittsdatum = datetime.strptime(austrittsdatum, "%Y-%m-%d").date()
    return "Aktiv" if austrittsdatum >= today else "Inaktiv"
