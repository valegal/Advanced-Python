from navigation import switch_to_iframe
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time

# -------------------------------------------------
def write_run_estado_registro(driver, summary_steps):
    """Navega hasta el input 'Estado Registro' y escribe '8'"""
    # Volver al iframe `e1menuAppIframe`
    driver.switch_to.default_content()  # Salir del iframe actual
    switch_to_iframe(driver, "e1menuAppIframe")

    # Buscar el input de fecha y escribir '20150914' o '20160208'
    input_fecha = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@title='Estado Registro']"))
    )
    input_fecha.clear()
    input_fecha.send_keys(8)
    print("Escribir en input Estado Registro el número 8")

    # Hacer clic en el icono de buscar
    buscar_icon = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "hc_Find"))
    )
    buscar_icon.click()
    print("Clic en el icono de búsqueda realizado.")
    summary_steps.append("→ Realizar busqueda de errores en Hechos Económicos IF")
    time.sleep(20)

# ---------------------------------------------------