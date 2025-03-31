
import time
import os
import shutil
import re
import pdfplumber
import openpyxl
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from config import fecha_con

# Expresiones regulares mejoradas
regex_agrupacion = re.compile(r'EMONTANC.*?\s(\d{5})')
regex_carga = re.compile(r'(\d{5})\s+\d{4}/\d{2}/\d{2}')
regex_fecha_contable = re.compile(r'(\d{4}/\d{2}/\d{2})\s+.*Asientos Interface Facturacion')
regex_debitos = re.compile(r'DEBITOS GENERAL\s+([\d,]+\.\d{2})')
regex_creditos = re.compile(r'CREDITOS GENERAL\s+([\d,]+\.\d{2})-?')

# Carpeta con los archivos PDF
carpeta_pdf = r"D:\OneDrive - Grupo EPM\Descargas\R5609FCT"
carpeta_pdf2 = r"D:\OneDrive - Grupo EPM\Descargas\ReportesDinamicaContable"

#-----------------------------------------------------------------------------

def review_pdfs(driver, reportes, res_carga):
    """
    Esta función automatiza la revisión de los Reportes para Generar Dinámica Contable, seleccionando los archivos para que se genere el pdf.
    """

    # Hacer clic en el icono de la tabla
    icono = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='listRRpt_WSJ']/table/tbody/tr/td[1]"))
    )
    icono.click()
    time.sleep(5)

    # Cambiar al iframe
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "e1menuAppIframe")))
    driver.switch_to.frame(driver.find_element(By.ID, "e1menuAppIframe"))

    for i in range(reportes - 1, -1, -1):  
        # Esperar a que el elemento esté presente y visible
        tarea_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//*[@id='G0_1_R{i}']/td[1]/div/input"))
        )

        # Crear una instancia de ActionChains y hacer doble clic en el elemento
        action = ActionChains(driver)
        action.double_click(tarea_element).perform()

        print(f"Doble clic realizado en el elemento {i}")
        time.sleep(3)

    # Mover los archivos descargados
    mover_reportes()
    contrastar_debitos_y_creditos(carpeta_pdf, res_carga)
    time.sleep(5)
    eliminar_reportes()


#-----------------------------------------------------------------------------

def mover_reportes():
    """
    Esta función automatiza el proceso de mover todos los archivos PDF cuyo nombre inicie por 'R5609FCT_'
    de la carpeta Descargas a la carpeta Descargas/R5609FCT.
    """
    # Definir rutas
    carpeta_origen = r"D:\OneDrive - Grupo EPM\Descargas"
    carpeta_destino = os.path.join(carpeta_origen, "R5609FCT")
    carpeta_destino2 = os.path.join(carpeta_origen, "ReportesDinamicaContable")

    # Asegurar que las carpetas de destino existen
    for carpeta in [carpeta_destino, carpeta_destino2]:
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

    # Buscar archivos que cumplan con el patrón
    for archivo in os.listdir(carpeta_origen):
        if archivo.startswith("R5609FCT_") and archivo.endswith(".pdf"):
            ruta_origen = os.path.join(carpeta_origen, archivo)

            # Mover el archivo a la primera carpeta
            ruta_destino = os.path.join(carpeta_destino, archivo)
            shutil.move(ruta_origen, ruta_destino)
            print(f"Movido a reportes: {archivo}")
            ruta_destino2 = os.path.join(carpeta_destino2, archivo)
            shutil.copy(ruta_destino, ruta_destino2)


    print("Proceso completado.")

#-----------------------------------------------------------------------------

