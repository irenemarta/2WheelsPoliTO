"""
Configurazione del sistema di assegnazione turni
"""

# File paths
INPUT_CSV = "disponibili/A&T_Disp_2WheelsPoliTO.csv"
EVENTO = 'A&T_2026'  # Nome evento per output

# Parametri turni
NUM_PERSONE_PER_TURNO = 7
NUM_ESPERTI_MINIMI = 1  # Minimo un esperto per turno

# Definizione turni (giorno, fascia oraria)
# IMPORTANTE: Le fasce devono corrispondere alle chiavi in COLONNE_DISPONIBILITA
TURNI = [
    ("Mercoledì", "9:30 - 13"),
    ("Mercoledì", "13 - 17"),
    ("Giovedì", "9:30 - 13"),
    ("Giovedì", "13 - 17"),
    ("Venerdì", "9:30 - 13"),
    ("Venerdì", "13 - 17"),
]
# Colonne CSV
MATRICOLA = "Matricola"
NOME = "Nome"
COGNOME = "Cognome"
ESPERTO = "NEW 2026"  # 1 = nuovo, 0 = esperto

# Mapping giorni -> colonne nel CSV
# IMPORTANTE: Le chiavi devono corrispondere esattamente UGUALI a quelle in TURNI
MAP_COLONNE_DISPONIBILITA = {
    "Mercoledì": {
        "9:30 - 13": "MeMatt",      # Colonna CSV per mercoledì 9:30-13
        "13 - 17": "MePom"          # Colonna CSV per mercoledì 13-17
    },
    "Giovedì": {
        "9:30 - 13": "GioMatt",     # Colonna CSV per giovedì 9:30-13
        "13 - 17": "GioPomm"        # Colonna CSV per giovedì 13-17
    },
    "Venerdì": {
        "9:30 - 13": "VeMatt",      # Colonna CSV per venerdì 9:30-13
        "13 - 17": "VePom"          # Colonna CSV per venerdì 13-17
    }
}