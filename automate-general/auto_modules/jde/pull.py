import os
import re
import pdfplumber

# Carpeta con los archivos PDF
carpeta_pdf = r"D:\OneDrive - Grupo EPM\Descargas\reportes"
archivo_salida = r"D:\OneDrive - Grupo EPM\Descargas\resultados.txt"

# Expresiones regulares para extraer datos
regex_agrupacion = re.compile(r'EMONTANC\s+\d+\s+\.\d+\s+\d+\s+\d+\s+[A-Z]\s+(\d+)')  # Agrupación
regex_carga = re.compile(r'\d{7}\s+(\d{5})\s+\d{4}/\d{2}/\d{2}')  # Carga
regex_fecha_contable = re.compile(r'(\d{4}/\d{2}/\d{2})')  # Fecha contable
regex_debitos = re.compile(r'DEBITOS GENERAL\s+([\d,]+\.\d{2})')  # Débitos
regex_creditos = re.compile(r'CREDITOS GENERAL\s+([\d,]+\.\d{2})-?')  # Créditos

def extraer_datos(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Leer primera y última página
            primera_pagina = pdf.pages[0].extract_text()
            ultima_pagina = pdf.pages[-1].extract_text()

            if not primera_pagina or not ultima_pagina:
                print(f"Advertencia: No se pudo extraer texto en {pdf_path}")
                return None

            # Buscar Agrupación, Carga y Fecha Contable en la primera página
            agrupacion = regex_agrupacion.search(primera_pagina)
            carga = regex_carga.search(primera_pagina)
            fecha_contable = regex_fecha_contable.search(primera_pagina)

            agrupacion = agrupacion.group(1) if agrupacion else "N/A"
            carga = carga.group(1) if carga else "N/A"
            fecha_contable = fecha_contable.group(1) if fecha_contable else "N/A"

            # Buscar Débitos y Créditos en la última página
            match_debitos = regex_debitos.search(ultima_pagina)
            match_creditos = regex_creditos.search(ultima_pagina)

            if not match_debitos or not match_creditos:
                print(f"Advertencia: No se encontraron los valores en {pdf_path}")
                return None

            debitos = match_debitos.group(1).replace(",", "")
            creditos = match_creditos.group(1).replace(",", "")

            return {
                "archivo": os.path.basename(pdf_path),
                "agrupacion": agrupacion,
                "carga": carga,
                "fecha_contable": fecha_contable,
                "debitos": debitos,
                "creditos": creditos
            }

    except Exception as e:
        print(f"Error al procesar {pdf_path}: {e}")
        return None

# Procesar todos los archivos y escribir resultados en el TXT
with open(archivo_salida, "w", encoding="utf-8") as salida:
    salida.write("Archivo | Agrupación | Carga | Fecha Contable | Débitos | Créditos\n")
    salida.write("-" * 100 + "\n")

    for archivo in os.listdir(carpeta_pdf):
        if archivo.lower().endswith(".pdf"):
            ruta_pdf = os.path.join(carpeta_pdf, archivo)
            datos = extraer_datos(ruta_pdf)

            if datos:
                salida.write(f"{datos['archivo']} | {datos['agrupacion']} | {datos['carga']} | {datos['fecha_contable']} | {datos['debitos']} | {datos['creditos']}\n")

print(f"✅ Proceso completado. Resultados guardados en: {archivo_salida}")
