# Sistema Assegnazione Turni - 2WheelsPoliTO

> 🇮🇹 Italiano | 🇬🇧 [English version](README.en.md)

Sistema automatico per l'assegnazione dei turni rispettando vincoli di disponibilità ed esperienza.

*ATTENZIONE*: EVITARE DI ESPORRE DATI SENSIBILI SU GITHUB -> inserire tutti i file nelle apposite cartelle, oppure ricordarsi di aggiornare il file `.gitignore`. (vedi sezione **Privacy**.)

## Caratteristiche e vincoli rispettati

- **Massimo turnover**: priorità a chi ha fatto meno turni
- **Vincolo esperti**: almeno 1 esperto per turno (ossia, una persona nel team da almeno 1 anno)
- **Randomizzazione**: selezione casuale in caso di parità
- **Statistiche dettagliate**: analisi delle assegnazioni

## Per chi non ha mai usato GitHub

Se non hai mai usato Git o GitHub, segui questi passaggi per scaricare ed eseguire il progetto sul tuo computer.

### 1. Scarica il codice

Non serve creare un account GitHub né installare Git per iniziare. Il modo più semplice:

1. Vai sulla pagina del repository su GitHub.
2. Clicca sul pulsante verde **"Code"** in alto a destra.
3. Seleziona **"Download ZIP"**.
4. Estrai la cartella ZIP scaricata in una posizione comoda (es. Desktop o Documenti).

