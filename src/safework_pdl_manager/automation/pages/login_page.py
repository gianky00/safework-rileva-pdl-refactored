"""Astrazione della pagina di Login del portale SafeWork."""

import time
import logging
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..automation.locators import LoginLocators, CommonLocators
from ..core.config import Config

logger = logging.getLogger("safework_pdl_manager.pages.login")

class LoginPage:
    """Gestisce l'autenticazione sul portale."""

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, 40)

    def navigate(self) -> None:
        """Naviga all'URL del portale."""
        logger.info(f"Navigazione a {Config.URL}")
        self.driver.get(Config.URL)
        self.attendi_scomparsa_overlay()

    def attendi_scomparsa_overlay(self, timeout: int = 120) -> None:
        """Attende la scomparsa dell'overlay di caricamento."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(CommonLocators.OVERLAY_WAIT)
            )
        except Exception:
            logger.warning("Timeout overlay di caricamento.")

    def is_logged_in(self) -> bool:
        """Verifica se la sessione è già attiva."""
        try:
            # Se troviamo il link alle attività, siamo loggati
            self.driver.find_element(*CommonLocators.NAV_VISUALIZZA_ATTIVITA)
            return True
        except Exception:
            return False

    def login(self, user: str, password: str) -> None:
        """Esegue la procedura completa di login."""
        logger.info(f"Esecuzione login per utente: {user}")
        
        # Selezione Sito
        self.wait.until(EC.element_to_be_clickable(LoginLocators.SITO_DROPDOWN)).click()
        self.wait.until(EC.element_to_be_clickable(LoginLocators.ISAB_SUD_OPTION)).click()
        
        # Inserimento Credenziali
        u_field = self.wait.until(EC.visibility_of_element_located(LoginLocators.USERNAME_FIELD))
        u_field.clear()
        u_field.send_keys(user)
        
        p_field = self.wait.until(EC.visibility_of_element_located(LoginLocators.PASSWORD_FIELD))
        p_field.clear()
        p_field.send_keys(password)
        
        self.driver.find_element(*LoginLocators.LOGIN_BUTTON).click()
        self.attendi_scomparsa_overlay()
        
        # Navigazione post-login
        self.wait.until(EC.element_to_be_clickable(CommonLocators.HOME_BUTTON)).click()
        self.attendi_scomparsa_overlay()
        
        logger.info("Login completato.")
