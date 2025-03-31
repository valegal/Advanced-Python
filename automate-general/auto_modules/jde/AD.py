from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyautogui

def buscar_revisiones_AD(driver):
    try:
        # Esperar y cambiar al iframe
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "e1menuAppIframe"))
        )

        # Esperar el campo de texto y escribir en él
        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='qbeRow0_1']/td[2]/div/nobr/input"))
        )
        input_field.click()
        input_field.clear()
        input_field.send_keys("EMONTANC")
        time.sleep(3)
        
        # Buscar el botón de búsqueda y hacer clic
        search_button = driver.find_element(By.ID, "hc_Find")
        search_button.click()
        
        # Esperar a que cargue el siguiente elemento moviendo el mouse sutilmente
        while True:
            try:
                next_element = WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located((By.XPATH, "XPATH_DEL_SIGUIENTE_ELEMENTO"))
                )
                break  # Sale del loop cuando el elemento aparece
            except:
                pyautogui.moveRel(1, 0)  # Mueve el mouse sutilmente para evitar interrupciones
                time.sleep(2)  # Pequeña espera antes de intentar de nuevo
    
        print("Carga completa, elemento encontrado.")
    except Exception as e:
        print(f"Error: {e}")
