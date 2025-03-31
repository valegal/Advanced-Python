from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from navigation import switch_to_iframe, navigate_home
import time

def action_cargar_fases(driver, fecha_con):
    fases = ['01', '02', '03', '04', '05']  # Lista de fases a recorrer
    
    for fase in fases:
        try:
            # Volver al iframe `e1menuAppIframe`
            driver.switch_to.default_content()
            switch_to_iframe(driver, "e1menuAppIframe")
            
            # Buscar el input de fecha y escribir
            input_fecha = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[@title='FECHA CONTABLE']"))
            )
            input_fecha.clear()
            input_fecha.send_keys(fecha_con)
            
            # Buscar el input de fase y escribir
            input_fase = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[@title='FASE']"))
            )
            input_fase.clear()
            input_fase.send_keys(fase)
            
            print(f"Fecha: {fecha_con} y Fase: {fase} escrita en los filtros.")
            
            # Hacer clic en el icono de buscar
            buscar_icon = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.ID, "hc_Find"))
            )
            buscar_icon.click()
            
            time.sleep(2)
            
            tabla = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "jdeGridData0_1.0"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tabla)

            time.sleep(5)
            
            # Intentar hacer clic en la imagen de "Sin anexos" con reintentos
            intento = 0
            while intento < 3:
                try:
                    elemento_clic = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, ".//td[@colindex='-2']//a/img[@title='Sin anexos']"))
                    )
                    ActionChains(driver).move_to_element(elemento_clic).click().perform()
                    break
                except Exception:
                    intento += 1
                    time.sleep(1)
        
            time.sleep(1)
            # Localizar y hacer clic en el botón "Ejecutar Carga"
            ejecutar_carga_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='G0_1_R0']/td[2]/div/a"))
            )
            ActionChains(driver).move_to_element(ejecutar_carga_button).click().perform()
            
            # Hacer clic en el icono de OK
            ok_icon = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.ID, "hc_OK"))
            )
            ok_icon.click()
            
            # Esperar 3 segundos antes de continuar con la siguiente fase
            
            
            print(f"Fase {fase} procesada correctamente.")
        except Exception as e:
            print(f"Error en la fase {fase}: {str(e)}")
            driver.save_screenshot(f"error_state_fase_{fase}.png")
    
    time.sleep(100000000)
    # Finalizar volviendo a la vista home
    navigate_home(driver)
    time.sleep(4)
    
    print("Proceso de carga de fases finalizado.")


# ------------------------------------------------

def agrupar(driver, numero):
    # Volver al iframe `e1menuAppIframe`
    driver.switch_to.default_content()
    switch_to_iframe(driver, "e1menuAppIframe")
    
    # Paso 1: Buscar el botón de envío, mover el cursor hasta él y hacer clic
    boton_envio = driver.find_element(By.XPATH, "//*[@id='outer0_30']")
    ActionChains(driver).move_to_element(boton_envio).click().perform()

    time.sleep(5)
    
    # Paso 2: Buscar el input, borrar su contenido y escribir el número correspondiente
    input_campo = driver.find_element(By.XPATH, "//*[@id='PO1T0']")
    input_campo.click()
    input_campo.send_keys(Keys.BACKSPACE * 10)  # Borrar varias veces
    for digito in str(numero):
        input_campo.send_keys(digito)
        time.sleep(0.2)  # Pequeña pausa para simular escritura humana
    
    # Paso 3: Buscar el botón OK, mover el cursor y hacer clic
    boton_ok = driver.find_element(By.XPATH, "//*[@id='hc_Select']")
    ActionChains(driver).move_to_element(boton_ok).click().perform()
    
    # Esperar 10 segundos antes del siguiente paso
    time.sleep(10)
    
    # Paso 4: Buscar el otro botón OK, mover el cursor y hacer clic
    boton_final = driver.find_element(By.XPATH, "//*[@id='hc_OK']")
    ActionChains(driver).move_to_element(boton_final).click().perform()
    
    # Esperar 15 segundos antes de continuar
    time.sleep(15)
    
    print(f"Proceso de agrupación finalizado para {numero}.")

# ------------------------------------------------

def generar_movimiento_contable(driver, bcg):
    # Volver al iframe `e1menuAppIframe`
    driver.switch_to.default_content()
    switch_to_iframe(driver, "e1menuAppIframe")
    
    # Paso 1: Buscar el botón de envío, mover el cursor hasta él y hacer clic
    boton_envio = driver.find_element(By.XPATH, "//*[@id='divC0_30']/span")
    ActionChains(driver).move_to_element(boton_envio).click().perform()

    time.sleep(5)
    
    # Paso 2: Buscar el input, borrar su contenido y escribir el número correspondiente
    input_campo = driver.find_element(By.XPATH, "//*[@id='PO7T0']")
    input_campo.click()
    input_campo.send_keys(Keys.BACKSPACE * 10)  # Borrar varias veces
    for digito in str(bcg):
        input_campo.send_keys(digito)
        time.sleep(0.2)  # Pequeña pausa para simular escritura humana
    
    # Paso 3: Buscar el botón OK, mover el cursor y hacer clic
    boton_ok = driver.find_element(By.XPATH, "//*[@id='hc_Select']")
    ActionChains(driver).move_to_element(boton_ok).click().perform()
    
    # Esperar 10 segundos antes del siguiente paso
    time.sleep(3)
    
    # Paso 4: Buscar el otro botón OK, mover el cursor y hacer clic
    boton_final = driver.find_element(By.XPATH, "//*[@id='hc_OK']")
    ActionChains(driver).move_to_element(boton_final).click().perform()
    
    # Esperar 15 segundos antes de continuar
    time.sleep(3)
    
    print(f"Proceso de generar movimiento contable finalizado para {bcg}.")