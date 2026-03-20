"""
Modulo per calcolo e visualizzazione statistiche
"""

from typing import List, Dict
from collections import Counter
from models import Turno

import pandas as pd
import os
from config import EVENTO
import config


def stampa_riepilogo(turni: List[Turno]):
    """
    Args:
        turni: Lista di turni assegnati
    """
    print("\n" + "=" * 70)
    print("RIEPILOGO ASSEGNAZIONI")
    print("=" * 70)

    for turno in turni:
        print(f"\n{turno}:")
        esperti = turno.get_esperti()
        nuovi = turno.get_nuovi()

        print(f"  Esperti ({len(esperti)}):")
        for persona in esperti:
            print(f"    • {persona.nome} {persona.cognome} ({persona.matricola})")

        print(f"  Nuovi ({len(nuovi)}):")
        for persona in nuovi:
            print(f"    • {persona.nome} {persona.cognome} ({persona.matricola})")


def calcola_statistiche(turni: List[Turno]):
    """
    Args:
        turni: Lista di turni assegnati
    """
    # Conta turni per persona
    conteggio: Dict[str, int] = {}
    info_persone: Dict[str, tuple] = {}  # matricola -> (nome, cognome, is_esperto)

    for turno in turni:
        for persona in turno.persone:
            conteggio[persona.matricola] = conteggio.get(persona.matricola, 0) + 1
            if persona.matricola not in info_persone:
                info_persone[persona.matricola] = (
                    persona.nome,
                    persona.cognome,
                    persona.new_entry,
                )

    # Statistiche generali
    print("\n" + "=" * 70)
    print("STATISTICHE")
    print("=" * 70)

    distribuzione = Counter(conteggio.values())
    print(f"\nDistribuzione turni:")
    for num_turni in sorted(distribuzione.keys(), reverse=True):
        num_persone = distribuzione[num_turni]
        print(f"  {num_turni} turni: {num_persone} persone")

    # Dettaglio per persona
    print(f"\nDettaglio per persona:")
    persone_ordinate = sorted(
        conteggio.items(),
        key=lambda x: (
            -x[1],
            info_persone[x[0]][1],
        ),  # Ordina per turni (desc) poi cognome
    )

    for matricola, num_turni in persone_ordinate:
        nome, cognome, is_esperto = info_persone[matricola]
        tipo = "Esperto" if is_esperto else "Nuovo"
        print(f"  {cognome} {nome} (s{matricola}) [{tipo}]: {num_turni} turni")

    # Statistiche esperti
    print(f"\nStatistiche esperti per turno:")
    for turno in turni:
        esperti = turno.get_esperti()
        print(f"  {turno}: {len(esperti)} esperti")


def verifica_vincoli(turni: List[Turno]) -> bool:
    """
    Args:
        turni: Lista di turni assegnati
    """
    print("\n" + "=" * 70)
    print("VERIFICA VINCOLI")
    print("=" * 70)

    tutto_ok = True

    for turno in turni:
        esperti = turno.get_esperti()

        # Verifica numero esperti
        if len(esperti) < 1:
            print(f"{turno}: SOLO {len(esperti)} esperti (minimo 1)")
            tutto_ok = False
        else:
            print(f"{turno}: {len(esperti)} esperti OK")

    if tutto_ok:
        print("\nOK: Tutti i vincoli rispettati!")
    else:
        print("\nERRORE: Alcuni vincoli NON rispettati!")

    print("=" * 70)
    return tutto_ok


def salvataggio_output(turni: List[Turno]) -> pd.DataFrame:
    try:
        output_directory = os.path.join(os.getcwd(), "output") # nella cartella corrente crea cartella "output"
        os.makedirs(output_directory, exist_ok=True)
        # turno = List[Turno(giorno, fascia, persone)]
        df_turni = pd.DataFrame([
            {
                "Giorno": turno.giorno,
                "Fascia": turno.fascia,
                "Assegnati": ", ".join(turno.get_dati_assegnati())
            }
            for turno in turni
        ])
        df_turni.to_excel(os.path.join(output_directory, f"turni_{EVENTO}.xlsx"), index=False)
        print(f"\nFile Excel finale salvato in {output_directory}")

    except Exception as e:
        print(f'ERRORE nella creazione del file Excel: {e}')

    return df_turni


