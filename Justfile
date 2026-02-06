# Variabili
python := "uv run"
VENV_DIR := ".venv"
REQUIREMENTS_FILE := "requirements.txt"

# Defualt task
default: help


# Installazione delle dipendenze
setup:
    uv sync
    @echo "Setup completato. Virtual environment creaato e dipendenze installate."

make-turni:
    @echo "Generazione dei turni in corso..."
    {{python}} main.py
    @echo "Turni generati con successo."

# Pulizia dei file temporanei
clean:
    rm -rf programmi/__pycache__
    find . -type d -name __pycache__ -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete

help:
    @echo "Comandi disponibili:"
    @echo "  setup         - Crea un virtual environment e installa le dipendenze."
    @echo "  make-turni   - Genera i turni utilizzando lo script principale."
    @echo "  clean        - Rimuove i file temporanei e le cache di Python."