from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
import time

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

    # Localizar y hacer clic en la pestaña `tab3`
    tab_cp = WebDriverWait(driver, 150).until(
        EC.presence_of_element_located((By.ID, "tab3"))
    )
    action = ActionChains(driver)
    action.move_to_element(tab_cp).click().perform()
    # Cambiar al segundo y tercer iframe
    switch_to_iframe(driver, "wcFrame3")
    switch_to_iframe(driver, "RIPaneIFRAME1")

    # Localizar el elemento objetivo y hacer clic
    target_element = WebDriverWait(driver, 150).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='Carga Archivo Interfaz Facturación - Contabilidad']"))
    )

    # Forzar desplazamiento para visibilidad
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_element)
    time.sleep(3)  # Esperar un momento después del desplazamiento

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
def navigate_to_revision_hechos(driver):
    """Navega a la vista de revisión hechos económicos"""
    # Cambiar al primer iframe
    switch_to_iframe(driver, "e1menuAppIframe")

    # Localizar y hacer clic en la pestaña `tab3`
    tab_cp = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.ID, "tab3"))
    )
    action = ActionChains(driver)
    action.move_to_element(tab_cp).click().perform()
    # Cambiar al segundo y tercer iframe
    switch_to_iframe(driver, "wcFrame3")
    switch_to_iframe(driver, "RIPaneIFRAME1")

    # Localizar el elemento objetivo y hacer clic
    target_element = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='Revisión Hechos Económicos Interfaz Facturación']"))
    )

    # Forzar desplazamiento para visibilidad
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_element)
    time.sleep(3)  # Esperar un momento después del desplazamiento

    # Verificar si el elemento está visible
    if target_element.is_displayed():
        try:
            # Intentar clic con ActionChains
            action.move_to_element(target_element).click().perform()
            print("¡Entramos a Revisión Hechos Económicos!")
        except ElementClickInterceptedException:
            print("Elemento bloqueado por otro elemento, intentando clic con JavaScript.")
            # Forzar clic con JavaScript
            driver.execute_script("arguments[0].click();", target_element)
    else:
        print("El elemento no es interactivo o está oculto.")


#           TRES
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
        except Exception as e:
            print(f"Error al hacer clic en el logotipo de Oracle: {e}")
            return
        
# ------------------------------------------------

def close_page(driver):

    try:
        boton_close = driver.find_element(By.XPATH, "//*[@id='hc_Close']")
        ActionChains(driver).move_to_element(boton_close).click().perform()

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
    """Navega a la vista de Control Archivos Cargados"""
    # Cambiar al primer iframe
    switch_to_iframe(driver, "e1menuAppIframe")

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
    target_element = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='Control Archivos Cargados']"))
    )

    # Forzar desplazamiento para visibilidad
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_element)
    time.sleep(3)  # Esperar un momento después del desplazamiento

    # Verificar si el elemento está visible
    if target_element.is_displayed():
        try:
            # Intentar clic con ActionChains
            action.move_to_element(target_element).click().perform()
            print("¡Entramos a Control Archivos Cargados!")
        except ElementClickInterceptedException:
            print("Elemento bloqueado por otro elemento, intentando clic con JavaScript.")
            # Forzar clic con JavaScript
            driver.execute_script("arguments[0].click();", target_element)
    else:
        print("El elemento no es interactivo o está oculto.")

#           OCHO
#       ██████   ███     
#      ██    ██   ██     
#      ██    ██   ██     
#      ██    ██   ██     
#       ██████   ████ 

# ------------------------------------------------

def navigate_agrupacion_hechos(driver):
    """Navega a la vista de Agrupación Hechos Económicos IF"""
    # Cambiar al primer iframe
    driver.switch_to.default_content()
    switch_to_iframe(driver, "e1menuAppIframe")

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
    target_element = WebDriverWait(driver, 100).until(
    EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Agrupación Hechos Económicos Interfaz Facturación')]"))
    )

    # Forzar desplazamiento para visibilidad
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_element)
    time.sleep(3)  # Esperar un momento después del desplazamiento

    # Verificar si el elemento está visible
    if target_element.is_displayed():
        try:
            # Intentar clic con ActionChains
            action.move_to_element(target_element).click().perform()
            print("¡Entramos a Agrupación Hechos Económicos IF!")
        except ElementClickInterceptedException:
            print("Elemento bloqueado por otro elemento, intentando clic con JavaScript.")
            # Forzar clic con JavaScript
            driver.execute_script("arguments[0].click();", target_element)
    else:
        print("El elemento no es interactivo o está oculto.")

