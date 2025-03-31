from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
import time

def goto_verificar(driver, files):
    """
    Esta función automatiza la verificación del estado de trabajo de las tareas
    """

    # Hacer clic en el icono de la tabla
    icono = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='listRRpt_WSJ']/table/tbody/tr/td[1]"))
    )
    icono.click()
    time.sleep(7)

    # Cambiar al iframe
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "e1menuAppIframe")))
    driver.switch_to.frame(driver.find_element(By.ID, "e1menuAppIframe"))

    # Lista para almacenar tareas (mantiene valores repetidos)
    tareas = []

    for i in range(files):  # Iterar sobre todas las filas disponibles
        try:
            tarea_xpath = f"//*[@id='G0_1_R{i}']/td[4]/div"
            estado_xpath = f"//*[@id='G0_1_R{i}']/td[9]/div"

            tarea_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, tarea_xpath))
            )
            estado_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, estado_xpath))
            )

            tareas.append((tarea_element.text, estado_element.text))

        except (NoSuchElementException, TimeoutException, StaleElementReferenceException) as e:
            print(f"Error al obtener datos en la fila {i}: {e}")

    # Imprimir los resultados
    print(tareas)

    time.sleep(5)

    # Aceptar la alerta de cierre de sesión si aparece
    try:
        alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert.accept()
    except TimeoutException:
        print("No se encontró alerta de confirmación de cierre de sesión.")

    time.sleep(3)

    return tareas



#-----------------------------------------------------------------------------

def esperar_tareas_completas(driver, files, max_retries=6, retry_interval=300):
    """
    Ejecuta goto_verificar hasta que todas las tareas estén en estado 'Hecho' 
    o hasta alcanzar el tiempo máximo de espera (30 min).
    """
    for attempt in range(max_retries):
        tareas = goto_verificar(driver, files)

        if not tareas:  # Si la lista es None o vacía, prevenir errores
            print("⚠️ No se encontraron tareas. Reintentando...")
            time.sleep(retry_interval)
            continue

        # Verifica si todas las tareas están en estado 'Hecho'
        if all(estado == "Hecho" for _, estado in tareas):  # Tomar el segundo valor de cada tupla
            print("✅ Todas las tareas están en estado 'Hecho'. Continuando...")
            return True  # Indica que las tareas están listas

        print(f"🔄 Intento {attempt + 1}/{max_retries}: Algunas tareas no están listas. Esperando {retry_interval // 60} min...")
        time.sleep(retry_interval)

    print("⚠️ Se alcanzó el tiempo máximo de espera (30 min). Continuando con el proceso...")
    return False  # Indica que el tiempo máximo se alcanzó sin completar todas las tareas
