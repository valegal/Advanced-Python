from config import setup_driver
from login import login
from info import copy_info_tabla_carga, informes_recientes_estado
from navigation import navigate_to_carga_archivo, navigate_to_fecha_gen, navigate_to_review_hechos_econo, navigate_home, navigate_control_archivos_cargados, navigate_agrupacion_hechos, navigate_gen_movimiento,navigate_AD, navigate_revision_comprobante
from utils import take_screenshot
from utils import clasificar_tablas_por_procesado
from verify import verificar_carga_en_sidebar
from config import fecha
from input import input_estado_registro, input_fecha_contable
from button import clic_boton_envio, clic_boton_lupa
import time


def main():
    driver = setup_driver()
    try:

        # Realizar el login
        login(driver, "EMONTANC", "edmcESSA03**")
        # ================= PASO 1 CARGA ARCHIVO IF =================
        # Navegar a la vista de carga de archivo
        navigate_to_carga_archivo(driver)

        # Escribir una fecha en el campo Fecha Generación
        navigate_to_fecha_gen(driver, fecha)
        
        # Extraer primeras 10 filas tabla Registros en Carga Archivo
        registros_df = copy_info_tabla_carga(driver)


        # Clasificar tablas según el estado 'Procesado (S/N)'
        pendientes, procesadas = clasificar_tablas_por_procesado(registros_df)

        print(f"Hay {len(pendientes)} registros pendientes y {len(procesadas)} registros procesados")


        # Sidebar inicial
        sidebar01 = informes_recientes_estado(driver)
        print(str(sidebar01))
 
        # Ejecutar Cargar Archivos IF (jde file)
        time.sleep(5) #Debería tardar un poco más

        #Imprimir y añadir a registro tabla de reguistros depués de Ejecutar carga
        registros_df = copy_info_tabla_carga(driver)

        df = registros_df

        time.sleep(8)

        # Sidebar despues de las cargas
        sidebar02 = informes_recientes_estado(driver)

        
        # Volver al inicio
        navigate_home(driver)


        # ================= PASO 2 VERIFICAR ERRORES 'REVISIÓN HECHOS ECONÓMICOS' =================
        # Navegar a la vista Revisión de hechos económicos
        navigate_to_review_hechos_econo(driver)

        # Escribir 8 en Estado de Registro
        input_estado_registro(driver)

        #Se rompe el ciclo

        # Volver al inicio
        navigate_home(driver)

        # ================= PASO 3 VERIFICAR EL CONTROL DE LOS ARCHIVOS QUE SE ACABAN DE SUBIR =================
        # Navegar a la vista Control Archivos Cargados
        navigate_control_archivos_cargados(driver)
        input_fecha_contable(driver)
        clic_boton_lupa(driver)

        # abrir_formato_registro_excel(driver)

        navigate_home(driver) 


        # ================= PASO 4 AGRUPACIÓN DE HECHOS ECONOMICOS =================

        navigate_agrupacion_hechos(driver)
        clic_boton_envio(driver)

           # Volver al inicio
        navigate_home(driver)


        # ================= PASO 5 GENERAR MOVIMIENTO CONTABLE IF =================

        # Verificar que todo lo anterior esté correcto
        navigate_gen_movimiento(driver)
        # Volver al inicio
        navigate_home(driver)

        # ================= PASO 6 REVISIONES AD BATCH =================

        navigate_AD(driver)

        # Volver al inicio
        navigate_home(driver)



        # ================= PASO 7 REVISION DEL COMPROBANTE =================

        navigate_revision_comprobante(driver)
        # Volver al inicio
        navigate_home(driver)


        # ================= PASO 9 =================

        # Hacer una verificación generla y generar un reporte de la calidad del paso a paso

        # ================= PASO 11 =================

        # Que la fecha de archivo config se establezca en la interfaz de power apps
        # Hacer una speudo vista para colocar el usuario y contraseña una sola vez de forma segura
        #Qué problemas ha habido en el desarollo de la autoatización, retrasos inconenientes, perdidas y ... después cuales son las posibles soluciones

# ---------------------------------------------------
    
    except Exception as e:
        error_message = f"Error durante la ejecución: {e}"
        print(error_message)
        take_screenshot(driver, "error_state.png")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
