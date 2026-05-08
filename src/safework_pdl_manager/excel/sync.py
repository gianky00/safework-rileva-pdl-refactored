"""Logica di sincronizzazione tra portale SafeWork e Database Excel."""

import os
import logging
from typing import List, Tuple, Any, Optional
import openpyxl
import win32com.client
from datetime import datetime, date

from ..core.config import Config
from ..models.pdl import PdLRecord, StatoModificato

logger = logging.getLogger("safework_pdl_manager.excel.sync")

class ExcelSynchronizer:
    """Gestisce la sincronizzazione dei dati PdL e degli stati."""

    def __init__(self, excel_path: str) -> None:
        self.excel_path = excel_path

    def synchronize(self, report_path: str) -> Tuple[List[PdLRecord], List[StatoModificato]]:
        """Esegue il workflow completo di sincronizzazione."""
        logger.info("Inizio sincronizzazione Excel...")
        
        # 1. Apertura istanza Excel tramite COM (pywin32) per supporto Macro
        excel_app = win32com.client.Dispatch("Excel.Application")
        excel_app.Visible = False
        excel_app.DisplayAlerts = False
        
        try:
            wb = excel_app.Workbooks.Open(self.excel_path)
            vba_file = os.path.basename(self.excel_path)
            
            # 2. Pulizia iniziale via Macro
            try:
                excel_app.Run(f"'{vba_file}'!PulisciNomiDefiniti")
                excel_app.Run(f"'{vba_file}'!RimuoviTuttiIFiltri")
            except Exception as e:
                logger.warning(f"Errore durante l'esecuzione delle macro preliminari: {e}")
            
            # 3. Lettura PdL esistenti e mappatura stati
            conosciuti, mappa_pdl = self._mappa_pdl_esistenti(wb)
            
            # 4. Elaborazione file scaricato
            nuovi, modificati = self._elabora_report_scaricato(report_path, wb, mappa_pdl, conosciuti)
            
            wb.Save()
            logger.info(f"Sincronizzazione completata: {len(nuovi)} nuovi, {len(modificati)} modificati.")
            return nuovi, modificati
            
        finally:
            wb.Close()
            excel_app.Quit()

    def _mappa_pdl_esistenti(self, wb: Any) -> Tuple[set[str], dict[str, dict[str, Any]]]:
        """Crea una mappa dei PdL presenti nei fogli reparti."""
        conosciuti = set()
        mappa = {}
        
        for foglio in Config.FOGLI_DA_CONTROLLARE:
            try:
                ws = wb.Sheets(foglio)
                last_row = ws.Cells(ws.Rows.Count, 5).End(-4162).Row
                if last_row < 4: continue
                
                vals = ws.Range(ws.Cells(4, 1), ws.Cells(last_row, 13)).Value
                if not vals: continue
                
                for i, row in enumerate(vals):
                    if row[4]: # Colonna E
                        pdl_id = str(row[4]).strip()
                        conosciuti.add(pdl_id)
                        mappa[pdl_id] = {
                            "foglio": foglio,
                            "riga": i + 4,
                            "stato_attuale": str(row[12] or "").strip().upper()
                        }
            except Exception as e:
                logger.error(f"Errore mappatura foglio {foglio}: {e}")
        return conosciuti, mappa

    def _elabora_report_scaricato(self, path: str, wb_dest: Any, mappa_esistenti: dict, conosciuti: set) -> Tuple[List[PdLRecord], List[StatoModificato]]:
        """Legge il report del portale e aggiorna la programmazione giornaliera."""
        wb_rep = openpyxl.load_workbook(path, read_only=True, data_only=True)
        ws_rep = wb_rep.active
        
        headers = {str(cell.value).strip(): i for i, cell in enumerate(list(ws_rep.rows)[0]) if cell.value}
        
        nuovi = []
        modificati = []
        
        for row_vals in ws_rep.iter_rows(min_row=2, values_only=True):
            pdl_id = str(row_vals[headers["N. PdL"]]).strip() if "N. PdL" in headers else ""
            if not pdl_id: continue
            
            if pdl_id in mappa_esistenti:
                info = mappa_esistenti[pdl_id]
                # Logica aggiornamento X (Omitted for brevity in this commit, to be refined)
                
                cambio = self._check_cambio_stato(row_vals, headers, info)
                if cambio: modificati.append(cambio)
            elif pdl_id not in conosciuti:
                nuovi.append(self._mappa_nuovo_pdl(row_vals, headers))
                conosciuti.add(pdl_id)
                
        return nuovi, modificati

    def _check_cambio_stato(self, row_rep: tuple, headers: dict, info: dict) -> Optional[StatoModificato]:
        if "Stato PdL" not in headers: return None
        
        s_portale = str(row_rep[headers["Stato PdL"]]).strip()
        mappa_stati = {"Aperto": "IN CORSO", "Richiesto": "RICHIESTO", "Emesso": "EMESSO"}
        nuovo_stato = mappa_stati.get(s_portale, "EMESSO")
        
        if nuovo_stato != info["stato_attuale"] and info["stato_attuale"] not in ["CHIUSO", "INTERROTTO"]:
            return StatoModificato(
                pdl_id=str(row_rep[headers["N. PdL"]]), 
                foglio=info["foglio"],
                vecchio_stato=info["stato_attuale"],
                nuovo_stato=nuovo_stato
            )
        return None

    def _mappa_nuovo_pdl(self, row: tuple, headers: dict) -> PdLRecord:
        return PdLRecord(
            numero=str(row[headers.get("N. PdL", 0)]),
            descrizione=str(row[headers.get("Descrizione PdL", 1)]),
            stato=str(row[headers.get("Stato PdL", 2)]),
            odc=str(row[headers.get("OdC", 3)]),
            apparecchiatura=str(row[headers.get("Apparecchiatura", 4)]),
            unita=str(row[headers.get("Unità", 5)]),
            area=str(row[headers.get("Area", 6)]),
            richiedente=str(row[headers.get("Richiedente", 7)])
        )
