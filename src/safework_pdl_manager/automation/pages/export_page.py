"""Gestione dell'esportazione della programmazione PdL mensile."""

import os
import time
import logging
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..automation.locators import ExportLocators, CommonLocators
from ..core.config import Config

logger = logging.getLogger("safework_pdl_manager.pages.export")

class ExportPage:
    """Gestisce la ricerca e l'esportazione dei PdL."""

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.TIMEOUT_EXPORT)

    def navigate_to_activities(self) -> None:
        """Naviga alla pagina di visualizzazione attività."""
        self.wait.until(EC.element_to_be_clickable(CommonLocators.NAV_VISUALIZZA_ATTIVITA)).click()
        self.attendi_scomparsa_overlay()

    def attendi_scomparsa_overlay(self) -> None:
        """Attende overlay con timeout configurato."""
        try:
            WebDriverWait(self.driver, Config.TIMEOUT_OVERLAY).until(
                EC.invisibility_of_element_located(CommonLocators.OVERLAY_WAIT)
            )
        except Exception:
            logger.warning("Timeout overlay in ExportPage.")

    def esporta_programmazione(self, dal: datetime, al: datetime) -> str:
        """
        Esegue i filtri e scarica l'Excel.
        Returns: percorso del file scaricato.
        """
        logger.info(f"Esportazione programmazione dal {dal.date()} al {al.date()}")
        
        # Filtro Ditta (CO.EMI)
        self.wait.until(EC.element_to_be_clickable(ExportLocators.DITTA_DROPDOWN)).click()
        self.wait.until(EC.element_to_be_clickable(ExportLocators.COEMI_OPTION)).click()
        
        # Selezione Richiedenti (Multi-select)
        self._seleziona_richiedenti(Config.RICHIEDENTI)
        
        # Inserimento Date
        self._set_date(ExportLocators.DATE_DAL, dal.strftime('%d/%m/%Y'))
        self._set_date(ExportLocators.DATE_AL, al.strftime('%d/%m/%Y'))
        
        # Avvio Ricerca
        self.driver.find_element(*ExportLocators.SEARCH_BUTTON).click()
        self.attendi_scomparsa_overlay()
        
        # Click Esporta
        btn = self.wait.until(EC.presence_of_element_located(ExportLocators.EXPORT_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
        
        return self._wait_for_download("Programmazione.xlsx")

    def _seleziona_richiedenti(self, nomi: list[str]) -> None:
        """Helper per la complessa selezione multipla del portale."""
        self.wait.until(EC.element_to_be_clickable(ExportLocators.RICHIEDENTE_DROPDOWN)).click()
        container = self.wait.until(EC.visibility_of_element_located(ExportLocators.RICHIEDENTE_CONTAINER))
        search = container.find_element(*ExportLocators.RICHIEDENTE_SEARCH)
        
        for nome in nomi:
            search.clear()
            search.send_keys(nome)
            time.sleep(0.5)
            try:
                # Click sulla checkbox relativa al nome trovato
                xpath = f".//label//span[normalize-space()='{nome}']"
                item = container.find_element(By.XPATH, xpath)
                self.driver.execute_script("arguments[0].click();", item)
            except Exception:
                logger.warning(f"Richiedente '{nome}' non trovato nel menu.")
        
        # Chiudi dropdown
        self.driver.find_element(*ExportLocators.RICHIEDENTE_DROPDOWN).click()

    def _set_date(self, locator: tuple[str, str], date_str: str) -> None:
        """Pulisce e imposta una data nel campo specifico."""
        el = self.driver.find_element(*locator)
        el.click()
        el.send_keys(Keys.CONTROL + "a")
        el.send_keys(Keys.BACK_SPACE)
        el.send_keys(date_str)

    def _wait_for_download(self, filename: str) -> str:
        """Attende il completamento del download e rinomina il file."""
        download_dir = Config.BASE_DIR / "Downloads"
        target_path = download_dir / filename
        dest_path = download_dir / f"Nuovi_PdL_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        if not download_dir.exists():
            download_dir.mkdir(parents=True)
            
        for _ in range(Config.TIMEOUT_EXPORT):
            if target_path.exists():
                time.sleep(Config.SLEEP_DOWNLOAD)
                os.rename(target_path, dest_path)
                return str(dest_path)
            time.sleep(1)
        raise TimeoutError("Download non completato.")