def conta_esclusi_con_disponibilita(df: pd.DataFrame, turni_assegnati: List[Turno]) -> dict:
    """
    Conta e mostra le persone che hanno dato disponibilità (almeno un 1)
    ma non hanno ricevuto NESSUN turno
    
    Args:
        df: DataFrame completo con tutte le persone
        turni_assegnati: Lista di turni assegnati
        
    Returns:
        Dict con statistiche e lista nomi
    """
    from data_loader import filtra_disponibili
    
    # Matricole che hanno almeno un turno
    matricole_assegnate = set()
    for turno in turni_assegnati:
        for persona in turno.persone:
            matricole_assegnate.add(persona.matricola)
    
    # Trova persone con disponibilità ma senza turni
    esclusi_con_disponibilita = []
    
    for _, row in df.iterrows():
        matricola = str(row[config.MATRICOLA])
        
        # Se ha già turni, skip
        if matricola in matricole_assegnate:
            continue
        
        # Verifica se ha almeno una disponibilità (almeno un 1)
        ha_disponibilita = False
        for giorno, fasce in config.MAP_COLONNE_DISPONIBILITA.items():
            for fascia, colonna_csv in fasce.items():
                if colonna_csv in df.columns and row[colonna_csv] == 1:
                    ha_disponibilita = True
                    break
            if ha_disponibilita:
                break
        
        # Se ha disponibilità ma 0 turni, aggiungilo alla lista
        if ha_disponibilita:
            nome_completo = f"{row[config.NOME]} {row[config.COGNOME]}"
            is_esperto = (row[config.ESPERTO] == 0)
            
            # Conta quante disponibilità ha dato
            num_disponibilita = 0
            for giorno, fasce in config.MAP_COLONNE_DISPONIBILITA.items():
                for fascia, colonna_csv in fasce.items():
                    if colonna_csv in df.columns and row[colonna_csv] == 1:
                        num_disponibilita += 1
            
            esclusi_con_disponibilita.append({
                'matricola': matricola,
                'nome': nome_completo,
                'esperto': is_esperto,
                'num_disponibilita': num_disponibilita
            })
    
    # Stampa risultati
    print(f"\n{'='*70}")
    print(f" PERSONE ESCLUSE CON DISPONIBILITÀ")
    print(f"{'='*70}")
    print(f"Persone con disponibilità ma 0 turni: {len(esclusi_con_disponibilita)}")
    
    if esclusi_con_disponibilita:
        # Ordina per numero di disponibilità (decrescente)
        esclusi_ordinati = sorted(esclusi_con_disponibilita, 
                                key=lambda x: x['num_disponibilita'], 
                                reverse=True)
        
        print(f"\nLista:")
        for persona in esclusi_ordinati:
            tipo = "Esperto" if persona['esperto'] else "Nuovo"
            print(f"  - {persona['nome']:30} ({persona['matricola']}) [{tipo:6}] - {persona['num_disponibilita']} disponibilità date")
        
        # Statistiche per tipo
        num_esperti = sum(1 for p in esclusi_con_disponibilita if p['esperto'])
        num_nuovi = len(esclusi_con_disponibilita) - num_esperti
        
        print(f"\nBreakdown:")
        print(f"  - Esperti esclusi: {num_esperti}")
        print(f"  - Nuovi esclusi: {num_nuovi}")
    else:
        print("\n Nessuna persona esclusa! Tutti con disponibilità hanno ricevuto turni.")
    
    return {
        'totale': len(esclusi_con_disponibilita),
        'esperti': sum(1 for p in esclusi_con_disponibilita if p['esperto']),
        'nuovi': sum(1 for p in esclusi_con_disponibilita if not p['esperto']),
        'dettagli': esclusi_con_disponibilita
    }