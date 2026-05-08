# CLAUDE.md

## Project Overview
**SafeWork PDL Manager** è la versione Enterprise per il rilevamento e la programmazione dei PdL ISAB.

## Development Commands
```bash
# Setup
poetry install

# Qualità
ruff check src
mypy src
interrogate src

# Esecuzione
python -m safework_pdl_manager.main
```

## Architecture
- **POM (Page Object Model)**: Logica Selenium isolata in `automation/pages/`.
- **Excel Synchronizer**: Gestione atomica del database Excel via `pywin32`.
- **Typed Models**: Utilizzo estensivo di `dataclasses` per la coerenza dei dati.
