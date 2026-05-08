# ♾️ SAFEWORK PDL MANAGER - AI GUIDELINES

## 🚨 REGOLE FERREE
1. **LINGUA**: Rispondi sempre in ITALIANO.
2. **MODULARITÀ**: Non mescolare mai logica Excel con logica Selenium.
3. **QUALITÀ**: Superamento obbligatorio di `ruff` e `mypy` prima di ogni commit.
4. **POM**: Ogni nuovo elemento UI del portale deve essere aggiunto in `locators.py` e gestito in una classe `Page`.

## 🏗️ MAPPA MODULI
- `automation/`: Selenium Driver & Pages.
- `excel/`: Sincronizzazione stati.
- `core/`: Config & Secret.
- `models/`: Dati tipizzati.
