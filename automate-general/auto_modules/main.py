from config import setup_driver
from login import login
from info import copy_info_tabla_carga, informes_recientes_estado
from navigation import navigate_to_carga_archivo, navigate_to_fecha_gen, navigate_to_review_hechos_econo, navigate_home, navigate_control_archivos_cargados
from utils import take_screenshot
from utils import clasificar_tablas_por_procesado
from jde import procesar_pendientes
from verify import verificar_carga_en_sidebar
from config import fecha
from write import write_run_estado_registro
import time

summary_steps = []

def main():
    driver = setup_driver()
    try:
        summary_steps.append("INICIO del proceso Interfaz de Facturación")

        # Realizar el login
        login(driver, "EMONTANC", "edmcESSA02**")
        summary_steps.append("→ Login exitoso con usuario EMONTANC.")
        
        # Navegar a la vista de carga de archivo
        navigate_to_carga_archivo(driver)
        summary_steps.append("→ Navegación a la vista de Carga de Archivo IF-C ")

        # Escribir una fecha en el campo Fecha Generación
        navigate_to_fecha_gen(driver, fecha)
        summary_steps.append(f"→ Fecha Generación establecida a {fecha}")
        
        # Extraer primeras 10 filas tabla Registros en Carga Archivo
        registros_df = copy_info_tabla_carga(driver)
        summary_steps.append("→ Datos extraídos de tablas en Carga Archivo.")

        # Guardar las primeras 10 filas en el resumen
        summary_steps.append("→ Primeras 10 filas extraídas de las tablas:")
        summary_steps.append(registros_df.head(10).to_string(index=False))

        # Clasificar tablas según el estado 'Procesado (S/N)'
        pendientes, procesadas = clasificar_tablas_por_procesado(registros_df)
        summary_steps.append("→ Clasificar Registros procesados o no en OneWorld")
        summary_steps.append(f"Tablas pendientes (Procesado = 'N'): {pendientes}")
        summary_steps.append(f"Tablas descartadas (Procesado = 'S'): {procesadas}")
        print(f"➡️ Hay {len(pendientes)} registros pendientes y {len(procesadas)} registros procesados")
        summary_steps.append(f"➡️ Hay {len(pendientes)} registros pendientes y {len(procesadas)} registros procesados")

        # Sidebar inicial
        sidebar01 = informes_recientes_estado(driver)
        summary_steps.append("➤ Sidebar inicial:")
        summary_steps.append("\n".join(map(str, sidebar01)) if isinstance(sidebar01, list) else str(sidebar01))
        print(str(sidebar01))
 
        # Ejecutar Cargar Archivos IF (jde file)
        procesar_pendientes(driver, pendientes, summary_steps)
        time.sleep(60)

        #Imprimir y añadir a registro tabla de reguistros depués de Ejecutar carga
        registros_df = copy_info_tabla_carga(driver)
        summary_steps.append("➡️ Tabla de registros Carga Archivo IF-C después de las cargas:")
        summary_steps.append(registros_df.head(10).to_string(index=False))
        df = registros_df

        time.sleep(8)

        # Sidebar despues de las cargas
        sidebar02 = informes_recientes_estado(driver)
        summary_steps.append("➤ Sidebar después de las cargas:")
        summary_steps.append("\n".join(map(str, sidebar02)) if isinstance(sidebar02, list) else str(sidebar01))
        print(sidebar02)
        
        #Verificar la palabra carga en 'informes recientes'
        verificar_carga_en_sidebar(sidebar02)
        time.sleep(180)
        if sidebar02 == True:
            print("Ya hay carga")
            summary_steps.append("→ Palabra 'Carga' existente en Informes recientes")
        else:
            print("No hay carga")
        summary_steps.append("→ Palabra 'Carga' NO existente en Informes recientes")

        navigate_home(driver)
        
        # Navegar a la vista Revisión de hechos económicos
        navigate_to_review_hechos_econo(driver)
        summary_steps.append("→ Navegación a la vista de Revisión Hechos Económicos IF.")

        # Escribir 8 en Estado de Registro
        write_run_estado_registro(driver, summary_steps)
        summary_steps.append(f"→ Escribir 8 en Estado de Registro")

        # Volver al inicio
        navigate_home(driver)
        summary_steps.append("→ Volver al inicio")
        
        # Navegar a la vista Control Archivos Cargados
        navigate_control_archivos_cargados(driver)
        summary_steps.append("→ Navegación a la vista de Control Archivos Cargados.")

# ---------------------------------------------------

        # Crear resumen de pasos
        summary_path = r"D:\OneDrive - Grupo EPM\Descargas\Resumen001.txt"
        with open(summary_path, "w", encoding="utf-8") as file:
            file.write("\n".join(summary_steps))
        summary_steps.append(f"Resumen de pasos guardado en '{summary_path}'.")
    
    except Exception as e:
        error_message = f"Error durante la ejecución: {e}"
        print(error_message)
        summary_steps.append(error_message)
        take_screenshot(driver, "error_state.png")
        summary_steps.append("Captura de pantalla del estado de error guardada como 'error_state.png'.")
    finally:
        # Registrar cierre del navegador
        summary_steps.append("Cierre del navegador.")
        # Guardar resumen final
        summary_path = r"D:\OneDrive - Grupo EPM\Descargas\RESUMEN.txt"
        with open(summary_path, "w", encoding="utf-8") as file:
            file.write("\n".join(summary_steps))
        input("Presiona Enter para cerrar la ventana...")
        driver.quit()

if __name__ == "__main__":
    main()
