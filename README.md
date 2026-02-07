# Sistema Assegnazione Turni - A&T 2WheelsPoliTO

Sistema automatico per l'assegnazione dei turni rispettando vincoli di disponibilità ed esperienza.

## 📋 Caratteristiche

- **Massimo turnover**: priorità a chi ha fatto meno turni
- **Vincolo esperti**: almeno 1 esperto per turno
- **Randomizzazione**: selezione casuale in caso di parità
- **Statistiche dettagliate**: analisi delle assegnazioni

## 🏗️ Struttura del progetto

```
project/
├── .gitignore                      # File da escludere da git
├── README.md                       # Questo file, con spiegazione della struttura del codice
├── config.py                       # Configurazioni standard
├── models.py                       # Classi e strutture dati utilizzate
├── data_loader.py                  # Caricamento dati da input (CSV)
├── scheduler.py                    # Logica di assegnazione
├── statistics.py                   # Calcolo statistiche dei turni
├── main.py                         # Entry point
└── disponibilità/
    ├── esempio_disponibilita.csv   # File esempio (versionato)
    └── A&T_Disp_2WheelsPoliTO.csv  # File reale (NON versionato)
```

## 🚀 Utilizzo

### 1. Prepara il file CSV

Il file CSV deve avere questa struttura: (DA RIVEDERE)

```csv
Matricola,Nome,Cognome,NEW 2026,Mercoledì Mattina,Mercoledì Pomeriggio,...
123456,Mario,Rossi,0,1,1,0,1,1,0
```

**Colonne richieste:**
- `Matricola`: identificativo univoco dello studente
- `Nome`, `Cognome`: dati anagrafici
- `NEW 2026`: 0 = esperto, 1 = nuovo
- Disponibilità per ogni turno: 1 = disponibile, 0 = non disponibile

### 2. Configura il percorso

Modifica `config.py` se necessario:

```python
INPUT_CSV = "disponibilità/nome_file.csv"
```

### 3. Esegui il programma

```bash
python main.py
```

## 📊 Output

Il programma stamperà:

1. **Assegnazioni per turno**: chi è stato selezionato
2. **Riepilogo**: divisione esperti/nuovi per turno
3. **Statistiche**: distribuzione dei turni per persona
4. **Verifica vincoli**: controllo rispetto delle regole

## 🔧 Configurazione

Per adattare le logiche di assegnazione, modifica i parametri nel modulo `config.py`:

```python
NUM_PERSONE_PER_TURNO = 4      # Persone per turno
NUM_ESPERTI_MINIMI = 1          # Esperti minimi per turno
```

## 🔒 Privacy

Dal momento che la repository è stata resa pubblica su GitHub, è necessario assicurarsi che dati sensibili non vengano comunicati all'esterno.
A tal proposito, il file `.gitignore` è configurato per **non versionare** i CSV con dati reali:

```gitignore
disponibilità/*.csv              # Tutti i CSV
!disponibilità/esempio_*.csv     # Eccetto gli esempi
```

Prima di committare, **verifica che i dati personali non siano tracciati**, controllando se siano stati salvati in staging pre-commit con il comando:

```bash
git status
```

## 📦 Dipendenze

Tutte le dipendenze necessarie verranno scaricate dal comando

```bash
uv sync
```
che leggerà tutto il necessario dall'apposito file `pyproject.toml`.

## 🛠️ Sviluppo

### Moduli principali

- **config.py**: costanti e configurazioni utili
- **models.py**: classi `Persona`, `Turno`, `AssegnazioneTurni` e relativi attributi
- **data_loader.py**: funzioni per caricare e filtrare i dati CSV
- **scheduler.py**: logica di selezione turni
- **statistics.py**: analisi e visualizzazione risultati
- **main.py**: coordinamento generale del progetto

### Algoritmo di selezione

1. Filtra persone disponibili per il turno
2. Separa esperti e nuovi
3. Calcola priorità (basata su numero turni già assegnati - più è alto il numero di turni, minore sarà la priorità)
4. Seleziona un esperto (random se parità)
5. Seleziona rimanenti (esperti + nuovi)
6. Randomizza ordine finale

## 📝 Note

- I dati nel file `esempio_disponibilita.csv` sono a titolo di esempio
- Il tuo file reale va inserito nella cartella `disponibilità/`
- Il file reale NON verrà versionato

## 📄 Licenza

Progetto per uso interno del Team 2WheelsPoliTO