# Shift Assignment System - 2WheelsPoliTO

> 🇬🇧 English | 🇮🇹 [Versione italiana](README.md)

Automatic shift assignment system that respects availability and experience constraints.

*WARNING*: AVOID EXPOSING SENSITIVE DATA ON GITHUB -> place all files in the appropriate folders, or remember to update the `.gitignore` file. (see the **Privacy** section.)

## Features and constraints

- **Maximum turnover**: priority to people with fewer shifts
- **Expert constraint**: at least 1 expert per shift (i.e. someone who has been on the team for at least 1 year)
- **Randomization**: random selection in case of a tie
- **Detailed statistics**: analysis of the assignments

## For people who have never used GitHub

If you have never used Git or GitHub before, follow these steps to download and run the project on your computer.

### 1. Download the code

You don't need a GitHub account or Git to get started. The simplest way:

1. Go to the repository page on GitHub.
2. Click the green **"Code"** button in the top right.
3. Select **"Download ZIP"**.
4. Extract the downloaded ZIP folder to a convenient location (e.g. Desktop or Documents).

Alternatively, if you'd also like to easily "update" the project when it changes in the future, you can install [Git](https://git-scm.com/downloads) and run from a terminal:

```bash
git clone <repository-URL>
```

You can find the URL by clicking the same "Code" button (HTTPS option).

### 2. Install Python

The project requires **Python 3.14 or later**. You can download it from [python.org/downloads](https://www.python.org/downloads/). On Windows, make sure to check "Add Python to PATH" during installation.

### 3. Install `uv`

The project uses [`uv`](https://docs.astral.sh/uv/) to manage dependencies instead of plain `pip`. To install it, open a terminal and type:

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 4. Open a terminal in the project folder

- **Windows**: open the extracted folder in File Explorer, click the address bar, type `cmd` and press Enter.
- **macOS**: open the "Terminal" app, type `cd ` (with a trailing space), drag the project folder into the Terminal window, then press Enter.
- **Linux**: right-click the folder → "Open in Terminal" (varies by distribution).

### 5. What is `just`

The project uses [`just`](https://github.com/casey/just) as a "shortcut" to run the most common commands (`just setup`, `just make-turni`, etc.) without having to remember them. It's not required: every `just` command corresponds to a longer command that you can find in the `Justfile`. To install it:

```bash
# macOS (Homebrew)
brew install just

# Windows (with winget)
winget install --id Casey.Just

# Alternatively, without installing just, you can run directly:
uv sync
uv run main.py
```

## Usage

### 1. Prepare the CSV file

The CSV file must have this structure: (TO BE REVIEWED)

```csv
Matricola,Nome,Cognome,NEW 2026,1°turno,2°turno,...
123456,Mario,Rossi,0,1,1,0,1,1,0
```

**Required columns:**
- `Matricola`: unique student ID
- `Nome`, `Cognome`: first and last name
- `NEW 2026`: 0 = expert, 1 = new member
- Availability for each shift: 1 = available, 0 = not available

Save the file inside the `disponibili/` folder (this folder is NOT tracked by Git, so real data stays only on your computer).


### 2. Configure the file path

Edit `config.py` if needed:

```python
NAME_FILE = "file_name.csv"
```

### 3. Run the program
From a terminal, type the following command

```bash
just make-turni
```

If you haven't installed `just`, use this instead:

```bash
uv run main.py
```

## Output

The program will print:

1. **Assignments per shift**: who was selected
2. **Summary**: split between experts/new members per shift
3. **Statistics**: distribution of shifts per person
4. **Constraint check**: verifies the rules were respected

### Statistics
1. Detailed shift distribution
2. Number of shifts assigned per person
3. Verification of assignment constraints
4. Summary of any excluded people

## Configuration

All parameters that control the assignment logic are in `config.py`. This is the section to update **every time the event changes**, the number of shifts changes, or the CSV structure changes.

| Variable | What it does | When to change it |
|---|---|---|
| `NAME_FILE` | Name of the CSV file with availability data (inside `disponibili/`) | Every event, if the file name changes |
| `EVENTO` | Event name, used to name the output Excel file (`turni_<EVENTO>.xlsx`) | Every event |
| `NUM_PERSONE_PER_TURNO` | How many people to assign to each shift | If the number of required stations/volunteers changes |
| `NUM_ESPERTI_MINIMI` | Minimum number of experts required per shift | If the experience requirement changes |
| `TURNI` | List of `(day, time slot)` pairs defining which shifts exist | Every event, if days or time slots change |
| `MATRICOLA`, `NOME`, `COGNOME`, `ESPERTO` | Exact column names in the CSV that hold this data | Only if the source CSV has different headers |
| `MAP_COLONNE_DISPONIBILITA` | Maps each `(day, time slot)` pair defined in `TURNI` to the corresponding CSV column | Every event, if the days/slots or the availability column names in the CSV change |

**Warning**: the (day, time slot) keys in `TURNI` and in `MAP_COLONNE_DISPONIBILITA` must match **exactly** (same spelling, same accents), otherwise the program won't find the right column.

Example: if for a new event the shifts become only Monday morning and afternoon, you must update **both** `TURNI` **and** `MAP_COLONNE_DISPONIBILITA` with the new corresponding CSV columns.

## Privacy

Since the repository has been made public on GitHub, it's important to make sure sensitive data is not exposed externally.
For this reason, the `.gitignore` file is configured to **not track** CSV files containing real data:

```gitignore
disponibili/*.csv              # All CSVs
!disponibili/esempio_*.csv     # Except the examples
```

Before committing any changes, **verify that personal data is not being tracked** by checking whether it has been staged, with the command:

```bash
git status
```

As an extra safety net, the project also includes an automatic pre-commit hook that blocks the commit if it detects an untracked-by-design CSV file (see the **Automated testing** section).

## Dependencies

All required dependencies (including development ones, such as `pytest` and `pre-commit`) will be downloaded with the command

```bash
uv sync
```
which reads everything it needs from the `pyproject.toml` file, containing the list of required packages and their compatible versions.

## Development

### Main modules

- **config.py**: constants and configuration settings
- **models.py**: `Persona`, `Turno`, `AssegnazioneTurni` classes and their attributes
- **data_loader.py**: functions to load and filter CSV data
- **scheduler.py**: shift selection logic
- **statistics.py**: results analysis and display
- **main.py**: overall project coordination

### Selection algorithm

1. Filter people available for the shift
2. Separate experts and new members
3. Compute priority (based on the number of shifts already assigned — the more shifts, the lower the priority)
4. Select one expert (random in case of a tie)
5. Select the remaining people (experts + new members)
6. Randomize the final order

### Automated testing

The project uses [`pytest`](https://docs.pytest.org/) for automated testing, focused mainly on `scheduler.py` (the module with the most delicate logic).

To run the tests locally:

```bash
uv run pytest -v
```

**Pre-commit hook**: before every commit, it's automatically verified that no CSV file with real data (other than `esempio_*.csv`) is being added. It needs to be installed once per person, right after cloning the project:

```bash
uv run pre-commit install
```

**Automated CI**: on every `push` or pull request, GitHub automatically runs the tests via GitHub Actions (`.github/workflows/test.yaml`). You can check the outcome in the **"Actions"** tab of the repository on GitHub.

## Notes

- The data in the `esempio_disponibilita.csv` file is for illustration purposes only
- Your real file should be placed inside the `disponibili/` folder
- The real file will NOT be tracked by Git

## License

Project for internal use by Team 2WheelsPoliTO (see [LICENSE.txt](LICENSE.txt))