In alternativa, se in futuro vorrai anche "aggiornare" facilmente il progetto quando viene modificato, puoi installare [Git](https://git-scm.com/downloads) e usare da terminale:

```bash
git clone <URL-del-repository>
```

L'URL lo trovi cliccando sempre sul pulsante "Code" (opzione HTTPS).

### 2. Installa Python

Il progetto richiede **Python 3.14 o superiore**. Puoi scaricarlo da [python.org/downloads](https://www.python.org/downloads/). Durante l'installazione su Windows, spunta l'opzione "Add Python to PATH".

### 3. Installa `uv`

Il progetto usa [`uv`](https://docs.astral.sh/uv/) per gestire le dipendenze al posto del classico `pip`. Per installarlo, apri un terminale e digita:

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 4. Apri un terminale nella cartella del progetto

- **Windows**: apri la cartella estratta in Esplora File, clicca nella barra dell'indirizzo, scrivi `cmd` e premi Invio.
- **macOS**: apri l'app "Terminale", digita `cd ` (con lo spazio) e trascina la cartella del progetto dentro la finestra del Terminale, poi premi Invio.
- **Linux**: tasto destro nella cartella → "Apri nel terminale" (varia in base alla distribuzione).

### 5. Cos'è `just`

Il progetto usa [`just`](https://github.com/casey/just) come "scorciatoia" per lanciare i comandi più comuni (`just setup`, `just make-turni`, ecc.) senza doverli ricordare a memoria. Non è obbligatorio: ogni comando `just` corrisponde a un comando più lungo che trovi nel file `Justfile`. Per installarlo:

```bash
# macOS (Homebrew)
brew install just

# Windows (con winget)
winget install --id Casey.Just

# In alternativa, senza installare just, puoi eseguire direttamente:
uv sync
uv run main.py
```

## Utilizzo

### 1. Prepara il file CSV

Il file CSV deve avere questa struttura: (DA RIVEDERE)

```csv
Matricola,Nome,Cognome,NEW 2026,1°turno,2°turno,...
123456,Mario,Rossi,0,1,1,0,1,1,0
```

**Colonne richieste:**
- `Matricola`: identificativo univoco dello studente
- `Nome`, `Cognome`: dati anagrafici
- `NEW 2026`: 0 = esperto, 1 = nuovo
- Disponibilità per ogni turno: 1 = disponibile, 0 = non disponibile

Salva il file dentro la cartella `disponibili/` (questa cartella NON VIENE VERSIONATA su Git, quindi i dati reali restano solo sul tuo computer).


### 2. Configura il percorso

Modifica `config.py` se necessario:

```python
FILE_NAME = "nome_file.csv"
```

### 3. Esegui il programma
Da terminale, digitare il seguente comando

```bash
just make-turni
```

Se non hai installato `just`, usa invece:

```bash
uv run main.py
```

## Output

Il programma stamperà:

1. **Assegnazioni per turno**: chi è stato selezionato
2. **Riepilogo**: divisione esperti/nuovi per turno
3. **Statistiche**: distribuzione dei turni per persona
4. **Verifica vincoli**: controllo rispetto delle regole

### Statistiche
1. Distribuzione turni dettagliata
2. Numero di turni assgenati per persona
2. Verifica vincoli di assegnazione
3. Riepilogo eventuali esclusi

## Configurazione

Tutti i parametri che regolano la logica di assegnazione si trovano in `config.py`. Questa è la sezione da modificare **ogni volta che cambia l'evento**, il numero di turni o la struttura del CSV.

| Variabile | Cosa fa | Quando modificarla |
|---|---|---|
| `FILE_NAME` | Percorso del file CSV con le disponibilità | Ogni evento, se il nome del file cambia |
| `EVENTO` | Nome dell'evento, usato per nominare il file Excel di output (`turni_<EVENTO>.xlsx`) | Ogni evento |
| `NUM_PERSONE_PER_TURNO` | Quante persone assegnare a ciascun turno | Se cambia il numero di postazioni/volontari necessari |
| `NUM_ESPERTI_MINIMI` | Numero minimo di esperti richiesti per turno | Se cambia il vincolo di esperienza richiesto |
| `TURNI` | Lista di coppie `(giorno, fascia)` che definisce quali turni esistono | Ogni evento, se cambiano i giorni o gli orari |
| `MATRICOLA`, `NOME`, `COGNOME`, `ESPERTO` | Nomi esatti delle colonne nel CSV che contengono questi dati | Solo se il CSV di origine ha intestazioni diverse |
| `MAP_COLONNE_DISPONIBILITA` | Mappa ogni coppia `(giorno, fascia)` definita in `TURNI` alla colonna del CSV corrispondente | Ogni evento, se cambiano i giorni/le fasce o i nomi delle colonne di disponibilità nel CSV |

**Attenzione**: le chiavi (giorno, fascia) in `TURNI` e in `MAP_COLONNE_DISPONIBILITA` devono corrispondere **esattamente** (stessa scrittura, stessi accenti), altrimenti il programma non troverà la colonna giusta.

Esempio: se per un nuovo evento i turni diventano solo il Lunedì mattina e pomeriggio, bisogna aggiornare **sia** `TURNI` **sia** `MAP_COLONNE_DISPONIBILITA` con le nuove colonne del CSV corrispondenti.

## Privacy

Dal momento che la repository è stata resa pubblica su GitHub, è necessario assicurarsi che dati sensibili non vengano comunicati all'esterno.
A tal proposito, il file `.gitignore` è configurato per **non versionare** i CSV con dati reali:

```gitignore
disponibili/*.csv              # Tutti i CSV
!disponibili/esempio_*.csv     # Eccetto gli esempi
```

Prima di committare eventuali modifiche, **verifica che i dati personali non siano tracciati**, controllando se siano stati salvati in staging pre-commit con il comando:

```bash
git status
```

## Dipendenze

Tutte le dipendenze necessarie verranno scaricate dal comando

```bash
uv sync
```
che leggerà tutto il necessario dall'apposito file `pyproject.toml` contenente la lista dei moduli necessari e corrispettive versioni compatibili.

## Sviluppo

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

## Note

- I dati nel file `esempio_disponibilita.csv` sono a titolo di esempio
- Il tuo file reale va inserito nella cartella `disponibili/`
- Il file reale NON verrà versionato

## Licenza

Progetto per uso interno del Team 2WheelsPoliTO (vedi LICENSE.txt)