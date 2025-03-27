from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
import time

def goto_verificar(driver):
    """
    Esta función automatiza la verificación de tareas y su estado dentro de un iframe,
    luego cierra sesión en la plataforma.
    """
    
    # Hacer clic en el icono de la tabla
    icono = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='listRRpt_WSJ']/table/tbody/tr/td[1]"))
    )
    icono.click()
    time.sleep(7)

    # Cambiar al iframe
    driver.switch_to.frame(driver.find_element(By.ID, "e1menuAppIframe"))
    
    # Obtener nombres de las tareas
    tareas = {}
    for i in range(10):
        tarea_xpath = f"//*[@id='G0_1_R{i}']/td[4]/div"
        estado_xpath = f"//*[@id='G0_1_R{i}']/td[5]/div"
        
        tarea_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, tarea_xpath))
        )
        estado_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, estado_xpath))
        )
        
        tareas[tarea_element.text] = estado_element.text
    
    print(tareas)
    time.sleep(5)
    
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
    
    time.sleep(5)