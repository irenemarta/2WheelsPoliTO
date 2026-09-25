"""
Configurazione del sistema di assegnazione turni
"""
import os
from pathlib import Path

# File paths
INPUT_FOLDER: Path = Path.cwd() / "disponibili"
INPUT_FOLDER.mkdir(exist_ok=True)
NAME_FILE = "SaloneAuto_disp_2WheelsPoliTO.csv"  # MODIFICARE in base all'evento
INPUT_CSV: Path = os.path.join(INPUT_FOLDER, NAME_FILE)
EVENTO: str = 'SALONE_AUTO_2026'  # Nome evento per output

# Parametri turni -> DA MODIFICARE in base alle necessità
NUM_PERSONE_PER_TURNO = 3
# TODO: CORREGGERE NUM_ESPERTI_MINIMI = 0 non funziona
NUM_ESPERTI_MINIMI = 1  # Minimo un esperto per turno

# Definizione turni (giorno, fascia oraria)
# IMPORTANTE: Le fasce devono corrispondere alle chiavi in MAP_COLONNE_DISPONIBILITA
TURNI = [
    ("Venerdì 11 Settembre", "09:00-11:00"),
    ("Venerdì 11 Settembre", "11:00-13:00"),
    ("Venerdì 11 Settembre", "13:00-16:00"),
    ("Venerdì 11 Settembre", "16:00-19:00"),
    ("Sabato 12 Settembre", "09:00-11:00"),
    ("Sabato 12 Settembre", "11:00-13:00"),
    ("Sabato 12 Settembre", "13:00-16:00"),
    ("Sabato 12 Settembre", "16:00-19:00"),
    ("Domenica 13 Settembre", "09:00-11:00"),
    ("Domenica 13 Settembre", "11:00-13:00"),
    ("Domenica 13 Settembre", "13:00-16:00"),
    ("Domenica 13 Settembre", "16:00-19:00"),
]
# Colonne CSV
MATRICOLA = "Matricola"
NOME = "Nome"
COGNOME = "Cognome"
ESPERTO = "NEW 2026"  # 1 = nuovo, 0 = esperto

# Mapping giorni -> fascia -> colonne nel CSV
# IMPORTANTE: Le chiavi devono corrispondere esattamente UGUALI a quelle in TURNI
MAP_COLONNE_DISPONIBILITA = {
    "Venerdì 11 Settembre": {
        "09:00-11:00": "ven 09-11",
        "11:00-13:00": "ven 11-13",
        "13:00-16:00": "ven 13-16",
        "16:00-19:00": "ven 16-19",
    },
    "Sabato 12 Settembre": {
        "09:00-11:00": "sab 09-11",
        "11:00-13:00": "sab 11-13",
        "13:00-16:00": "sab 13-16",
        "16:00-19:00": "sab 16-19",
    },
    "Domenica 13 Settembre": {
        "09:00-11:00": "dom 09-11",
        "11:00-13:00": "dom 11-13",
        "13:00-16:00": "dom 13-16",
        "16:00-19:00": "dom 16-19",
    },
}