#           OCHO
#       ██████   ███     
#      ██    ██   ██     
#      ██    ██   ██     
#      ██    ██   ██     
#       ██████   ████ 

# ------------------------------------------------

def navigate_generar_mov_contable(driver):
    """Navega a la vista de Generar Movimiento Contable IF"""
    # Cambiar al primer iframe
    driver.switch_to.default_content()
    switch_to_iframe(driver, "e1menuAppIframe")

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
    target_element = WebDriverWait(driver, 100).until(
    EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Generar Movimiento Contable Interfaz Facturación')]"))
    )

    # Forzar desplazamiento para visibilidad
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_element)
    time.sleep(3)  # Esperar un momento después del desplazamiento

    # Verificar si el elemento está visible
    if target_element.is_displayed():
        try:
            # Intentar clic con ActionChains
            action.move_to_element(target_element).click().perform()
            print("¡Entramos a Generar Movimiento Contable Interfaz Facturación!")
        except ElementClickInterceptedException:
            print("Elemento bloqueado por otro elemento, intentando clic con JavaScript.")
            # Forzar clic con JavaScript
            driver.execute_script("arguments[0].click();", target_element)
    else:
        print("El elemento no es interactivo o está oculto.")

#           OCHO
#       ██████   ███     
#      ██    ██   ██     
#      ██    ██   ██     
#      ██    ██   ██     
#       ██████   ████ 

# ------------------------------------------------

def navigate_AD(driver):
    """Navega a la vista de Control Archivos Cargados en la plataforma sin ir al tab3"""
    # Cambiar al primer iframe
    switch_to_iframe(driver, "e1menuAppIframe")
    action = ActionChains(driver)
    # Cambiar al segundo y tercer iframe
    switch_to_iframe(driver, "wcFrame3")
    switch_to_iframe(driver, "RIPaneIFRAME1")

    # Localizar el elemento objetivo y hacer clic
    target_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='Revisiones de AD (Batch)']"))
    )

    # Forzar desplazamiento para visibilidad
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_element)
    time.sleep(1)  # Esperar un momento después del desplazamiento
    
    # Verificar si el elemento está visible
    if target_element.is_displayed():
        try:
            # Intentar clic con ActionChains
            action.move_to_element(target_element).click().perform()
            print("¡Open OneWorld: Revisiones de AD (Batch)!")
        except ElementClickInterceptedException:
            print("Elemento bloqueado por otro elemento, intentando clic con JavaScript.")
            # Forzar clic con JavaScript
            driver.execute_script("arguments[0].click();", target_element)
    else:
        print("El elemento no es interactivo o está oculto.")

#           OCHO
#       ██████   ███     
#      ██    ██   ██     
#      ██    ██   ██     
#      ██    ██   ██     
#       ██████   ████ 

# ------------------------------------------------

def navigate_revision_comprobante(driver):
    """Navega a la vista de Control Archivos Cargados en la plataforma sin ir al tab3"""
    # Cambiar al primer iframe
    switch_to_iframe(driver, "e1menuAppIframe")
    action = ActionChains(driver)
    # Cambiar al segundo y tercer iframe
    switch_to_iframe(driver, "wcFrame3")
    switch_to_iframe(driver, "RIPaneIFRAME1")

    # Localizar el elemento objetivo y hacer clic
    target_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='Revisión del Comprobante']"))
    )

    # Forzar desplazamiento para visibilidad
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_element)
    time.sleep(1)  # Esperar un momento después del desplazamiento
    
    # Verificar si el elemento está visible
    if target_element.is_displayed():
        try:
            # Intentar clic con ActionChains
            action.move_to_element(target_element).click().perform()
            print("¡Open OneWorld: Revisión del Comprobante!")
        except ElementClickInterceptedException:
            print("Elemento bloqueado por otro elemento, intentando clic con JavaScript.")
            # Forzar clic con JavaScript
            driver.execute_script("arguments[0].click();", target_element)
    else:
        print("El elemento no es interactivo o está oculto.")

#           OCHO
#       ██████   ███     
#      ██    ██   ██     
#      ██    ██   ██     
#      ██    ██   ██     
#       ██████   ████ 

# -----------------------------------------------


#           OCHO
#       ██████   ███     
#      ██    ██   ██     
#      ██    ██   ██     
#      ██    ██   ██     
#       ██████   ████ 

# ------------------------------------------------