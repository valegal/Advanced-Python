from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
from navigation import switch_to_iframe
import pandas as pd

# ---------------------------------------------------
def copy_info_tabla_carga_simple(driver):
    """Copia el primer nombre y la fase de todos los archivos de la tabla"""
    # Salir del iframe actual y entrar en el iframe específico
    driver.switch_to.default_content()
    switch_to_iframe(driver, "e1menuAppIframe")
    print("Copiando infromación de la tabla Registros en Carga Archivos")
    
    celdasNombre = driver.find_elements(By.CSS_SELECTOR, "td[colindex='1'].JSGridCell.textModifier.selectedModifier div")
    celdasFase = driver.find_elements(By.CSS_SELECTOR, "td[colindex='3'].JSGridCell.textModifier.selectedModifier div")
    celdasFechaContable = driver.find_elements(By.CSS_SELECTOR, "td[colindex='4'].JSGridCell.textModifier.selectedModifier div")
    celdasFechaGen = driver.find_elements(By.CSS_SELECTOR, "td[colindex='8'].JSGridCell.textModifier.selectedModifier div")
    celdasProcesadoOW = driver.find_elements(By.CSS_SELECTOR, "td[colindex='9'].JSGridCell.textModifier.selectedModifier div")

    # Extraer el texto de cada celda y almacenarlo en listas
    nombres = [celda.text for celda in celdasNombre]
    fases = [celda.text for celda in celdasFase]
    fechaContable = [celda.text for celda in celdasFechaContable]
    fechaGen = [celda.text for celda in celdasFechaGen]
    procesadoOW = [celda.text for celda in celdasProcesadoOW]

    print("Primera fila | tabla Registros | Carga Archivo")
    print("Nombre archivo:", nombres)
    print("Fase:", fases)
    print("Fecha contable:", fechaContable)
    print("Fecha generación:", fechaGen)
    print("Procesado (S/N):", procesadoOW)
    
    return nombres, fases, fechaContable, fechaGen, procesadoOW

# ---------------------------------------------------

def copy_info_tabla_carga(driver):
    """Copia los valores de las tablas jdeGridData0_1.x, manejando casos donde no existan."""
    # Salir del iframe actual y entrar en el iframe específico
    driver.switch_to.default_content()
    switch_to_iframe(driver, "e1menuAppIframe")
    print("Estamos en el iframe e1menuAppIframe")

    # Identificar las tablas específicas
    tablas = [
        "jdeGridData0_1.0",
        "jdeGridData0_1.1",
        "jdeGridData0_1.2",
        "jdeGridData0_1.3",
        "jdeGridData0_1.4",
        "jdeGridData0_1.5",
        "jdeGridData0_1.6",
        "jdeGridData0_1.7",
        "jdeGridData0_1.8",
        "jdeGridData0_1.9",
    ]
    
    # Inicializar lista para almacenar los resultados
    registros = []

    for tabla_id in tablas:
        try:
            # Buscar la tabla por ID
            tabla = driver.find_element(By.ID, tabla_id)
            
            # Extraer los valores de las celdas específicas dentro de la tabla
            nombre = tabla.find_element(By.CSS_SELECTOR, "td[colindex='1'] div").text
            fase = tabla.find_element(By.CSS_SELECTOR, "td[colindex='3'] div").text if tabla.find_elements(By.CSS_SELECTOR, "td[colindex='3'] div") else "N/A"
            fecha_contable = tabla.find_element(By.CSS_SELECTOR, "td[colindex='4'] div").text if tabla.find_elements(By.CSS_SELECTOR, "td[colindex='4'] div") else "N/A"
            fecha_gen = tabla.find_element(By.CSS_SELECTOR, "td[colindex='8'] div").text if tabla.find_elements(By.CSS_SELECTOR, "td[colindex='8'] div") else "N/A"
            procesado = tabla.find_element(By.CSS_SELECTOR, "td[colindex='9'] div").text if tabla.find_elements(By.CSS_SELECTOR, "td[colindex='9'] div") else "N/A"
        except NoSuchElementException:
            # Manejar el caso en que la tabla no exista
            print(f"Tabla con ID '{tabla_id}' no encontrada.")
            nombre, fase, fecha_contable, fecha_gen, procesado = "N/A", "N/A", "N/A", "N/A", "N/A"

        # Agregar los valores a la lista de registros
        registros.append({
            "Tabla": tabla_id,
            "Nombre": nombre,
            "Fase": fase,
            "Fecha Contable": fecha_contable,
            "Fecha Generación": fecha_gen,
            "Procesado (S/N)": procesado,
            "Estado": "",  # Estado vacío por ahora
        })

    # Convertir registros a un DataFrame de Pandas
    df = pd.DataFrame(registros)

    # Imprimir el DataFrame como una tabla
    print(df.to_string(index=False))

    return df

# ---------------------------------------------------

def informes_recientes_estado(driver):
    driver.switch_to.default_content()
    """
    Extrae los textos de los últimos diez registros en la lista con id 'listRecRpts'.
    
    """
    try:
        # Localizar la lista de registros recientes
        lista_elementos = driver.find_elements(By.CSS_SELECTOR, "#listRecRptsInner .listItem .listText")
        
        # Extraer los textos de los elementos
        textos_registros = [elemento.text for elemento in lista_elementos]
        
        # Tomar los últimos diez registros (o menos si no hay suficientes)
        ultimos_diez_registros = textos_registros[-10:]
        
        return ultimos_diez_registros
    
    except Exception as e:
        print(f"Error al obtener los últimos diez registros: {e}")
        return []