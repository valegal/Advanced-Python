from selenium.webdriver.common.action_chains import ActionChains
import time

def verificar_carga_en_sidebar(lista, driver):
    """
    Realiza un doble clic en el botón 'Actualizar' antes de verificar.
    Verifica si alguno de los últimos cinco elementos de la lista contiene la palabra 'Carga'.
    Retorna True si la encuentra, False en caso contrario.
    """
    # Localizar el botón 'Actualizar'
    boton_actualizar = driver.find_element_by_class_name("recentReportsRefreshControl")

    # Realizar doble clic en el botón
    action = ActionChains(driver)
    action.double_click(boton_actualizar).perform()

    # Esperar un breve momento para que la acción se complete
    time.sleep(2)  # Ajusta el tiempo según sea necesario para permitir que la página actualice

    # Obtener los últimos 5 elementos
    ultimos_cinco = lista[-5:]

    # Verificar si alguno contiene la palabra 'Carga'
    for item in ultimos_cinco:
        if 'Carga' in item:
            print("Encontrado un valor con 'Carga':", item)
            return True

    print("Ninguno de los últimos cinco valores contiene 'Carga'.")
    return False
