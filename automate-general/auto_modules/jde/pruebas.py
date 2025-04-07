import fitz  # pymupdf
import re

# Ruta del PDF
pdf_path = "D:/OneDrive - Grupo EPM/Descargas/R5609FCT/sample.pdf"

# Expresión regular para fase con contexto
regex_nfase = re.compile(r'\d{4}/\d{2}/\d{2}\s+\d{4}/\d{2}/\d{2}\s+(\d)')

with fitz.open(pdf_path) as doc:
    primera_pagina = doc[0]  # Solo leer la primera página
    texto = primera_pagina.get_text("text")  # Extraer texto

    # Intentar buscar con regex en el texto extraído
    match = regex_nfase.search(texto)
    
    if match:
        fase = match.group(1)
        print(f"Fase encontrada: {fase}")
    else:
        print("⚠ No se encontró la fase de carga.")

    # Alternativa: Extraer texto en un área específica
    rect = fitz.Rect(100, 50, 200, 100)  # Ajusta estos valores según el PDF
    texto_area = primera_pagina.get_text("text", clip=rect)
    print(f"Texto en el área específica: {texto_area}")
