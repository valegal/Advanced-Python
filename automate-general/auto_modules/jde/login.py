from selenium.webdriver.common.by import By
import time
WEBSITE_URL_JDE = "https://epm-vws20c.corp.epm.com.co/jde/E1Menu.maf"

def login(driver, username, password):
    """Realiza el inicio de sesión en la aplicación."""
    driver.get(WEBSITE_URL_JDE)

    # Localizar y completar el formulario de inicio de sesión
    driver.find_element(By.ID, "User").send_keys(username)
    driver.find_element(By.ID, "Password").send_keys(password)
    driver.find_element(By.XPATH, "//input[@value='Conexión']").click()

    # Esperar unos segundos para asegurar la carga
    time.sleep(10)
