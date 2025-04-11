from datetime import datetime, timedelta
from pathlib import Path

#========= Configuración general ==========

# Rutas
CHROMEDRIVER_PATH = Path.home() / "Escritorio" / "chromedriver" / "chromedriver-win64" / "chromedriver.exe"
WEBSITE_URL_JDE = "https://epm-vws20c.corp.epm.com.co/jde/E1Menu.maf"
EXCEL_PATH = Path.home() / "OneDrive - Grupo EPM" / "Documentos" / "InterfazFacturacion" / "07.  FFN014-V1-Formato Registro BATCH-ABRIL.xlsx"
RUTA_RES_CARGA = Path.home() / "OneDrive - Grupo EPM" / "Descargas" / "res_carga.txt"

# Credenciales
USER = "EMONTANC"
PASS = "edmcESSA08**"

# Carpeta con los archivos PDF
FOLDER_R5609FCT = Path.home() / "OneDrive - Grupo EPM" / "Descargas" / "R5609FCT"
FOLDER_DINAMICAS = Path.home() / "OneDrive - Grupo EPM" / "Descargas" / "ReportesDinamicaContable"
FOLDER_ORIGEN = Path.home() / "OneDrive - Grupo EPM" / "Descargas" 

#========= Variables de fecha automáticas ==========

# Día anterior al día actual
yesterday = datetime.now() - timedelta(days=1)

# Formato requerido por los sistemas (yyyymmdd)
fecha_con = yesterday.strftime("%Y%m%d")
fecha_con_lib = f"*{fecha_con}*"
fecha_gen = datetime.now().strftime("%Y%m%d")  # Fecha de generación actual


#-------------------------------------------------------------------------------------------------------

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
