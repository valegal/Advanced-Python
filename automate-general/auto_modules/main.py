from config import setup_driver
from login import login
from info import copy_info_tabla_carga
from navigation import navigate_to_carga_archivo, navigate_to_fecha_gen
from utils import take_screenshot
from utils import clasificar_tablas_por_procesado
from jde import procesar_pendientes, informes_recientes_estado

fecha = "20241226"
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
        print(registros_df)

        # Guardar las primeras 10 filas en el resumen
        summary_steps.append("- Primeras 10 filas extraídas de las tablas:")
        summary_steps.append(registros_df.head(10).to_string(index=False))

        # Clasificar tablas según el estado 'Procesado (S/N)'
        pendientes, descartadas = clasificar_tablas_por_procesado(registros_df)
        summary_steps.append(f"- Tablas pendientes (Procesado = 'N'): {pendientes}")
        summary_steps.append(f"- Tablas descartadas (Procesado = 'S'): {descartadas}")
        sidebar01 = informes_recientes_estado(driver)
        print(sidebar01)
        summary_steps.append(sidebar01)
        print(pendientes)
        procesar_pendientes(driver, pendientes)
        

# ---------------------------------------------------


        # Crear resumen de pasos
        summary_path = r"D:\OneDrive - Grupo EPM\Descargas\RESUMEN.txt"
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
