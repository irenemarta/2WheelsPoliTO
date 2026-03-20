"""
Modulo per caricamento e gestione dati di input
"""
import pandas as pd
from typing import List
from models import Persona
import config


def get_data_persone(filepath: str) -> List[Persona]:
    """
    Args:
        filepath: percorso del file CSV
        
    Returns:
        Lista di oggetti Persona
    """
    df = pd.read_csv(filepath, sep=";", encoding="utf-8").fillna(0)

    df['MeMatt'] = df['MeMatt'].rename('Mercoledì Mattino').astype(int)
    df['MePom'] = df['MePom'].rename('Mercoledì Pomeriggio').astype(int)
    df['GioMatt'] = df['GioMatt'].rename('Giovedì Mattino').astype(int)
    df['GioPomm'] = df['GioPomm'].rename('Giovedì Pomeriggio').astype(int)
    df['VeMatt'] = df['VeMatt'].rename('Venerdì Mattino').astype(int)
    df['VePom'] = df['VePom'].rename('Venerdì Pomeriggio').astype(int)

    if df['NEW 2026'] == 'SI':
        df['NEW 2026'] = 1
    else:
        df['NEW 2026'] = 0
    
    persone = []
    for idx, row in df.iterrows():
        persona = Persona(
            matricola=str(row[config.MATRICOLA]),
            nome=row[config.NOME],
            cognome=row[config.COGNOME],
            new_entry=(row[config.ESPERTO])  # 0 = esperto, 1 = nuovo
        )
        persone.append(persona)
    
    return persone


def filtra_disponibili(
    df: pd.DataFrame,
    giorno: str,
    fascia: str
) -> pd.DataFrame:
    """
    Filtra il DataFrame per ottenere solo le persone disponibili per un dato turno
    
    Args:
        df: DataFrame completo
        giorno: nome del giorno (es. "Mercoledì")
        fascia: "Mattino" o "Pomeriggio"
        
    Returns:
        DataFrame filtrato con solo i disponibili
    """
    disponibilità = config.MAP_COLONNE_DISPONIBILITA[giorno][fascia]
    return df[df[disponibili] == 1].copy()


def separa_esperti(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Args:
        df: DataFrame da separare
        
    Returns:
        (df_nuovi, df_esperti)
    """
    # NEW 2026: 1 = nuovo, 0 = esperto
    nuovi = df[df[config.ESPERTO].astype(str) == "SI"].copy()
    esperti = df[df[config.ESPERTO].astype(str) == "NO"].copy()
    return nuovi, esperti
