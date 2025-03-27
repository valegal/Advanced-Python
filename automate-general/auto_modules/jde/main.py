from config import setup_driver
from login import login
from info import copy_info_tabla_carga, informes_recientes_estado
from navigation import navigate_to_carga_archivo,  navigate_to_revision_hechos, navigate_control_archivos_cargados, navigate_home, navigate_agrupacion_hechos, navigate_generar_mov_contable
from utils import take_screenshot
from utils import clasificar_tablas_por_procesado
from config import fecha_con, fecha_gen
from input import input_estado_registro, input_fecha_contable
from verify import verify_estado_trabajo, verify_control_archivos
from button import clic_boton_envio, clic_boton_lupa
from actions import action_cargar_fases, agrupar, generar_movimiento_contable
from search import search_estado_registro
from goto import goto_verificar
import time

def main():
    driver = setup_driver()
   # try:

    # Realizar el login
    login(driver, "EMONTANC", "edmcESSA07**")

    goto_verificar(driver)


    driver.quit()

    # ================= PASO 1 CARGA ARCHIVO IF =================
    # Navegar a la vista
    #navigate_to_carga_archivo(driver)

    # Cargar las 5 fases
    # action_cargar_fases(driver, fecha_con)

    # Volver al inicio
    #navigate_home(driver)

    # Verificación del estado del trabajo para las 5 cargas
    # verify_estado_trabajo(driver)

    # ================= PASO 2 VERIFICAR ERRORES 'REVISIÓN HECHOS ECONÓMICOS' =================

    # time.sleep(10)
    # navigate_to_revision_hechos(driver)
    # time.sleep(10)
    # search_estado_registro(driver)
    # time.sleep(10)

    # ================= PASO 3 CONTROL DE LOS ARCHIVOS QUE SE ACABAN DE SUBIR =================

    # navigate_control_archivos_cargados(driver)
    # time.sleep(3)

    # # Verificar control de archivos y obtener los datos
    # resultado = verify_control_archivos(driver)

    # # Procesar datos para batchcarga
    # values = list(resultado.values())
    # batchcarga = {values[i + 1]: values[i] for i in range(0, len(values), 2)}
    # numbatchcarga = len(batchcarga)

    # # Guardar resultados en archivo de texto
    # ruta_archivo = "D:/OneDrive - Grupo EPM/Descargas/resultado_main.txt"
    # with open(ruta_archivo, "w") as file:
    #     for key, value in batchcarga.items():
    #         file.write(f"{key} = {value}\n")
    
    # print(f"📁 Archivo guardado en: {ruta_archivo}")

    # navigate_home(driver)
    # time.sleep(3)

    # ================= PASO 4 AGRUPACIÓN DE HECHOS ECONOMICOS =================

    # for _ in range(numbatchcarga):
    #     navigate_agrupacion_hechos(driver)
    #     time.sleep(3)
    #     agrupar(driver, list(batchcarga.values())[_])
    #     navigate_home(driver)
    #     time.sleep(5)

    # # ================= PASO 5 GENERAR MOVIMIENTO CONTABLE IF =================

    # for _ in range(numbatchcarga):
    #     navigate_generar_mov_contable(driver)
    #     time.sleep(3)
    #     generar_movimiento_contable(driver, list(batchcarga.values())[_])
    #     navigate_home(driver)
    #     time.sleep(3)

    # ================= PASO 6 REVISIONES AD BATCH =================




#     # ================= PASO 7 REVISION DEL COMPROBANTE =================

#     # ================= PASO 9 =================

#     # ================= PASO 11 =================



# ---------------------------------------------------
    
    # except Exception as e:
    #     error_message = f"Error durante la ejecución: {e}"
    #     print(error_message)
    #     take_screenshot(driver, "error_state.png")

    # finally:
    #     driver.quit()

if __name__ == "__main__":
    main()
