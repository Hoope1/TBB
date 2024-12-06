from datetime import datetime

def calculate_age(sv_nummer):
    """
    Berechnet das Alter basierend auf den letzten sechs Ziffern der SV-Nummer (Format: DDMMYY).
    :param sv_nummer: Sozialversicherungsnummer im Format XXXXXXXXDDMMYY.
    :return: Alter als Integer.
    """
    try:
        birth_date_str = sv_nummer[-6:]
        birth_date = datetime.strptime(birth_date_str, "%d%m%y")
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except ValueError:
        raise ValueError("Ungültige SV-Nummer: Kann kein Geburtsdatum extrahieren.")

def calculate_status(austrittsdatum):
    """
    Berechnet den Status eines Teilnehmers basierend auf dem Austrittsdatum.
    :param austrittsdatum: Datum, an dem der Teilnehmer den Kurs verlässt (YYYY-MM-DD) oder None.
    :return: "Aktiv" oder "Inaktiv".
    """
    if not austrittsdatum:
        return "Aktiv"
    today = datetime.today().date()
    austrittsdatum = datetime.strptime(austrittsdatum, "%Y-%m-%d").date()
    return "Aktiv" if austrittsdatum >= today else "Inaktiv"

def format_date(date_str):
    """
    Formatiert ein Datum im Format YYYY-MM-DD in TT.MM.JJJJ.
    :param date_str: Datum im Format YYYY-MM-DD.
    :return: Formatiertes Datum als String.
    """
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d.%m.%Y")
    except ValueError:
        raise ValueError("Ungültiges Datumsformat: Erwartet YYYY-MM-DD.")
