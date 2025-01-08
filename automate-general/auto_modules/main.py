from config import setup_driver
from login import login
from info import copy_info_tabla_carga, informes_recientes_estado
from navigation import navigate_to_carga_archivo, navigate_to_fecha_gen
from utils import take_screenshot
from utils import clasificar_tablas_por_procesado
from jde import procesar_pendientes
from verify import verificar_carga_en_sidebar
import time

fecha = "20150914"
summary_steps = []

def main():
    driver = setup_driver()
    try:
        summary_steps.append("Inicio del proceso Interfaz de Facturación")

        # Realizar el login
        login(driver, "EMONTANC", "edmcESSA02**")
        summary_steps.append("- Login exitoso con usuario EMONTANC.")
        
        # Navegar a la vista de carga de archivo
        navigate_to_carga_archivo(driver)
        summary_steps.append("- Navegación a la vista de carga de archivo completada.")

        # Escribir una fecha en el campo Fecha Generación
        navigate_to_fecha_gen(driver, fecha)
        summary_steps.append("- Fecha Generación establecida a {fecha}")
        
        # Imprimir primeras 10 filas tabla Registros en Carga Archivo
        registros_df = copy_info_tabla_carga(driver)
        summary_steps.append("- Datos extraídos de tablas en Carga Archivo.")

        # Guardar las primeras 10 filas en el resumen
        summary_steps.append("- Primeras 10 filas extraídas de las tablas:")
        summary_steps.append(registros_df.head(10).to_string(index=False))

        # Clasificar tablas según el estado 'Procesado (S/N)'
        pendientes, procesadas = clasificar_tablas_por_procesado(registros_df)
        summary_steps.append(f"- Tablas pendientes (Procesado = 'N'): {pendientes}")
        summary_steps.append(f"- Tablas descartadas (Procesado = 'S'): {procesadas}")
        print(f"Hay {len(pendientes)} registros pendientes y {len(procesadas)} registros procesados")
        summary_steps.append(f"Hay {len(pendientes)} registros pendientes y {len(procesadas)} registros procesados")

        # Sidebar inicial
        sidebar01 = informes_recientes_estado(driver)
        summary_steps.append("Sidebar inicial:")
        summary_steps.append("\n".join(map(str, sidebar01)) if isinstance(sidebar01, list) else str(sidebar01))
        print(sidebar01)

        print(pendientes)
        procesar_pendientes(driver, pendientes)
        time.sleep(12)
        registros_df = copy_info_tabla_carga(driver)
        summary_steps.append("- Después de la carga:")
        summary_steps.append(registros_df.head(10).to_string(index=False))
        df = registros_df

        time.sleep(8)

        # Sidebar despues de las cargas
        sidebar02 = informes_recientes_estado(driver)
        summary_steps.append("Sidebar después de las cargas:")
        summary_steps.append("\n".join(map(str, sidebar02)) if isinstance(sidebar02, list) else str(sidebar01))
        print(sidebar02)

        verificar_carga_en_sidebar(sidebar02)
        print("Espera, cuenta: ")
        time.sleep(180)
        print("Fin de la espera")
        
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
