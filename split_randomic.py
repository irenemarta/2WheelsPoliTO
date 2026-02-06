
import pandas as pd
import random
from collections import defaultdict

# PARAMETRI CONFIGURABILI
PERSONE_PER_TURNO = 4
FILE_CSV = "disponibilità/A&T_Disp_2WheelsPoliTO.csv" 
SEED_RANDOM = None # reproducibility seed

# Nomi delle colonne dei turni (nomi csv)
COLONNE_TURNI = ["MeMatt", "MePom", "GioMatt", "GioPomm", "VeMatt", "VePom"]

# Mapping da nomi csv a nomi lunghi (per display)
MAP_COLONNE_TURNI = {
    "MeMatt": "Mercoledì 9:30 - 13",
    "MePom": "Mercoledì 13 - 17",
    "GioMatt": "Giovedì 9:30 - 13",
    "GioPomm": "Giovedì 13 - 17",
    "VeMatt": "Venerdì 9:30 - 13",
    "VePom": "Venerdì 13 - 16:30"
}

def carica_dati(file_path):
    try:
        df = pd.read_csv(file_path, sep=';', encoding='utf-8')
        print(f"File caricato: {len(df)} persone trovate\n")
        # Converti le colonne di turni a integer
        for col in COLONNE_TURNI:
            if col in df.columns:
                # Sostituisci NaN, stringhe vuote e valori nulli con 0
                df[col] = df[col].fillna(0)
                # Converti a int per sicurezza
                df[col] = df[col].astype(int)
        return df
    except FileNotFoundError:
        print(f"Errore: File '{file_path}' non trovato")
        return None
    except Exception as e:
        print(f"Errore nel caricamento: {e}")
        return None

def trova_disponibili(df, colonna_turno):
    return df[df[colonna_turno] == 1].copy()

def separa_esperti(df_disponibili):
    nuovi = df_disponibili[df_disponibili['NEW 2026'].astype(str) == 'SI'].copy()
    esperti = df_disponibili[df_disponibili['NEW 2026'].astype(str) == 'NO'].copy()
    return nuovi, esperti

def seleziona_turno(df_disponibili, persone_gia_assegnate, num_persone):
    """
    Seleziona le persone per un turno rispettando i vincoli:
    - Almeno un esperto
    - Massimo turnover (preferenza a chi non ha ancora fatto turni)
    """
    nuovi, esperti = separa_esperti(df_disponibili)
    
    # Verifica se ci sono abbastanza persone
    totale_disponibili = len(df_disponibili)
    if totale_disponibili < num_persone:
        return None, f"Solo {totale_disponibili} disponibili (servono {num_persone})"
    
    # Verifica se c'è almeno un esperto
    if len(esperti) == 0:
        return None, "Nessun esperto disponibile"
    
    # Calcola priorità in base a quanti turni ha già fatto ciascuno
    def calcola_priorita(persona_matricola):
        return -persone_gia_assegnate[persona_matricola]  # Negativo per ordinare crescente
    
    # Ordina per priorità (chi ha fatto meno turni prima)
    nuovi_sorted = nuovi.copy()
    esperti_sorted = esperti.copy()
    
    nuovi_sorted['_priorita'] = nuovi_sorted['Matricola'].apply(calcola_priorita)
    esperti_sorted['_priorita'] = esperti_sorted['Matricola'].apply(calcola_priorita)
    
    nuovi_sorted = nuovi_sorted.sort_values('_priorita', ascending=False)
    esperti_sorted = esperti_sorted.sort_values('_priorita', ascending=False)
    
    # Selezionati almeno 1 esperto
    esperti_selezionati = []
    
    # Prendi 1 esperto con priorità (chi ha fatto meno turni)
    # Se ci sono esperti con stessa priorità, randomizza tra loro
    max_priorita_esperti = esperti_sorted['_priorita'].max()
    esperti_top = esperti_sorted[esperti_sorted['_priorita'] == max_priorita_esperti]
    esperto_scelto = esperti_top.sample(n=1).iloc[0]
    esperti_selezionati.append(esperto_scelto.to_dict())
    
    # Rimuovi l'esperto selezionato dalle liste
    esperti_sorted = esperti_sorted[esperti_sorted['Matricola'] != esperto_scelto['Matricola']]
    
    # Combina i rimanenti (esperti + nuovi) e seleziona il resto
    rimanenti = pd.concat([esperti_sorted, nuovi_sorted])
    rimanenti = rimanenti.drop(columns=['_priorita'])
    
    num_rimanenti = num_persone - 1
    
    if len(rimanenti) < num_rimanenti:
        return None, f"Non abbastanza persone disponibili dopo aver scelto l'esperto"
    
    # Tra i rimanenti, prendi quelli con priorità massima e randomizza
    rimanenti['_priorita'] = rimanenti['Matricola'].apply(calcola_priorita)
    max_priorita_rim = rimanenti['_priorita'].max()
    
    # Costruisci il pool per i rimanenti slot
    pool_finale = []
    priorita_corrente = max_priorita_rim
    
    while len(pool_finale) < num_rimanenti and len(rimanenti) > 0:
        candidati = rimanenti[rimanenti['_priorita'] == priorita_corrente]
        
        if len(candidati) + len(pool_finale) <= num_rimanenti:
            # Possiamo prendere tutti
            pool_finale.extend(candidati.to_dict('records'))
            rimanenti = rimanenti[rimanenti['_priorita'] < priorita_corrente]
        else:
            # Dobbiamo scegliere random tra i candidati
            num_da_prendere = num_rimanenti - len(pool_finale)
            scelti = candidati.sample(n=num_da_prendere)
            pool_finale.extend(scelti.to_dict('records'))
            break
        
        if len(rimanenti) > 0:
            priorita_corrente = rimanenti['_priorita'].max()
    
    # Converti pool_finale in DataFrame
    if pool_finale:
        df_pool = pd.DataFrame(pool_finale)
        esperti_selezionati.extend(df_pool.to_dict('records'))
    
    # Converti selezionati in DataFrame
    if esperti_selezionati:
        df_selezionati = pd.DataFrame(esperti_selezionati)
        # Randomizza l'ordine finale
        df_selezionati = df_selezionati.sample(frac=1).reset_index(drop=True)
        return df_selezionati, None
    else:
        return pd.DataFrame(), None

