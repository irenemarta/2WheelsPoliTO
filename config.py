"""
Configurazione del sistema di assegnazione turni
"""

# File paths
INPUT_CSV = "disponibili/Biennale_disp_2WheelsPoliTO.csv"
EVENTO = 'BIENNALE_TECNOLOGIA_2026'  # Nome evento per output

# Parametri turni
NUM_PERSONE_PER_TURNO = 6
NUM_ESPERTI_MINIMI = 1  # Minimo un esperto per turno

# Definizione turni (giorno, fascia oraria)
# IMPORTANTE: Le fasce devono corrispondere alle chiavi in COLONNE_DISPONIBILITA
TURNI = [
    ("Mattina", "7:00 - 10:00"),
    ("Mattina", "10:00 - 13:00"),
    ("Pomeriggio", "13:00 - 16:00"),
    ("Pomeriggio", "16:00 - 19:30")
]
# Colonne CSV
MATRICOLA = "Matricola"
NOME = "Nome"
COGNOME = "Cognome"
ESPERTO = "NEW"  # 1 = nuovo, 0 = esperto

# Mapping giorni -> colonne nel CSV
# IMPORTANTE: Le chiavi devono corrispondere esattamente UGUALI a quelle in TURNI
MAP_COLONNE_DISPONIBILITA = {
    "Mattina": {
        "7:00 - 10:00": "Mattina 7:00-10:00",
        "10:00 - 13:00": "Mattina 10:00-13:00"
    },
    "Pomeriggio": {
        "13:00 - 16:00": "Pomeriggio 13:00-16:00",
        "16:00 - 19:30": "Pomeriggio 16:00-19:30"
    },
}