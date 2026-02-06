"""
Sistema di assegnazione turni A&T 2WheelsPoliTO

Entry point principale del programma
"""
import pandas as pd
import config
from data_loader import get_data_persone
from scheduler import assegna_turni
from statistics import stampa_riepilogo, calcola_statistiche, verifica_vincoli


def main():
    """Funzione principale"""
    print("=" * 70)
    print("SISTEMA ASSEGNAZIONE TURNI - 2WheelsPoliTO")
    print("=" * 70)
    
    # Carica dati
    print(f"\nCaricamento dati da: {config.INPUT_CSV}")
    try:
        df = pd.read_csv(config.INPUT_CSV)
        print(f"Caricate {len(df)} persone")
    except FileNotFoundError:
        print(f"ERRORE: File {config.INPUT_CSV} non trovato!")
        return
    except Exception as e:
        print(f"ERRORE durante il caricamento: {e}")
        return
    
    # Assegna turni
    print(f"\nInizio assegnazione")
    print(f"\nConfigurazione:")
    print(f"\t- Persone per turno: {config.NUM_PERSONE_PER_TURNO}")
    print(f"\t- Esperti minimi: {config.NUM_ESPERTI_MINIMI}")
    print(f"\t- Numero turni: {len(config.TURNI)}")
    
    turni = assegna_turni(df)
    
    # Stampa risultati
    stampa_riepilogo(turni)
    
    # Calcola statistiche
    calcola_statistiche(turni)
    
    # Verifica vincoli
    verifica_vincoli(turni)
    
    print("\nProcesso completato!")


if __name__ == "__main__":
    main()
