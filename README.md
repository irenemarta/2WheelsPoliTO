# Organizzatore Turni

Script Python per organizzare automaticamente i turni per gli eventi in base alla disponibilità.

## Requisiti

Prima di fare una run del codice, è necessario installare le dependencies del file requirements.txt.

- Python 3.6 o superiore
- Libreria pandas

Ciò può essere fatto eseguendo a terminale il comando 

```bash
uv sync
```
oppure 

```bash
uv add -r requirements.txt

```

## Configurazione

### 1. Preparazione del file CSV

Il file CSV deve contenere le seguenti colonne:

- `Nome`: Nome della persona
- `Cognome`: Cognome della persona
- `Matricola`: Numero di matricola (identificativo univoco)
- `Mail Poli`: Email politecnico
- `Mail drive`: Email drive
- `Reparto`: Reparto di appartenenza
- `NEW 2026`: Indica se la persona è nuova (1) o esperta (0)
- `Disponibilità` (da definire per generalizzazione)

**NB:** I campi vuoti nelle colonne di disponibilità vengono automaticamente considerati come 0 (non disponibile).

### 2. Parametri configurabili nello script

Aprendo il file `split_random.py` è possibile modificare i parametri nella sezione iniziale:

```python
# PARAMETRI CONFIGURABILI
PERSONE_PER_TURNO = 3  # Numero di persone da assegnare per ogni turno
FILE_CSV = "disponibilità.nome_file.csv"  # Preferibilmente in encoding utf-8
SEED_RANDOM = None  
```

#### Parametri:

- **PERSONE_PER_TURNO**: Quante persone assegnare per ogni turno
- **FILE_CSV**: Path al file CSV in input da leggere (da caricare nella cartella `disponibilità`)
- **SEED_RANDOM**: se si vuole utilizzare una suddivisione totalmente randomizzata e diversa a ogni esecuzione lasciare il seed impostato come `None`, altrimenti, per assicurare di ottenere risultati identici ma comunque randomizzati, cambiarlo a piacimento (ex: 36, 42,  etc.)

## Utilizzo

### Esecuzione

1. Posiziona il file CSV nella stessa cartella apposita (da sistemare, magari mettere anche if-try pd.read_excel())
2. Esegui lo script da terminale:

```bash
uv run python split_randomic.py
```

Lo script visualizzerà a schermo (da terminale) i risultati e mostrerà assegnazioni e statistiche. 

## Regole di assegnazione

Lo script rispetta automaticamente le seguenti regole:

1. **Almeno un esperto per turno**: Ogni turno ha sempre almeno una persona con esperienza (NEW 2026 = 0)

2. **Massimo turnover**: Priorità a chi ha fatto meno turni, per coinvolgere il maggior numero di persone possibile tra coloro che si sono resi disponibili.

3. **Assegnazione randomica**: Tra persone con la stessa priorità, la scelta è casuale

4. **Rispetto delle disponibilità**: Vengono assegnate solo persone che hanno dato la propria disponibilità (valore 1)

## Risoluzione problemi

### "File 'dipendenti.csv' non trovato"
- Verifica che il file CSV sia nella cartella giusta: `disponibilità`
- Oppure modifica il parametro `FILE_CSV` con il percorso completo

### "Nessun esperto disponibile"
- Almeno un esperto (NEW 2026 = 0) deve essere disponibile per ogni turno
- Verifica le disponibilità nel CSV

### "Solo X disponibili (servono Y)"
- Non ci sono abbastanza persone disponibili per quel turno -> ridurre `PERSONE_PER_TURNO`

## Personalizzazioni avanzate

### Modificare i nomi dei turni
DA RIVEDERE PER GENERALIZZARE

Se i tuoi turni hanno nomi diversi, modifica la lista `COLONNE_TURNI` nello script:

```python
COLONNE_TURNI = ["MeMatt", "MePom", "GioMatt", "GioPomm", "VeMatt", "VePom"]
```

### Esportare i risultati in un file ?????


ADELANTEEEEEEEEEEE