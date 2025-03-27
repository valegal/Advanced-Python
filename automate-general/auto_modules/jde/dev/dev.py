from config import setup_driver
from login import login
from utils import take_screenshot
from config import fecha_con, fecha_gen
from navigation import switch_to_iframe
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pyautogui
import time


def main():
    driver = setup_driver()

    # Realizar el login
    login(driver, "EMONTANC", "edmcESSA07**")

    # Esperar unos segundos para cambiar de ventana si es necesario
    time.sleep(6)

    # Hacer scroll antes de buscar la pestaña
    pyautogui.scroll(-500)
    time.sleep(2)

    # Intentar localizar la pestaña correcta
    pestañas = list(pyautogui.locateAllOnScreen("pes_factura.png", confidence=0.8))
    print(f"Se encontraron {len(pestañas)} coincidencias para la pestaña de facturación.")

    if pestañas:
        pestaña_correcta = pestañas[0]  # Tomar la primera coincidencia
        pyautogui.moveTo(pestaña_correcta)  # Mover el cursor primero
        time.sleep(1)  # Espera para mayor precisión
        pyautogui.click()
        print("Pestaña encontrada y clickeada.")
        time.sleep(5)
    else:
        print("No se encontró la pestaña. Verifica la imagen y la confianza.")

    # Hacer scroll nuevamente por si el botón está fuera de vista
    pyautogui.scroll(-300)
    time.sleep(6)

    # Intentar localizar y hacer clic en el botón correcto
    botones = list(pyautogui.locateAllOnScreen("Carga_ArchivoIF.png", confidence=0.8))
    print(f"Se encontraron {len(botones)} coincidencias para el botón de carga.")

    if botones:
        boton_correcto = botones[0]  # Tomar la primera coincidencia
        pyautogui.moveTo(boton_correcto)  # Mover el cursor primero
        time.sleep(1)  # Pausa para mayor precisión
        pyautogui.click()
        print("Botón encontrado y clickeado.")
        time.sleep(5)
    else:
        print("No se encontró el botón de carga.")

    # Volver al iframe e1menuAppIframe
    driver.switch_to.default_content()
    switch_to_iframe(driver, "e1menuAppIframe")

    fase = '01'
    
    # Buscar y escribir la fecha contable
    input_fecha = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@title='FECHA CONTABLE']"))
    )
    input_fecha.clear()
    input_fecha.send_keys(fecha_con)

    # Buscar y escribir la fase
    input_fase = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@title='FASE']"))
    )
    input_fase.clear()
    input_fase.send_keys(fase)

    time.sleep(1)

    # Buscar y hacer clic en el botón de búsqueda
    botones_buscar = list(pyautogui.locateAllOnScreen("boton_buscar.png", confidence=0.8))
    print(f"Se encontraron {len(botones_buscar)} coincidencias para el botón buscar.")

    if botones_buscar:
        boton_buscar = botones_buscar[0]  # Tomar la primera coincidencia
        pyautogui.moveTo(boton_buscar)  # Mover el cursor primero
        time.sleep(1)  # Espera para mayor precisión
        pyautogui.click()
        print("Botón buscar encontrado y clickeado.")
        time.sleep(5)
    else:
        print("No se encontró el botón buscar.")

    time.sleep(7)
    
    # Cerrar el navegador
    driver.quit()

if __name__ == "__main__":
    main()
