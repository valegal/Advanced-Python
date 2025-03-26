from navigation import switch_to_iframe
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from config import fecha_con
import time

# ---------------------------------------------------

def input_estado_registro(driver):
    """Navega hasta el input 'Estado Registro' y escribe '8'"""
    try:
        # Volver al iframe `e1menuAppIframe`
        driver.switch_to.default_content()  # Salir del iframe actual
        switch_to_iframe(driver, "e1menuAppIframe")

        # Buscar el input de Estado Registro usando su ID
        input_estado_registro = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "C0_20"))
        )

        # Asegurar que el input es interactivo
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "C0_20"))
        )

        # Limpiar el campo y escribir el valor
        input_estado_registro.clear()
        input_estado_registro.send_keys("8")
        print("Escribir en input Estado Registro el número 8")

        # Hacer clic en el icono de buscar
        buscar_icon = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, "hc_Find"))
        )
        buscar_icon.click()
        print("Clic en el icono de búsqueda realizado.")
        # Esperar un momento para la ejecución del proceso
        time.sleep(10)

    except Exception as e:
        print(f"Error durante la ejecución de write_run_estado_registro: {e}")


# ---------------------------------------------------

def input_fecha_contable(driver):
    # Cambia al iframe específico
    switch_to_iframe(driver, "e1menuAppIframe")
    
    try:
        # Espera a que el campo de entrada de la fecha contable esté presente
        campo_fecha = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "C0_18"))
        )
        # Limpia el campo de texto (si tiene un valor predeterminado)
        campo_fecha.clear()
        # Ingresa la fecha contable desde la configuración
        campo_fecha.send_keys(fecha_con)
        print("Fecha contable ingresada con éxito.")
    except Exception as e:
        print(f"Error al intentar ingresar la fecha contable: {e}")
    finally:
        # Espera adicional para permitir que el sistema procese el ingreso
        time.sleep(2)
