from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
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

def logout(driver):
        # Volver al contenido principal
    driver.switch_to.default_content()

    # Hacer clic en el menú de usuario
    user_menu = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "userSessionDropdownArrow"))
    )
    user_menu.click()
    time.sleep(2)

    # Hacer clic en "Desconexión"
    logout_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "signOutLinkDiv"))
    )
    logout_button.click()
    time.sleep(1)

    # Aceptar la alerta de cierre de sesión si aparece
    try:
        alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert.accept()
    except TimeoutException:
        print("No se encontró alerta de confirmación de cierre de sesión.")

    time.sleep(3)
