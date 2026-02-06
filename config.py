"""
Configurazione del sistema di assegnazione turni
"""

# File paths
INPUT_CSV = "disponibilità/A&T_Disp_2WheelsPoliTO.csv"

# Parametri turni
NUM_PERSONE_PER_TURNO = 4
NUM_ESPERTI_MINIMI = 1  # Minimo un esperto per turno

# Definizione turni (giorno, fascia)
TURNI = [
    ("Mercoledì", "Mattino"),
    ("Mercoledì", "Pomeriggio"),
    ("Giovedì", "Mattino"),
    ("Giovedì", "Pomeriggio"),
    ("Venerdì", "Mattino"),
    ("Venerdì", "Pomeriggio"),
]

# Colonne CSV
MATRICOLA = "Matricola"
NOME = "Nome"
COGNOME = "Cognome"
ESPERTO = "NEW 2026"  # 1 = nuovo, 0 = esperto

# Mapping giorni -> colonne nel CSV
COLONNE_DISPONIBILITA = {
    "Mercoledì": {
        "Mattino": "Mattino",
        "Pomeriggio": "Pomeriggio"
    },
    "Giovedì": {
        "Mattino": "Mattino",
        "Pomeriggio": "Pomeriggio"
    },
    "Venerdì": {
        "Mattino": "Mattino",
        "Pomeriggio": "Pomeriggio"
    }
}