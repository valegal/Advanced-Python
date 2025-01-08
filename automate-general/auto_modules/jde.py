from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
from navigation import switch_to_iframe
from navigation import navigate_to_carga_archivo
import time

def procesar_pendientes(driver, pendientes):

    """
    Procesa cada tabla pendiente ejecutando la función ejecutar_carga para cada una. """
    for i, id_tabla in enumerate(pendientes):
        try:
            print(f"Procesando tabla {i + 1}/{len(pendientes)}: {id_tabla}")
            ejecutar_carga(driver, id_tabla)  # Llama a ejecutar_carga con la tabla actual
            print(f"Tabla {id_tabla} procesada exitosamente.")
        except Exception as e:
            print(f"Error al procesar la tabla {id_tabla}: {e}")


def ejecutar_carga(driver, id_tabla):

            driver.switch_to.default_content()
            switch_to_iframe(driver, "e1menuAppIframe")
            # Localizar la tabla por su ID
            tabla = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, id_tabla))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tabla)
            print(f"Tabla {id_tabla} localizada y visible.")

            # Buscar el elemento dentro de la tabla y darle clic
            elemento_clic = tabla.find_element(By.XPATH, 
                ".//td[@colindex='-2']//a/img[@title='Sin anexos']"
            )
            ActionChains(driver).move_to_element(elemento_clic).click().perform()
            print(f"Clic en el elemento dentro de la tabla {id_tabla} realizado.")
            time.sleep(2) 
            # Clic en el botón "Ejecutar Carga"
            ejecutar_carga_boton = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "C0_28"))
            )
            ActionChains(driver).move_to_element(ejecutar_carga_boton).double_click().perform()
            print(f"Botón 'Ejecutar Carga' clickeado para la tabla {id_tabla}.")
            time.sleep(4) 

            # Cambiar al iframe en la nueva vista
            driver.switch_to.default_content()
            switch_to_iframe(driver, "e1menuAppIframe")

            # Localizar el botón "Cancelar" y darle clic
            cancelar_boton = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.ID, "jdeclose_ena"))
            )
            ActionChains(driver).move_to_element(cancelar_boton).double_click().perform()
            print(f"Botón 'Cancelar' clickeado en la vista secundaria para la tabla {id_tabla}.")
            time.sleep(2)

            driver.switch_to.default_content()
            switch_to_iframe(driver, "e1menuAppIframe")

            # Localizar el botón "Cancelar" en carga de archivos y darle clic
            cancelar_boton_2 = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.ID, "outer0_13"))
            )
            ActionChains(driver).move_to_element(cancelar_boton_2).double_click().perform()
            print(f"Botón 'Cancelar' clickeado para la tabla {id_tabla} vuelve a la vista principal.")

            time.sleep(2)
            navigate_to_carga_archivo(driver)

def informes_recientes_estado(driver):
    driver.switch_to.default_content()
    """
    Extrae los textos de los últimos diez registros en la lista con id 'listRecRpts'.
    
    """
    try:
        # Localizar la lista de registros recientes
        lista_elementos = driver.find_elements(By.CSS_SELECTOR, "#listRecRptsInner .listItem .listText")
        
        # Extraer los textos de los elementos
        textos_registros = [elemento.text for elemento in lista_elementos]
        
        # Tomar los últimos diez registros (o menos si no hay suficientes)
        ultimos_diez_registros = textos_registros[-10:]
        
        return ultimos_diez_registros
    
    except Exception as e:
        print(f"Error al obtener los últimos diez registros: {e}")
        return []
