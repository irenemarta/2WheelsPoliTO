"""
Modulo per calcolo e visualizzazione statistiche
"""
from typing import List, Dict
from collections import Counter
from models import Turno, AssegnazioneTurni


def stampa_riepilogo(turni: List[Turno]):
    """
    Stampa un riepilogo dei turni assegnati
    
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
        for p in esperti:
            print(f"    • {p.nome} {p.cognome} (s{p.matricola})")
        
        print(f"  Nuovi ({len(nuovi)}):")
        for p in nuovi:
            print(f"    • {p.nome} {p.cognome} (s{p.matricola})")


def calcola_statistiche(turni: List[Turno]):
    """
    Calcola e stampa statistiche dettagliate
    
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
                    persona.is_esperto
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
        key=lambda x: (-x[1], info_persone[x[0]][1])  # Ordina per turni (desc) poi cognome
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
    
    print("\n" + "=" * 70)


def verifica_vincoli(turni: List[Turno]) -> bool:
    """
    Verifica che tutti i vincoli siano rispettati
    
    Args:
        turni: Lista di turni assegnati
        
    Returns:
        True se tutti i vincoli sono OK, False altrimenti
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
