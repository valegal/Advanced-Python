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
    Procesa cada tabla pendiente ejecutando la función ejecutar_carga para cada una. """
    for i, id_tabla in enumerate(pendientes):
        try:
            print(f"Procesando tabla {i + 1}/{len(pendientes)}: {id_tabla}")
            ejecutar_carga(driver, id_tabla)  # Llama a ejecutar_carga con la tabla actual
            print(f"Tabla {id_tabla} procesada exitosamente.")
        except Exception as e:
            print(f"Error al procesar la tabla {id_tabla}: {e}")


def ejecutar_carga(driver, id_tabla):
    try:
        # Cambiar al contexto principal e ingresar al iframe
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
            print(f"Clic en el elemento dentro de la tabla {id_tabla} realizado.")
        except Exception as e:
            print(f"Error al localizar o hacer clic en el elemento dentro de la tabla {id_tabla}: {e}")
            return
        
        # Esperar un momento para la acción subsiguiente
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
        
        # Esperar para que la carga se procese
        time.sleep(4)

        # Clic en el botón "Cancelar" dentro del iframe
        try:
            driver.switch_to.default_content()
            switch_to_iframe(driver, "e1menuAppIframe")
            herramientas_element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='WebLabel' and @title='Herramientas (Ctrl+Alt+T)']")))
            herramientas_element.click()
            cancelar_element = WebDriverWait(driver, 40).until(
                EC.element_to_be_clickable((
                    By.XPATH, "//td[@valign='top' and @style='min-width:20px;' and @align='center']//a[img[@title='Cancelar (Ctrl+Alt+L)']]"
                ))
            )
            
            # Hacer clic en el elemento
            cancelar_element.click()
            print("Clic en el botón 'Cancelar' realizado.")
        except Exception as e:
            print(f"Error al hacer clic en el botón 'Cancelar': {e}")
            return
        
        # Esperar 5 segundos y clic en el logotipo de Oracle para volver al inicio
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
        print("Función navigate_to_carga_archivo_simple llamada exitosamente.")

    except Exception as e:
        print(f"Error en ejecutar_carga: {e}")


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
