"""Orchestratore principale per il rilevamento PdL e la sincronizzazione programmazione."""

import sys
import logging
from datetime import datetime, timedelta
from rich.console import Console
from rich.logging import RichHandler

from .core.config import Config
from .automation.driver import WebDriverFactory
from .automation.pages.login_page import LoginPage
from .automation.pages.export_page import ExportPage
from .excel.sync import ExcelSynchronizer

# Configurazione Logging avanzato con Rich
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger("safework_pdl_manager")
console = Console()

class PDLManagerOrchestrator:
    """Coordina il workflow end-to-end dell'applicazione."""

    def __init__(self, headless: bool = True) -> None:
        self.headless = headless
        self.driver = None
        self.sync = ExcelSynchronizer(Config.EXCEL_FILE_PATH)

    def run(self) -> None:
        """Esegue il processo di aggiornamento."""
        console.print("[bold blue]🚀 SafeWork PDL Manager v2.0[/bold blue]")
        start_time = datetime.now()
        
        try:
            # 1. Automazione Portale
            self.driver = WebDriverFactory.create_driver(headless=self.headless)
            
            # Login
            login_pg = LoginPage(self.driver)
            login_pg.navigate()
            
            if not login_pg.is_logged_in():
                user, pwd = Config.get_credentials()
                login_pg.login(user, pwd)
            
            # Esportazione
            export_pg = ExportPage(self.driver)
            export_pg.navigate_to_activities()
            
            # Definiamo il range (es. ultimi 7 giorni + prossimi 15)
            dal = datetime.now() - timedelta(days=7)
            al = datetime.now() + timedelta(days=15)
            
            report_path = export_pg.esporta_programmazione(dal, al)
            console.print(f"[green]✅ Report scaricato:[/green] {report_path}")
            
            # 2. Sincronizzazione Excel
            nuovi, modificati = self.sync.synchronize(report_path)
            
            # 3. Riepilogo Finale
            self._mostra_riepilogo(nuovi, modificati)
            
        except Exception as e:
            logger.error(f"Errore fatale durante l'esecuzione: {e}")
            sys.exit(1)
        finally:
            if self.driver:
                self.driver.quit()
            duration = datetime.now() - start_time
            console.print(f"\n[bold]Esecuzione completata in {duration.seconds}s.[/bold]")

    def _mostra_riepilogo(self, nuovi, modificati) -> None:
        """Visualizza un report sintetico dell'attività svolta."""
        console.print("\n[bold cyan]📊 Riepilogo Attività:[/bold cyan]")
        console.print(f" - Nuovi PdL rilevati: {len(nuovi)}")
        console.print(f" - Stati aggiornati: {len(modificati)}")
        
        if nuovi:
            console.print("\n[bold yellow]🆕 Elenco Nuovi PdL:[/bold yellow]")
            for n in nuovi[:10]: # Mostra i primi 10
                console.print(f"   • {n.numero}: {n.descrizione[:50]}...")

def main() -> None:
    """Entry point per la CLI."""
    orchestrator = PDLManagerOrchestrator(headless=True)
    orchestrator.run()

if __name__ == "__main__":
    main()
