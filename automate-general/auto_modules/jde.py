from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException, ElementClickInterceptedException, TimeoutException
from navigation import switch_to_iframe
from navigation import navigate_to_carga_archivo, navigate_to_carga_archivo_simple
import time

def procesar_pendientes(driver, pendientes):
    """
    Procesa cada tabla pendiente ejecutando la función ejecutar_carga para cada una.
    """
    if not pendientes:
        print("No hay tablas pendientes para procesar.")
        return
    
    for i, id_tabla in enumerate(pendientes):
        try:
            print(f"Procesando tabla {i + 1}/{len(pendientes)}: {id_tabla}")
            # Ejecutar la función para procesar la tabla
            ejecutar_carga(driver, id_tabla)
            print(f"Tabla {id_tabla} procesada exitosamente.")
        except Exception as e:
            # Captura cualquier error pero continúa con el siguiente pendiente
            print(f"Error al procesar la tabla {id_tabla}: {e}")
            continue  # Aseguramos que pase al siguiente elemento
    print("Todos los pendientes han sido procesados.")

def ejecutar_carga(driver, id_tabla):
    try:
        driver.switch_to.default_content()
        switch_to_iframe(driver, "e1menuAppIframe")

        # Localizar la tabla por su ID
        tabla = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, id_tabla))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tabla)
        print(f"Tabla {id_tabla} localizada y visible.")
        
        # Buscar el elemento dentro de la tabla y darle clic
        try:
            elemento_clic = tabla.find_element(
                By.XPATH, ".//td[@colindex='-2']//a/img[@title='Sin anexos']"
            )
            ActionChains(driver).move_to_element(elemento_clic).click().perform()
            print(f"Check en {id_tabla} HECHO.")
        except Exception as e:
            print(f"Error al localizar o hacer clic en el elemento dentro de la tabla {id_tabla}: {e}")
            return
        time.sleep(2)
        # Localizar y hacer doble clic en el botón "Ejecutar Carga"
        try:
            ejecutar_carga_boton = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "C0_28"))
            )
            ActionChains(driver).move_to_element(ejecutar_carga_boton).double_click().perform()
            print(f"Botón 'Ejecutar Carga' clickeado para la tabla {id_tabla}.")
        except Exception as e:
            print(f"Error al hacer clic en el botón 'Ejecutar Carga': {e}")
            return
        
        time.sleep(4)

        # Clic en el botón "Cancelar" dentro del iframe
        try:
            driver.switch_to.default_content()
            switch_to_iframe(driver, "e1menuAppIframe")
            herramientas_element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='WebLabel' and @title='Herramientas (Ctrl+Alt+T)']")))
            herramientas_element.click()
            buscar_cancel = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "hc_Cancel")))
            buscar_cancel.click()
            time.sleep(4)
            print("Clic en el botón 'Cancelar' realizado.")
        except Exception as e:
            print(f"Error al hacer clic en el botón 'Cancelar': {e}")
            return
        
        time.sleep(5)

        try:
            driver.switch_to.default_content()
            oracle_logo = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "oracleImage"))
            )
            oracle_logo.click()
            print("Clic en el logotipo de Oracle realizado para volver al inicio.")
        except Exception as e:
            print(f"Error al hacer clic en el logotipo de Oracle: {e}")
            return
        
        # Llamar a la función navigate_to_carga_archivo_simple
        navigate_to_carga_archivo_simple(driver)
        print(f"Función navigate_to_carga_archivo_simple en {id_tabla}")
        print("------ Repeat ------")

    except Exception as e:
        print(f"Error en ejecutar_carga: {e}")



