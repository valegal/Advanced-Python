from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import logging

# Configuración general
CHROMEDRIVER_PATH = r"C:\Users\vgaleanc\Escritorio\chromedriver\chromedriver-win64\chromedriver.exe"
WEBSITE_URL_JDE = "https://epm-vws20c.corp.epm.com.co/jde/E1Menu.maf"
fecha_gen = "20250328"
fecha_con = "20250326"
fecha_con_lib = f"*{fecha_con}*"
EXCEL_PATH = r"D:\OneDrive - Grupo EPM\Documentos\InterfazFacturacion\07.  FFN014-V1-Formato Registro BATCH-MARZO.xlsx"

def setup_driver():
    """Configura y retorna el driver de Selenium."""
    
    # Ignorar errores SSL
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors=yes')  # Esto también ayuda a ignorar los errores SSL

    # Redirigir los logs de Chrome para evitar mostrar mensajes de SSL en consola
    options.add_argument('--disable-logging')
    # options.add_argument('--log-level=3')  # Esto suprime los mensajes de log

    # Crear el driver de Selenium con la configuración de opciones
    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    # Ajustar ventana del navegador
    # driver.set_window_position(0, -1080)
    driver.maximize_window()
    
    return driver