def organizza_turni(df, num_persone=PERSONE_PER_TURNO):
    """Organizza tutti i turni"""
    risultati = {}
    persone_gia_assegnate = defaultdict(int)
    
    print(f"{'='*70}")
    print(f"ORGANIZZAZIONE TURNI ({num_persone} persone per turno)")
    print(f"{'='*70}\n")
    
    for idx, turno in MAP_COLONNE_TURNI.items():
        disponibili = trova_disponibili(df, idx)
        
        print(f"\n--- {turno} ---")
        print(f"Disponibili: {len(disponibili)} persone")
        
        if len(disponibili) == 0:
            print("ERRORE: Nessun disponibile per questo turno!")
            risultati[turno] = None
            continue
        
        selezionati, errore = seleziona_turno(disponibili, persone_gia_assegnate, num_persone)
        
        if errore:
            print(f"{errore}")
            risultati[turno] = None
        else:
            # Aggiorna il conteggio
            for _, persona in selezionati.iterrows():
                persone_gia_assegnate[persona['Matricola']] += 1
            
            risultati[turno] = selezionati
            print(f"✓ Turno assegnato:")
            for idx, persona in selezionati.iterrows():
                ruolo = "NUOVO" if persona['NEW 2026'] == 1 else "ESPERTO"
                turni_fatti = persone_gia_assegnate[persona['Matricola']]
                print(f"{persona['Nome']} {persona['Cognome']} ({ruolo}) - Turni totali: {turni_fatti}")
    
    return risultati, persone_gia_assegnate

def stampa_statistiche(persone_gia_assegnate, df):
    print(f"\n{'='*70}")
    print("ASSEGNAZIONI")
    print(f"{'='*70}\n")
    
    totale_persone = len(df)
    persone_coinvolte = len([k for k, v in persone_gia_assegnate.items() if v > 0])
    
    print(f"Persone totali nel database: {totale_persone}")
    print(f"Persone coinvolte nei turni: {persone_coinvolte}")
    print(f"Percentuale di coinvolgimento: {persone_coinvolte/totale_persone*100:.1f}%\n")
    
    print("Distribuzione turni per persona:")
    for num_turni in sorted(set(persone_gia_assegnate.values()), reverse=True):
        persone_con_n_turni = len([k for k, v in persone_gia_assegnate.items() if v == num_turni])
        print(f"  {num_turni} turno/i: {persone_con_n_turni} persone")
    
    # Persone non coinvolte
    matricole_assegnate = set(persone_gia_assegnate.keys())
    tutte_matricole = set(df['Matricola'].values)
    non_coinvolte = tutte_matricole - matricole_assegnate
    
    if non_coinvolte:
        print(f"\nPersone non coinvolte ({len(non_coinvolte)}):")
        for matricola in non_coinvolte:
            persona = df[df['Matricola'] == matricola].iloc[0]
            # Conta per quanti turni era disponibile
            disponibilita = sum([persona[col] for col in COLONNE_TURNI])
            print(f"  • {persona['Nome']} {persona['Cognome']} (disponibile per {disponibilita} turni)")

def main():
    # Imposta seed se specificato
    if SEED_RANDOM is not None:
        random.seed(SEED_RANDOM)
        print(f"Seed random impostato a: {SEED_RANDOM}\n")
    
    # Carica i dati
    df = carica_dati(FILE_CSV)
    if df is None:
        return
    
    # Organizza i turni
    risultati, assegnazioni = organizza_turni(df, PERSONE_PER_TURNO)
    
    # Stampa statistiche
    stampa_statistiche(assegnazioni, df)
    print(risultati)
    
    print(f"\n{'='*70}")
    print("✓ Organizzazione completata!")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
