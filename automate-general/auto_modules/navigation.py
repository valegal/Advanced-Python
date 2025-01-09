from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
import time
from utils import take_screenshot

# ------------------------------------------------
def switch_to_iframe(driver, iframe_id):
    """Cambia al iframe especificado."""
    iframe = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, iframe_id))
    )
    driver.switch_to.frame(iframe)

#           UNO
#       ██████   ███     
#      ██    ██   ██     
#      ██    ██   ██     
#      ██    ██   ██     
#       ██████   ████   

# ------------------------------------------------
def navigate_to_carga_archivo(driver):
    """Navega a la vista de carga de archivo en la plataforma."""
    # Cambiar al primer iframe
    switch_to_iframe(driver, "e1menuAppIframe")
    action = ActionChains(driver)

    # Localizar y hacer clic en la pestaña `tab3`
    tab_cp = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.ID, "tab3"))
    )
    action = ActionChains(driver)
    action.move_to_element(tab_cp).click().perform()
    # Cambiar al segundo y tercer iframe
    switch_to_iframe(driver, "wcFrame3")
    switch_to_iframe(driver, "RIPaneIFRAME1")

    # Localizar el elemento objetivo y hacer clic
    target_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='Carga Archivo Interfaz Facturación - Contabilidad']"))
    )

    # Forzar desplazamiento para visibilidad
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_element)
    time.sleep(1)  # Esperar un momento después del desplazamiento

    # Verificar si el elemento está visible
    if target_element.is_displayed():
        try:
            # Intentar clic con ActionChains
            action.move_to_element(target_element).click().perform()
            print("¡Entramos a Carga Archivo Facturación!")
        except ElementClickInterceptedException:
            print("Elemento bloqueado por otro elemento, intentando clic con JavaScript.")
            # Forzar clic con JavaScript
            driver.execute_script("arguments[0].click();", target_element)
    else:
        print("El elemento no es interactivo o está oculto.")

#           DOS
#       ██████   ███     
#      ██    ██   ██     
#      ██    ██   ██     
#      ██    ██   ██     
#       ██████   ████   

# -------------------------------------------------
def navigate_to_fecha_gen(driver, fecha):
    """Navega hasta la tabla de registros y selecciona el campo de fecha."""
    # Volver al iframe `e1menuAppIframe`
    driver.switch_to.default_content()  # Salir del iframe actual
    switch_to_iframe(driver, "e1menuAppIframe")

    # Buscar el input de fecha y escribir '20150914' o '20160208'
    input_fecha = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@title='FECHA DE GENERACIÓN EN LA INTERFACE']"))
    )
    input_fecha.clear()
    input_fecha.send_keys(fecha)
    print("Fecha escrita en el campo 'FECHA DE GENERACIÓN EN LA INTERFACE'.")

    # Hacer clic en el icono de buscar
    buscar_icon = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "hc_Find"))
    )
    buscar_icon.click()
    print("Clic en el icono de búsqueda realizado.")
    time.sleep(3)

#           TRES
#       ██████   ███     
#      ██    ██   ██     
#      ██    ██   ██     
#      ██    ██   ██     
#       ██████   ████ 

# ---------------------------------------------------
def ejecutar_carga_muchas(driver, id_tablas, fecha):
    """
    Ejecuta la carga para cada tabla no procesada en el sistema, siguiendo los pasos especificados.
    
    """
    for id_tabla in id_tablas:
        try:
            # Volver al iframe principal
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
            ActionChains(driver).move_to_element(ejecutar_carga_boton).click().perform()
            print(f"Botón 'Ejecutar Carga' clickeado para la tabla {id_tabla}.")
            time.sleep(3) 

            # Cambiar al iframe en la nueva vista
            driver.switch_to.default_content()
            switch_to_iframe(driver, "e1menuAppIframe")

            # Localizar el botón "Cancelar" y darle clic
            cancelar_boton = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "hc_Cancel"))
            )
            ActionChains(driver).move_to_element(cancelar_boton).click().perform()
            print(f"Botón 'Cancelar' clickeado en la vista secundaria para la tabla {id_tabla}.")
            time.sleep(2)
            driver.switch_to.default_content()
            switch_to_iframe(driver, "e1menuAppIframe")

            cancelar_boton_2 = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "hc_Cancel"))
            )
            ActionChains(driver).move_to_element(cancelar_boton_2).click().perform()
            print(f"Botón 'Cancelar' clickeado para la tabla {id_tabla} vuelve a la vista principal.")
            time.sleep(2)

            # Volver a la vista principal para procesar la siguiente tabla
            navigate_to_carga_archivo(driver)
            navigate_to_fecha_gen(driver, fecha)
            print(f"Preparado para procesar la siguiente tabla después de {id_tabla}.")

        except Exception as e:
            print(f"Error al procesar la tabla {id_tabla}: {e}")
            take_screenshot(driver, f"error_{id_tabla}.png")
            print(f"Captura de pantalla tomada para el error en la tabla {id_tabla}.")

