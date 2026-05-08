"""Fabbrica per la creazione e gestione del WebDriver Chrome."""

import logging
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from ..core.config import Config

logger = logging.getLogger("safework_pdl_manager.automation.driver")

class WebDriverFactory:
    """Gestisce la configurazione e l'istanza del WebDriver."""

    @staticmethod
    def create_driver(headless: bool = True) -> webdriver.Chrome:
        """Crea una nuova istanza di Chrome con configurazioni ottimizzate."""
        logger.info(f"Creazione WebDriver (headless={headless})")
        
        opt = Options()
        if headless:
            opt.add_argument("--headless=new")
            
        opt.add_argument("--window-size=1920,1080")
        opt.add_argument("--start-maximized")
        opt.add_argument("--disable-gpu")
        opt.add_argument("--no-sandbox")
        opt.add_argument("--log-level=3")
        opt.add_argument(f"--user-data-dir={Config.BROWSER_CACHE_DIR}")
        opt.add_argument("--profile-directory=Default")
        
        # Ottimizzazioni performance
        opt.page_load_strategy = 'eager'
        opt.add_argument("--disable-blink-features=AutomationControlled")

        opt.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        opt.add_experimental_option("useAutomationExtension", False)
        
        prefs = {
            "download.default_directory": str(Config.BASE_DIR / "Downloads"),
            "download.prompt_for_download": False,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "safebrowsing.enabled": False
        }
        opt.add_experimental_option("prefs", prefs)

        driver = webdriver.Chrome(options=opt)
        return driver
