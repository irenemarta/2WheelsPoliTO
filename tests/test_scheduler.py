"""
Test per la logica di selezione turni in scheduler.py
"""

import pandas as pd
import pytest

import config
from scheduler import seleziona_turno


def crea_persone(prefisso: str, n: int, esperto: str) -> list[dict]:
    """Genera n righe finte di persone (esperti o nuovi) per i test."""
    return [
        {
            config.MATRICOLA: f"{prefisso}{i}",
            config.NOME: f"Nome{i}",
            config.COGNOME: f"Cognome{i}",
            config.ESPERTO: esperto,
        }
        for i in range(n)
    ]


@pytest.fixture
def df_disponibili() -> pd.DataFrame:
    """5 esperti + 5 nuovi, tutti disponibili per il turno."""
    righe = crea_persone("esp", 5, "NO") + crea_persone("new", 5, "SI")
    return pd.DataFrame(righe)


def test_seleziona_numero_corretto_di_persone(df_disponibili):
    df_selezionati, errore = seleziona_turno(
        df_disponibili, persone_gia_assegnate={}, num_persone=4, num_esperti=1
    )

    assert errore is None
    assert len(df_selezionati) == 4


def test_seleziona_almeno_il_numero_minimo_di_esperti(df_disponibili):
    df_selezionati, errore = seleziona_turno(
        df_disponibili, persone_gia_assegnate={}, num_persone=4, num_esperti=1
    )

    num_esperti_selezionati = (df_selezionati[config.ESPERTO] == "NO").sum()
    assert errore is None
    assert num_esperti_selezionati >= 1


def test_errore_se_non_ci_sono_abbastanza_esperti():
    solo_nuovi = pd.DataFrame(crea_persone("new", 5, "SI"))

    df_selezionati, errore = seleziona_turno(
        solo_nuovi, persone_gia_assegnate={}, num_persone=4, num_esperti=1
    )

    assert df_selezionati is None
    assert errore is not None


def test_errore_se_non_ci_sono_abbastanza_persone_disponibili(df_disponibili):
    df_selezionati, errore = seleziona_turno(
        df_disponibili, persone_gia_assegnate={}, num_persone=100, num_esperti=1
    )

    assert df_selezionati is None
    assert errore is not None