#           CUATRO
#       ██████   ███     
#      ██    ██   ██     
#      ██    ██   ██     
#      ██    ██   ██     
#       ██████   ████ 

# ------------------------------------------------
def navigate_to_carga_archivo_simple(driver):
    """Navega a la vista de carga de archivo en la plataforma sin ir al tab3"""
    # Cambiar al primer iframe
    switch_to_iframe(driver, "e1menuAppIframe")
    action = ActionChains(driver)
    # Cambiar al segundo y tercer iframe
    switch_to_iframe(driver, "wcFrame3")
    switch_to_iframe(driver, "RIPaneIFRAME1")

    # Localizar el elemento objetivo y hacer clic
    target_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='Carga Archivo Interfaz Facturación - Contabilidad']"))
    )

    # Forzar desplazamiento para visibilidad
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_element)
    time.sleep(1)  # Esperar un momento después del desplazamiento

    # Verificar si el elemento está visible
    if target_element.is_displayed():
        try:
            # Intentar clic con ActionChains
            action.move_to_element(target_element).click().perform()
            print("¡Open OneWorld: Carga Archivo IF-C!")
        except ElementClickInterceptedException:
            print("Elemento bloqueado por otro elemento, intentando clic con JavaScript.")
            # Forzar clic con JavaScript
            driver.execute_script("arguments[0].click();", target_element)
    else:
        print("El elemento no es interactivo o está oculto.")

#           CINCO
#       ██████   ███     
#      ██    ██   ██     
#      ██    ██   ██     
#      ██    ██   ██     
#       ██████   ████ 

# ------------------------------------------------

def navigate_to_review_hechos_econo(driver):
    """Navega a la vista de Revisión Hechos Económicos Interfaz Facturación en la plataforma sin ir al tab3"""
    # Cambiar al primer iframe
    switch_to_iframe(driver, "e1menuAppIframe")
    action = ActionChains(driver)
    # Cambiar al segundo y tercer iframe
    switch_to_iframe(driver, "wcFrame3")
    switch_to_iframe(driver, "RIPaneIFRAME1")

    # Localizar el elemento objetivo y hacer clic
    target_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='Revisión Hechos Económicos Interfaz Facturación']"))
    )

    # Forzar desplazamiento para visibilidad
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_element)
    time.sleep(1)  # Esperar un momento después del desplazamiento
    
    # Verificar si el elemento está visible
    if target_element.is_displayed():
        try:
            # Intentar clic con ActionChains
            action.move_to_element(target_element).click().perform()
            print("¡Open OneWorld: Revisión Hechos Económicos IF!")
        except ElementClickInterceptedException:
            print("Elemento bloqueado por otro elemento, intentando clic con JavaScript.")
            # Forzar clic con JavaScript
            driver.execute_script("arguments[0].click();", target_element)
    else:
        print("El elemento no es interactivo o está oculto.")

#           SEIS
#       ██████   ███     
#      ██    ██   ██     
#      ██    ██   ██     
#      ██    ██   ██     
#       ██████   ████ 

# ------------------------------------------------

def navigate_home(driver):
        
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

#           SIETE
#       ██████   ███     
#      ██    ██   ██     
#      ██    ██   ██     
#      ██    ██   ██     
#       ██████   ████ 

# ------------------------------------------------

def navigate_control_archivos_cargados(driver):
    """Navega a la vista de Control Archivos Cargados en la plataforma sin ir al tab3"""
    # Cambiar al primer iframe
    switch_to_iframe(driver, "e1menuAppIframe")
    action = ActionChains(driver)
    # Cambiar al segundo y tercer iframe
    switch_to_iframe(driver, "wcFrame3")
    switch_to_iframe(driver, "RIPaneIFRAME1")

    # Localizar el elemento objetivo y hacer clic
    target_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='Control Archivos Cargados']"))
    )

    # Forzar desplazamiento para visibilidad
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_element)
    time.sleep(1)  # Esperar un momento después del desplazamiento
    
    # Verificar si el elemento está visible
    if target_element.is_displayed():
        try:
            # Intentar clic con ActionChains
            action.move_to_element(target_element).click().perform()
            print("¡Open OneWorld: Control Archivos Cargados!")
        except ElementClickInterceptedException:
            print("Elemento bloqueado por otro elemento, intentando clic con JavaScript.")
            # Forzar clic con JavaScript
            driver.execute_script("arguments[0].click();", target_element)
    else:
        print("El elemento no es interactivo o está oculto.")