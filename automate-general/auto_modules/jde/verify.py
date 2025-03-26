import time
import openpyxl
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from navigation import switch_to_iframe, navigate_home
from selenium.webdriver.common.keys import Keys
from config import fecha_con_lib


#---------------------------------------------------------

def update_excel_with_lotes(resultado):
    # Ruta del archivo Excel
    excel_path = r"D:\OneDrive - Grupo EPM\Documentos\InterfazFacturacion\07.  FFN014-V1-Formato Registro BATCH-MARZO.xlsx"
    
    # Cargar el archivo Excel
    wb = openpyxl.load_workbook(excel_path)
    
    # Obtener el día del mes desde fecha_con_lib
    dia = int(fecha_con_lib[-2:])  # Extrae los últimos dos caracteres como día
    celda_destino = f"B{7 + dia}"  # Calcula la celda destino (B8 es el día 1, B9 el día 2...)
    
    for index in range(1, len(resultado) // 2 + 1):
        nlote = resultado.get(f'nlote{index}')
        faselote = resultado.get(f'faselote{index}')
        
        if nlote and faselote:
            hoja_nombre = f"{faselote}-"
            if faselote == '1':
                hoja_nombre += "FACTURACIÓN"
            elif faselote == '3':
                hoja_nombre += "AJUSTES"
            elif faselote == '4':
                hoja_nombre += "RECAUDOS"
            else:
                continue  # Si no es una hoja esperada, continuar con el siguiente
            
            try:
                hoja = wb[hoja_nombre]
                hoja[celda_destino] = nlote  # Escribir el número de lote en la celda correspondiente
            except KeyError:
                print(f"⚠️ No se encontró la hoja {hoja_nombre} en el archivo Excel.")
    
    # Guardar los cambios en el archivo
    wb.save(excel_path)
    wb.close()
    print("✅ Archivo Excel actualizado correctamente.")

#---------------------------------------------------------

def verify_control_archivos(driver):
    driver.switch_to.default_content()
    switch_to_iframe(driver, "e1menuAppIframe")
    
    # Buscar y llenar el input de fecha contable
    input_fecha_contable = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='C0_18']"))
    )
    input_fecha_contable.click()
    input_fecha_contable.clear()
    time.sleep(1)
    
    # Eliminar cualquier carácter existente antes de escribir
    input_fecha_contable.send_keys(Keys.BACKSPACE * 10)
    time.sleep(1)
    
    # Asegurar que fecha_con_lib es una cadena
    fecha_str = str(fecha_con_lib)
    
    # Escribir la fecha carácter por carácter
    for char in fecha_str:
        input_fecha_contable.send_keys(char)
        time.sleep(0.2)  # Pequeña pausa entre caracteres
    
    time.sleep(1)

    # Buscar y hacer clic en el botón de búsqueda
    boton_buscar = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.ID, "hc_Find"))
    )
    boton_buscar.click()
    
    # Esperar a que los resultados carguen
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "JSSelectGrid"))
    )
    time.sleep(5)

    # Buscar todas las filas de la tabla
    filas = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.XPATH, "//tr[starts-with(@id, 'G0_1_R')]"))
    )
    
    # Inicializar variables dinámicas
    resultado = {}
    
    for index, fila in enumerate(filas):
        try:
            # Extraer número de lote (columna 6)
            nlote_element = fila.find_element(By.XPATH, ".//td[6]/div")
            nlote_value = nlote_element.text.replace(",", "").strip()
            
            # Extraer fase de lote (columna 0)
            faselote_element = fila.find_element(By.XPATH, ".//td[2]/div")
            faselote_value = faselote_element.text.strip()
            
            # Asignar valores a variables dinámicas
            resultado[f'nlote{index+1}'] = nlote_value
            resultado[f'faselote{index+1}'] = faselote_value
            
        except NoSuchElementException:
            print(f"⚠️ No se encontró uno de los valores en la fila {index+1}.")

    update_excel_with_lotes(resultado)
    return resultado

#---------------------------------------------------------

def verify_estado_trabajo(driver):
    driver.switch_to.default_content()
    
    # Esperar a que el elemento esté visible antes de buscarlo y hacerle clic
    try:
        elemento = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "listRRpt_WSJ"))
        )
        elemento.click()
    except TimeoutException:
        print("Error: No se encontró el elemento para ver el estado de trabajo.")
        return
    
    time.sleep(5)
    # Cambiar al iframe donde está la tabla
    switch_to_iframe(driver, "e1menuAppIframe")
    
    tiempo_maximo = 25 * 60  # 25 minutos en segundos
    intervalo_verificacion = 120  # 2 minutos en segundos
    tiempo_transcurrido = 0
    
    while tiempo_transcurrido < tiempo_maximo:
        try:
            # Esperar a que las filas estén presentes
            filas = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@id, 'G0_1_R')]"))
            )[:5]
            
            if not filas:
                print("No se encontraron filas en la tabla.")
                return
            
            estados = []
            for fila in filas:
                try:
                    celda_estado = WebDriverWait(fila, 5).until(
                        EC.presence_of_element_located((By.XPATH, ".//td[@colindex='9']/div"))
                    )
                    estado = celda_estado.get_attribute("innerText").strip()
                    print(f"Estado encontrado en fila: {estado}")  # Depuración
                    estados.append(estado)
                except TimeoutException:
                    print("No se encontró el estado en una fila.")
                    estados.append(None)
            
            # Imprimir la información de la lista estados
            print("Estados encontrados:", estados)
            
            # Verificar si todas están en "Hecho"
            if all(estado == "Hecho" for estado in estados if estado is not None):
                print("Verificación: Todas las fases cargadas y listas para revisión")
                navigate_home(driver)
                return
        except TimeoutException:
            print("Error: No se pudo cargar la tabla a tiempo.")
            return
    
        # Esperar 2 minutos antes de la siguiente verificación
        time.sleep(intervalo_verificacion)
        tiempo_transcurrido += intervalo_verificacion
    
    # Si después de 25 minutos no todas están en "Hecho", cerrar el navegador
    print("Error: No todas las fases están en 'Hecho' después de 25 minutos. Cerrando el navegador.")
    driver.quit()
