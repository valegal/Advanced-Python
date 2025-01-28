from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from navigation import switch_to_iframe
import time

def clic_boton_envio(driver):
    # Cambia al iframe "e1menuAppIframe"
    switch_to_iframe(driver, "e1menuAppIframe")
    
    try:
        # Espera a que el botón esté presente y sea interactivo dentro del iframe
        boton_envio = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "divC0_30"))
        )
        # Da clic al botón
        boton_envio.click()
    except Exception as e:
        print(f"Error al intentar clicar el botón de envío: {e}")
    finally:
        # Espera adicional después de realizar la acción
        time.sleep(5)
#----------------------------------------------------------

def clic_boton_lupa(driver):
    # Cambia al contexto principal y luego al iframe
    driver.switch_to.default_content()
    switch_to_iframe(driver, "e1menuAppIframe")
    
    try:
        # Espera a que el botón "Buscar" esté presente e interactivo
        boton_buscar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "hc_Find"))
        )
        # Da clic en el botón
        boton_buscar.click()
        print("Botón 'Buscar' clicado con éxito.")
    except Exception as e:
        print(f"Error al intentar clicar el botón 'Buscar': {e}")
    finally:
        # Espera adicional después de realizar la acción
        time.sleep(3)