from config import setup_driver
from login import login, logout, recargar_pagina
import ctypes
from info import copy_info_tabla_carga, informes_recientes_estado
from navigation import navigate_to_carga_archivo,  navigate_to_revision_hechos, navigate_control_archivos_cargados, navigate_home, navigate_agrupacion_hechos, navigate_generar_mov_contable, navigate_AD, navigate_pasa_comprobante_F0911Z1, navigate_revision_comprobante
from utils import take_screenshot
from utils import clasificar_tablas_por_procesado
from config import fecha_con, fecha_gen, fecha_con_lib, USER, PASS
from input import input_estado_registro, input_fecha_contable
from verify import verify_control_archivos
from button import clic_boton_envio, clic_boton_lupa
from actions import action_cargar_fases, agrupar, generar_movimiento_contable, contabilizar
from search import search_estado_registro
from goto import esperar_tareas_completas, actualizar_informes_recientes
from review import review_pdfs, mover_reportes
from pull import paso_al_f0911
from batch_revisiones import buscar_revisiones_AD
import time

def main():
    
    prevent_screen_lock()
    driver = setup_driver()

    # Realizar el login
    login(driver, USER, PASS)

    # ================= PASO 1 CARGA ARCHIVO IF =================

    # navigate_to_carga_archivo(driver)

    # action_cargar_fases(driver, fecha_con_lib)

    # actualizar_informes_recientes(driver)
    # time.sleep(3)

    # esperar_tareas_completas(driver, 5)

    # recargar_pagina(driver)

    # ================= PASO 2 VERIFICAR ERRORES 'REVISIÓN HECHOS ECONÓMICOS' =================

    # navigate_home(driver)
    # time.sleep(3)
    # navigate_to_revision_hechos(driver)
    # time.sleep(3)
    # search_estado_registro(driver)
    # navigate_home(driver)
    # recargar_pagina(driver)
    # time.sleep(3)

    # # ================= PASO 3 CONTROL DE LOS ARCHIVOS QUE SE ACABAN DE SUBIR =================

    # navigate_control_archivos_cargados(driver)
    # time.sleep(3)
    # # Verificar control de archivos y obtener los datos
    # res_carga = verify_control_archivos(driver)

    # # Procesar datos para batchcarga
    # values = list(res_carga.values())
    # batchcarga = {values[i + 1]: values[i] for i in range(0, len(values), 2)}
    # numbatchcarga = len(batchcarga)

    # # Guardar res_carga en archivo de texto
    # ruta_archivo = "D:/OneDrive - Grupo EPM/Descargas/res_carga.txt"
    # with open(ruta_archivo, "w") as file:
    #     for key, value in batchcarga.items():
    #         file.write(f"{key} = {value}\n")
    
    # print(f"📁 Archivo guardado en: {ruta_archivo}")

    # navigate_home(driver)
    # time.sleep(3)
    # recargar_pagina(driver)

    # # ================= PASO 4 AGRUPACIÓN DE HECHOS ECONOMICOS =================

    # for _ in range(numbatchcarga):
    #     navigate_agrupacion_hechos(driver)
    #     time.sleep(3)
    #     agrupar(driver, list(batchcarga.values())[_])
    #     recargar_pagina(driver)
    #     time.sleep(5)

    # actualizar_informes_recientes(driver)
    # time.sleep(3)


    # esperar_tareas_completas(driver, numbatchcarga)

    # recargar_pagina(driver)

    # # ================= PASO 5 GENERAR MOVIMIENTO CONTABLE IF =================

    # for _ in range(numbatchcarga):
    #     navigate_generar_mov_contable(driver)
    #     time.sleep(3)
    #     generar_movimiento_contable(driver, list(batchcarga.values())[_])
    #     recargar_pagina(driver)
    #     time.sleep(3)

    # actualizar_informes_recientes(driver)
    # time.sleep(3)


    # esperar_tareas_completas(driver, numbatchcarga)

    # recargar_pagina(driver)

    # # ================= PASO 6 REPORTES DINÁMICA CONTABLE =================

    # valores_columna_dos = review_pdfs(driver, numbatchcarga, batchcarga)
    # print(valores_columna_dos)

    # # # Ordenar por la clave
    # valores_columna_dos = dict(sorted(valores_columna_dos.items(), key=lambda x: int(x[0])))
    # print(valores_columna_dos)

    # navigate_home(driver)


    # recargar_pagina(driver)
    # time.sleep(1)


    # # ================= PASO 7 REVISIONES DE AD (BATCH) =================

    # navigate_AD(driver)
    # time.sleep(5)
    # buscar_revisiones_AD(driver, valores_columna_dos)

    # navigate_home(driver)

    # recargar_pagina(driver)


    # # ================= PASO 9 PASA COMPROBANTE DE F0911Z1 A F0911 =================

    # navigate_pasa_comprobante_F0911Z1(driver)
    # time.sleep(5)

    # # Obtener el mayor valor para campo_from y el menor valor para campo_to
    # campo_to_val = max(valores_columna_dos.values(), key=int)
    # campo_from_val = min(valores_columna_dos.values(), key=int)

    # paso_al_f0911(driver, campo_from_val, campo_to_val)
    # time.sleep(3)
    # recargar_pagina(driver)
    # time.sleep(3)
    # actualizar_informes_recientes(driver)
    # time.sleep(3)
    # esperar_tareas_completas(driver, 1)


    # ================= PASO 11 REVISIÓN DEL COMPROBANTE =================

    time.sleep(7)
    navigate_revision_comprobante(driver)

    contabilizar(driver)

    navigate_home(driver)
    time.sleep(3)

    logout(driver)
    

    # =============== ADD ===============

    restore_screen_lock()
    driver.quit()


# ---------------------------------------------------
    

def prevent_screen_lock():
    # Llamar a la función para evitar que el sistema entre en modo de suspensión
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)

def restore_screen_lock():
    # Restaurar el comportamiento normal del sistema
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)


if __name__ == "__main__":
    main()
