from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import logging

# Configuración general
CHROMEDRIVER_PATH = r"C:\Users\vgaleanc\Escritorio\chromedriver\chromedriver-win64\chromedriver.exe"
WEBSITE_URL_JDE = "https://epm-vws20c.corp.epm.com.co/jde/E1Menu.maf"
fecha_gen = "20250318"
fecha_con = "*20250311*"
fecha_con_lib = "20250310"
RUTA_ARCHIVO_BREAK = r"D:\OneDrive - Grupo EPM\Documentos\fallos"

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
