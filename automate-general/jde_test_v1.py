from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
import time

# Configuración del driver
website_jde = "https://epm-vws20c.corp.epm.com.co/jde/E1Menu.maf"
path = r"C:\Users\vgaleanc\Escritorio\chromedriver-win64\chromedriver.exe"

# Inicializar el servicio y el driver
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)

try:
    # Abrir la página web
    driver.set_window_position(1920, 0)
    driver.maximize_window()
    driver.get(website_jde)

    # Iniciar sesión
    input_login_jde = driver.find_element(By.ID, "User")
    input_login_jde.send_keys("EMONTANC")
    input_login_jde = driver.find_element(By.ID, "Password")
    input_login_jde.send_keys("edmcESSA02**")
    boton_conexion = driver.find_element(By.XPATH, "//input[@value='Conexión']")
    boton_conexion.click()

    # Esperar a que la página cargue completamente
    time.sleep(5)

#----- IR A LA VISTA DE CARGA ARCHIVO INTERFAZ -----

    # Cambiar al iframe `e1menuAppIframe`
    iframe = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "e1menuAppIframe"))
    )
    driver.switch_to.frame(iframe)

    # Localizar la pestaña `tab3`
    tab_cp = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "tab3")))

    # Usar ActionChains para simular un clic real
    action = ActionChains(driver)
    action.move_to_element(tab_cp).click().perform()

    # Cambiar al segundo iframe
    second_iframe = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "wcFrame3"))
    )
    driver.switch_to.frame(second_iframe)

    # Cambiar al tercer iframe
    third_iframe = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "RIPaneIFRAME1"))
    )
    driver.switch_to.frame(third_iframe)

    # Buscar el elemento deseado dentro del tercer iframe
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
            ActionChains(driver).move_to_element(target_element).click().perform()
            print("¡Clic realizado exitosamente!")
        except ElementClickInterceptedException:
            print("Elemento bloqueado por otro elemento, intentando clic con JavaScript.")
            # Forzar clic con JavaScript
            driver.execute_script("arguments[0].click();", target_element)
    else:
        print("El elemento no es interactivo o está oculto.")

#----- TABLA DE REGISTROS EN LA CARGA ARCHIVO INTERFAZ -----

    # Volver al iframe `e1menuAppIframe`
    driver.switch_to.default_content()  # Salir del iframe actual

    driver.switch_to.frame(iframe)
    print("Estamos en el iframe e1menuAppIframe")

    # Buscar el input de fecha y escribir '20150914' o '20160208'
    input_fecha = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@title='FECHA DE GENERACIÓN EN LA INTERFACE']"))
    )
    input_fecha.clear()
    input_fecha.send_keys('20150914')
    print("Fecha escrita en el campo 'FECHA DE GENERACIÓN EN LA INTERFACE'.")

    # Hacer clic en el icono de buscar
    buscar_icon = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "hc_Find"))
    )
    buscar_icon.click()
    print("Clic en el icono de búsqueda realizado.")
    time.sleep(3)

#----- FIN DEL PROCESO -----


except Exception as e:
    print(f"Error durante la ejecución: {e}")
    # Tomar una captura de pantalla para depuración
    driver.save_screenshot("debug_screenshot.png")
    print("Captura de pantalla guardada como 'debug_screenshot.png'")

finally:
    # Mantener el navegador abierto para depuración
    input("Presiona Enter para cerrar la ventana...")
    driver.quit()
