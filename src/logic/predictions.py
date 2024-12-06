import pandas as pd
from pycaret.regression import setup, compare_models, predict_model, save_model, load_model

def train_model(data, target_column="gesamt_prozent", model_path="models/best_model"):
    """
    Trainiert ein ML-Modell mit PyCaret und speichert das beste Modell.
    :param data: Pandas DataFrame mit Trainingsdaten.
    :param target_column: Zielvariable für das Training.
    :param model_path: Speicherort für das beste Modell.
    :return: Name des besten Modells.
    """
    # PyCaret-Setup
    ml_setup = setup(data, target=target_column, silent=True, session_id=42)
    best_model = compare_models()
    save_model(best_model, model_path)
    return str(best_model)


def generate_predictions(model_path, data):
    """
    Erzeugt Prognosen basierend auf einem gespeicherten Modell.
    :param model_path: Pfad zum gespeicherten Modell.
    :param data: Pandas DataFrame mit Eingabedaten für Prognosen.
    :return: DataFrame mit Prognosen.
    """
    model = load_model(model_path)
    predictions = predict_model(model, data=data)
    return predictions


def incremental_learning(new_data, model_path="models/best_model"):
    """
    Führt inkrementelles Lernen durch, indem ein gespeichertes Modell mit neuen Daten aktualisiert wird.
    :param new_data: Neue Daten als Pandas DataFrame.
    :param model_path: Pfad zum gespeicherten Modell.
    :return: Name des aktualisierten Modells.
    """
    model = load_model(model_path)
    retrained_model = setup(new_data, target="gesamt_prozent", silent=True, session_id=42)
    best_model = compare_models()
    save_model(best_model, model_path)
    return str(best_model)
