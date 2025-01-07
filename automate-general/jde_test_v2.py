from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

# Configuración del driver
def setup_driver(path, url):
    service = Service(executable_path=path)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    driver.get(url)
    return driver

# Inicio de sesión
def login(driver, username, password):
    driver.find_element(By.ID, "User").send_keys(username)
    driver.find_element(By.ID, "Password").send_keys(password)
    driver.find_element(By.XPATH, "//input[@value='Conexión']").click()
    time.sleep(5)

# Navegar a la vista de carga de archivos
def navigate_to_view(driver):
    iframe = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "e1menuAppIframe"))
    )
    driver.switch_to.frame(iframe)
    # ... (Resto del código de navegación)

# Proceso principal
def main():
    path = r"C:\path\to\chromedriver.exe"
    url = "https://example.com"
    driver = setup_driver(path, url)
    try:
        login(driver, "EMONTANC", "edmcESSA02**")
        navigate_to_view(driver)
        # Otros pasos...
    finally:
        input("Presiona Enter para cerrar la ventana...")
        driver.quit()

if __name__ == "__main__":
    main()
