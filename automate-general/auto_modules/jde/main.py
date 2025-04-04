from config import setup_driver
from login import login
import ctypes
from info import copy_info_tabla_carga, informes_recientes_estado
from navigation import navigate_to_carga_archivo,  navigate_to_revision_hechos, navigate_control_archivos_cargados, navigate_home, navigate_agrupacion_hechos, navigate_generar_mov_contable, navigate_AD
from utils import take_screenshot
from utils import clasificar_tablas_por_procesado
from config import fecha_con, fecha_gen, fecha_con_lib
from input import input_estado_registro, input_fecha_contable
from verify import verify_control_archivos
from button import clic_boton_envio, clic_boton_lupa
from actions import action_cargar_fases, agrupar, generar_movimiento_contable
from search import search_estado_registro
from goto import esperar_tareas_completas, actualizar_informes_recientes
from review import review_pdfs, mover_reportes
import time

def main():
    
    prevent_screen_lock()
    driver = setup_driver()

    # Realizar el login
    login(driver, "EMONTANC", "edmcESSA07**")

    # ================= PASO 1 CARGA ARCHIVO IF =================

    navigate_to_carga_archivo(driver)

    action_cargar_fases(driver, fecha_con_lib)

    actualizar_informes_recientes(driver)

    esperar_tareas_completas(driver, 5)

    # ================= PASO 2 VERIFICAR ERRORES 'REVISIÓN HECHOS ECONÓMICOS' =================

    navigate_home(driver)
    time.sleep(3)
    navigate_to_revision_hechos(driver)
    time.sleep(3)
    search_estado_registro(driver)
    navigate_home(driver)
    time.sleep(3)

    # ================= PASO 3 CONTROL DE LOS ARCHIVOS QUE SE ACABAN DE SUBIR =================

    navigate_control_archivos_cargados(driver)
    time.sleep(3)
    # Verificar control de archivos y obtener los datos
    res_carga = verify_control_archivos(driver)

    # Procesar datos para batchcarga
    values = list(res_carga.values())
    batchcarga = {values[i + 1]: values[i] for i in range(0, len(values), 2)}
    numbatchcarga = len(batchcarga)

    # Guardar res_carga en archivo de texto
    ruta_archivo = "D:/OneDrive - Grupo EPM/Descargas/res_carga.txt"
    with open(ruta_archivo, "w") as file:
        for key, value in batchcarga.items():
            file.write(f"{key} = {value}\n")
    
    print(f"📁 Archivo guardado en: {ruta_archivo}")

    navigate_home(driver)
    time.sleep(3)

    # ================= PASO 4 AGRUPACIÓN DE HECHOS ECONOMICOS =================

    for _ in range(numbatchcarga):
        navigate_agrupacion_hechos(driver)
        time.sleep(3)
        agrupar(driver, list(batchcarga.values())[_])
        navigate_home(driver)
        time.sleep(5)

    esperar_tareas_completas(driver, numbatchcarga)

    # # ================= PASO 5 GENERAR MOVIMIENTO CONTABLE IF =================

    for _ in range(numbatchcarga):
        navigate_generar_mov_contable(driver)
        time.sleep(3)
        generar_movimiento_contable(driver, list(batchcarga.values())[_])
        navigate_home(driver)
        time.sleep(3)

    esperar_tareas_completas(driver, numbatchcarga)

    # ================= PASO 6 REPORTES DINÁMICA CONTABLE =================

    review_pdfs(driver, numbatchcarga, res_carga)

    navigate_home(driver)
    time.sleep(5)

    # ================= PASO 7 REVISIONES DE AD (BATCH) =================

    navigate_AD(driver)
    time.sleep(5)

    print("Vamos muy bien!")


    # ================= PASO 9 PASA COMPROBANTE DE F0911Z1 A F0911 =================

    # ================= PASO 11 REVISIÓN DEL COMPROBANTE =================


    # =============== ADD ===============

    # esperar_tareas_completas(driver)



    # REALIZAR FUNCIÓN PARA QUE FINALICE PROCESOS ANTES DE TIEMPO POR INCONSISTENCIAS.
    restore_screen_lock()
    driver.quit()

    time.sleep(90000000000000)



# ---------------------------------------------------
    
    # except Exception as e:
    #     error_message = f"Error durante la ejecución: {e}"
    #     print(error_message)
    #     take_screenshot(driver, "error_state.png")

    # finally:
    #     driver.quit()

def prevent_screen_lock():
    # Llamar a la función para evitar que el sistema entre en modo de suspensión
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)

def restore_screen_lock():
    # Restaurar el comportamiento normal del sistema
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)


if __name__ == "__main__":
    main()
