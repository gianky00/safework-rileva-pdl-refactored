"""Modelli dati tipizzati per la gestione dei PdL."""

from dataclasses import dataclass
from typing import Optional, List

@dataclass
class PdLRecord:
    """Rappresenta un singolo record PdL estratto dal portale o da Excel."""
    
    numero: str
    descrizione: str
    stato: str
    odc: Optional[str] = None
    apparecchiatura: Optional[str] = None
    unita: Optional[str] = None
    area: Optional[str] = None
    richiedente: Optional[str] = None
    
    # Metadati Excel
    foglio_provenienza: Optional[str] = None
    riga_excel: Optional[int] = None

@dataclass
class StatoModificato:
    """Rappresenta un cambiamento di stato rilevato durante la sincronizzazione."""
    
    pdl_id: str
    foglio: str
    vecchio_stato: str
    nuovo_stato: str
    unita: str = ""
    apparecchiatura: str = ""
    descrizione: str = ""
    richiedente: str = ""