def contrastar_debitos_y_creditos(carpeta_pdf, res_carga):
    """
    Revisa todos los PDFs en la carpeta y extrae información clave.
    """
    resultados = []

    for archivo in os.listdir(carpeta_pdf):
        if archivo.endswith(".pdf"):
            pdf_path = os.path.join(carpeta_pdf, archivo)
            with pdfplumber.open(pdf_path) as pdf:
                primera_pagina = pdf.pages[0].extract_text()
                ultima_pagina = pdf.pages[-1].extract_text()

                if not primera_pagina or not ultima_pagina:
                    print(f"⚠ No se pudo extraer texto de {archivo}")
                    continue

                # Extraer información clave
                agrupacion = regex_agrupacion.search(primera_pagina)
                carga = regex_carga.search(primera_pagina)
                fecha_contable = regex_fecha_contable.search(primera_pagina)
                match_debitos = regex_debitos.search(ultima_pagina)
                match_creditos = regex_creditos.search(ultima_pagina)

                if not match_debitos or not match_creditos:
                    print(f"⚠ No se encontraron valores en {archivo}")
                    continue

                # Convertir los valores correctamente
                debitos = float(match_debitos.group(1).replace(",", ""))
                creditos = float(match_creditos.group(1).replace(",", ""))

                # Verificar igualdad
                if debitos == abs(creditos):
                    print(f"✅ Débitos y créditos coinciden en {archivo}")
                else:
                    print(f"⚠ Descuadre en {archivo}: Débitos {debitos} vs Créditos {creditos}")

                resultados.append({
                    "archivo": archivo,
                    "agrupacion": agrupacion.group(1) if agrupacion else "N/A",
                    "carga": carga.group(1) if carga else "N/A",
                    "fecha_contable": fecha_contable.group(1) if fecha_contable else "N/A",
                    "debitos": debitos,
                    "creditos": creditos
                })

    # Actualizar Excel
    update_excel_batch_agrupacion(resultados, res_carga)


#-----------------------------------------------------------------------------

def update_excel_batch_agrupacion(resultados, res_carga):
    # Ruta del archivo Excel
    excel_path = r"D:\OneDrive - Grupo EPM\Documentos\InterfazFacturacion\07.  FFN014-V1-Formato Registro BATCH-MARZO.xlsx"
    
    # Cargar el archivo Excel
    wb = openpyxl.load_workbook(excel_path)
    
    # Diccionario para mapear claves de res_carga a nombres de hojas
    hojas_map = {
        1: "1-FACTURACIÓN",
        2: "2-AUTOCONSUMOS",
        3: "3-AJUSTES",
        4: "4-RECAUDOS",
        5: "5-CASTIGO"
    }
    
    for resultado in resultados:
        agrupacion = resultado["agrupacion"]
        fecha = resultado["fecha_contable"]  # Formato esperado: YYYY/MM/DD
        
        if agrupacion == "N/A" or fecha == "N/A":
            print(f"⚠ Datos insuficientes para actualizar Excel en {resultado['archivo']}")
            continue
        
        # Extraer el día de la fecha (ej. "2025/03/16" → 16)
        try:
            dia = int(fecha.split("/")[2])
            celda_destino = f"C{7 + dia}"  # Ajusta la fila según el día del mes
        except ValueError:
            print(f"⚠ Fecha inválida en {resultado['archivo']}: {fecha}")
            continue
        
        # Determinar la hoja correcta usando res_carga
        for clave, lote in res_carga.items():
            if clave in hojas_map:
                hoja_nombre = hojas_map[clave]
                
                try:
                    hoja = wb[hoja_nombre]
                    hoja[celda_destino] = agrupacion  # Escribir el valor en la celda
                    print(f"✅ Actualizado {hoja_nombre} en {celda_destino} con {agrupacion}")
                except KeyError:
                    print(f"⚠ No se encontró la hoja {hoja_nombre} en el archivo Excel.")
    
    # Guardar cambios
    wb.save(excel_path)
    wb.close()
    print("✅ Archivo Excel actualizado correctamente.")


#-----------------------------------------------------------------------------

def eliminar_reportes():
    """
    Elimina los archivos PDF de la carpeta 'R5609FCT' después del proceso.
    """
    carpeta_destino = r"D:\OneDrive - Grupo EPM\Descargas\R5609FCT"

    if os.path.exists(carpeta_destino):
        for archivo in os.listdir(carpeta_destino):
            ruta_archivo = os.path.join(carpeta_destino, archivo)
            if os.path.isfile(ruta_archivo):
                os.remove(ruta_archivo)
                print(f"🗑 Eliminado: {archivo}")
        print("✅ Todos los archivos han sido eliminados.")
    else:
        print(f"⚠ La carpeta {carpeta_destino} no existe.")
