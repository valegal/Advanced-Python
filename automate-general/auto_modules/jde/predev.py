from config import setup_driver
from login import login
from info import copy_info_tabla_carga, informes_recientes_estado
from navigation import navigate_to_carga_archivo,  navigate_to_revision_hechos, navigate_control_archivos_cargados, navigate_home
from utils import take_screenshot
from utils import clasificar_tablas_por_procesado
from config import fecha
from input import input_estado_registro, input_fecha_contable
from jde.verify import verify_estado_trabajo, verify_control_archivos
from button import clic_boton_envio, clic_boton_lupa
from actions import action_cargar_fases
from search import search_estado_registro
import time

def main():
    driver = setup_driver()
    try:

        # Realizar el login
        login(driver, "EMONTANC", "edmcESSA06**")

        # ================= PASO 1 CARGA ARCHIVO IF =================
        
        # Verificación del estado del trabajo para las 5 cargas
        verify_estado_trabajo(driver)

        # ================= PASO 2 VERIFICAR ERRORES 'REVISIÓN HECHOS ECONÓMICOS' =================
        
        # ================= PASO 3 CONTROL DE LOS ARCHIVOS QUE SE ACABAN DE SUBIR =================

        # ================= PASO 4 AGRUPACIÓN DE HECHOS ECONOMICOS =================

        # ================= PASO 5 GENERAR MOVIMIENTO CONTABLE IF =================

        # ================= PASO 6 REVISIONES AD BATCH =================

        # ================= PASO 7 REVISION DEL COMPROBANTE =================

        # ================= PASO 9 =================

        # ================= PASO 11 =================

# ---------------------------------------------------
    
    except Exception as e:
        error_message = f"Error durante la ejecución: {e}"
        print(error_message)
        take_screenshot(driver, "error_state.png")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
