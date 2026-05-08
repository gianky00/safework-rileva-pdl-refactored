"""Configurazione centrale e gestione segreti per Safework PDL Manager."""

import os
from pathlib import Path
from typing import List

# Percorsi base
BASE_DIR = Path(__file__).parent.parent.parent
DEFAULT_DOWNLOAD_DIR = Path.home() / "Downloads"

class Config:
    """Gestisce tutte le impostazioni dell'applicazione."""
    
    # Parametri Sito
    URL = "https://safework.isab.com/"
    BROWSER_CACHE_DIR = BASE_DIR / "BrowserCache_Safework_Refactored"
    
    # Percorsi Excel (UNC supportati)
    EXCEL_FILE_PATH = os.getenv(
        "SAFEWORK_EXCEL_PATH", 
        r"\\192.168.11.251\Database_Tecnico_SMI\cartella strumentale condivisa\ALLEGRETTI\ATTIVITA_PROGRAMMATE.xlsm"
    )
    
    # Business Logic
    FOGLI_DA_CONTROLLARE = ["A1", "A2", "A3", "CTE", "BLENDING", "TAS", "IGCC"]
    RICHIEDENTI = [
        "Spicuglia Andrea", "Agusta Damiano", "Caldarella Ferdinando",
        "Messina Ivan", "Naselli Francesco", "Passanisi Domenico",
        "Barbagallo Giancarlo", "Prezzavento Manuel"
    ]
    
    # Timeout e Wait
    TIMEOUT_EXPORT = 90
    TIMEOUT_OVERLAY = 180
    SLEEP_DOWNLOAD = 3
    
    @staticmethod
    def get_credentials() -> tuple[str, str]:
        """
        Recupera le credenziali in modo sicuro.
        Priorità: Variabili d'ambiente > Keyring (se implementato) > Default (non raccomandato).
        """
        user = os.getenv("SAFEWORK_USER", "fcaldarella")
        pwd = os.getenv("SAFEWORK_PWD", "freddy69$")
        return user, pwd
