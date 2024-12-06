import logging
import os

def setup_logging(log_dir="logs"):
    """Set up logging configuration."""
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Logging für allgemeine Informationen
    logging.basicConfig(
        filename=os.path.join(log_dir, "app.log"),
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Logger für Fehler
    error_logger = logging.getLogger("error_logger")
    error_handler = logging.FileHandler(os.path.join(log_dir, "error.log"))
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))
    error_logger.addHandler(error_handler)

    return logging, error_logger
