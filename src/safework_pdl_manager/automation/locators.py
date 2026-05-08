"""Centralizzazione di tutti i selettori Selenium per il portale SafeWork."""

from selenium.webdriver.common.by import By

class LoginLocators:
    """Selettori per la pagina di login."""
    SITO_DROPDOWN = (By.XPATH, "//button[@class='ms-choice']")
    ISAB_SUD_OPTION = (By.XPATH, "//div[contains(@class, 'ms-drop')]//span[normalize-space()='ISAB Sud']")
    USERNAME_FIELD = (By.ID, "inpUtente")
    PASSWORD_FIELD = (By.ID, "inpPassword")
    LOGIN_BUTTON = (By.ID, "btnLogin")

class CommonLocators:
    """Selettori comuni a più pagine."""
    OVERLAY_WAIT = (By.ID, "GISWaitOverlay")
    LOADING_INDICATOR = (By.ID, "gis-loading") # Placeholder aggiornato
    HOME_BUTTON = (By.ID, "topIcon-actHomePage")
    NAV_VISUALIZZA_ATTIVITA = (By.ID, "sideBar-actVisualizzaAttivita")

class ExportLocators:
    """Selettori per la pagina di esportazione programmazione."""
    DITTA_DROPDOWN = (By.XPATH, "//select[@id='fldIdDitta']/following-sibling::div/button")
    COEMI_OPTION = (By.XPATH, "//span[normalize-space()='CO.EMI SRL']")
    RICHIEDENTE_DROPDOWN = (By.XPATH, "//select[@id='fldIdRichiedente']/following-sibling::div/button")
    RICHIEDENTE_SEARCH = (By.XPATH, "//div[contains(@class,'ms-drop') and contains(@style,'display: block')]//input[@type='text']")
    RICHIEDENTE_CONTAINER = (By.XPATH, "//div[contains(@class,'ms-drop') and contains(@style,'display: block')]")
    
    DATE_DAL = (By.ID, "programmazioneDal")
    DATE_AL = (By.ID, "programmazioneAl")
    SEARCH_BUTTON = (By.ID, "btnAvviaRicerca")
    EXPORT_BUTTON = (By.ID, "btnEsporta")
