"""
Logica di assegnazione turni
"""

import pandas as pd
from typing import Dict, Optional, Tuple, List
from models import Persona, Turno
from data_loader import separa_esperti
import config


def seleziona_turno(
    df_disponibili: pd.DataFrame,
    persone_gia_assegnate: Dict[str, int],
    num_persone: int = config.NUM_PERSONE_PER_TURNO,
    num_esperti: int = config.NUM_ESPERTI_MINIMI,
) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    """
    Seleziona le persone per un turno rispettando i vincoli:
    1. Almeno un esperto
    1. Massimo turnover (preferenza a chi non ha ancora fatto turni)
    3. Randomizzazione in caso di parità

    Args:
        df_disponibili: DataFrame con le persone disponibili
        persone_gia_assegnate: Dict {matricola: num_turni_assegnati}
        num_persone: numero di persone da selezionare

    Returns:
        (DataFrame selezionati, messaggio_errore)
        Se tutto ok: (DataFrame, None)
        Se errore: (None, messaggio_errore)
    """
    nuovi, esperti = separa_esperti(df_disponibili)

    # CHECK VINCOLI
    totale_disponibili = len(df_disponibili)
    if totale_disponibili < num_persone:
        return None, f"Solo {totale_disponibili} disponibili (servono {num_persone})"

    if len(esperti) < num_esperti:
        return None, "Non ci sono abbastanza esperti disponibili"

    # Calcola priorità per tutti
    def calcola_priorita(matricola: str) -> int:
        return -persone_gia_assegnate.get(matricola, 0)

    # Aggiungi priorità
    nuovi = nuovi.copy()
    esperti = esperti.copy()
    # per ogni matricola (sia per nuovi che esperti) aggiungere colonna priorità
    nuovi["_priorita"] = nuovi[config.MATRICOLA].apply(calcola_priorita)
    esperti["_priorita"] = esperti[config.MATRICOLA].apply(calcola_priorita)

    # Ordina per priorità (chi ha fatto meno turni viene prima)
    nuovi = nuovi.sort_values("_priorita", ascending=False)
    esperti = esperti.sort_values("_priorita", ascending=False)

    ### STEP 1: Seleziona 1 esperto (con randomizzazione se parità)
    max_priorita_esperti = esperti["_priorita"].max()
    esperti_top = esperti[esperti["_priorita"] == max_priorita_esperti]
    esperto_scelto = esperti_top.sample(n=num_esperti).iloc[0]

    selezionati = [esperto_scelto.to_dict()]
    # Rimuovi l'esperto selezionato (aggionramento della variabile)
    esperti = esperti[esperti[config.MATRICOLA] != esperto_scelto[config.MATRICOLA]]

    ### STEP 2: Seleziona le rimanenti persone
    rimanenti = pd.concat([esperti, nuovi]).drop(columns=["_priorita"])
    # ricalcolo delle priorità
    rimanenti["_priorita"] = rimanenti[config.MATRICOLA].apply(calcola_priorita)

    posti_rimanenti = num_persone - 1

    if len(rimanenti) < posti_rimanenti:
        return (
            None,
            "Non ci sono abbastanza persone disponibili dopo aver scelto l'esperto",
        )

    # Selezione con randomizzazione in caso di parità
    pool_selezionati = []  # variabile di persone già scelte (esperte o nuove)
    priorita_corrente = rimanenti["_priorita"].max()

    while len(pool_selezionati) < posti_rimanenti and len(rimanenti) > 0:
        candidati = rimanenti[rimanenti["_priorita"] == priorita_corrente]

        if len(candidati) + len(pool_selezionati) <= posti_rimanenti:
            # Tutti i candidati con questa priorità
            pool_selezionati.extend(
                candidati.to_dict("records")
            )  # allunga ola lista con i candidati
            rimanenti = rimanenti[rimanenti["_priorita"] < priorita_corrente]
        else:
            # Randomizzazione tra i candidati
            num_da_prendere = posti_rimanenti - len(pool_selezionati)
            scelti = candidati.sample(n=num_da_prendere)
            pool_selezionati.extend(scelti.to_dict("records"))
            break

        if len(rimanenti) > 0:
            priorita_corrente = rimanenti["_priorita"].max()

    # Combina esperto + altri selezionati
    selezionati.extend(pool_selezionati)

    # Converti in DataFrame e randomizza l'ordine finale
    df_selezionati = pd.DataFrame(selezionati)
    df_selezionati = df_selezionati.sample(frac=1).reset_index(drop=True)

    return df_selezionati, None


def converti_a_persona(row: pd.Series) -> Persona:
    """Converte una riga del DataFrame in un oggetto Persona"""
    return Persona(
        matricola=str(row[config.MATRICOLA]),
        nome=row[config.NOME],
        cognome=row[config.COGNOME],
        new_entry=(row[config.ESPERTO]),
    )


def assegna_turni(df: pd.DataFrame) -> List[Turno]:
    """
    Assegna le persone a tutti i turni

    Args:
        df: DataFrame completo con tutte le persone

    Returns:
        Lista di oggetti Turno con le persone assegnate
    """
    from data_loader import filtra_disponibili

    turni_assegnati = []

    conteggio_turni: Dict[str, int] = {}

    for giorno, fascia in config.TURNI:
        print(f"\n{'='*60}")
        print(f"TURNO: {giorno} {fascia}")
        print(f"{'='*60}")

        df_disponibili = filtra_disponibili(df, giorno, fascia)
        print(f"Persone disponibili: {len(df_disponibili)}")

        df_selezionati, errore = seleziona_turno(
            df_disponibili, conteggio_turni, config.NUM_PERSONE_PER_TURNO
        )

        if errore:
            print(f"ERRORE: {errore}")
            continue

        # Converti in oggetti Persona
        persone = [converti_a_persona(row) for _, row in df_selezionati.iterrows()]

        # Crea il turno
        turno = Turno(giorno=giorno, fascia=fascia, persone=persone)
        turni_assegnati.append(turno)

        # Aggiorna conteggio
        for persona in persone:
            conteggio_turni[persona.matricola] = (
                conteggio_turni.get(persona.matricola, 0) + 1
            )

        # Stampa risultati
        print(f"\nSelezionati ({len(persone)}):")

        for idx, persona in enumerate(persone, 1):  # conteggio parte da 1
            num_turni = conteggio_turni[persona.matricola]
            print(f"  {idx}. {persona}) - Turni totali: {num_turni}")

    return turni_assegnati
