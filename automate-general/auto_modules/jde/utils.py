import time

def take_screenshot(driver, filename="screenshot.png"):
    """Toma una captura de pantalla del estado actual."""
    driver.save_screenshot(filename)
    print(f"Captura de pantalla guardada como {filename}")

def wait_and_print(message, seconds=2):
    """Imprime un mensaje y espera un tiempo especificado."""
    print(message)
    time.sleep(seconds)

def clasificar_tablas_por_procesado(dataframe):
    """
    Clasifica las tablas según el valor de la columna 'Procesado (S/N)'.

    Args:
        dataframe (pd.DataFrame): DataFrame con los datos extraídos de las tablas.

    Returns:
        list, list: Dos listas, una con los IDs de tablas que tienen 'N' en 'Procesado (S/N)'
                    y otra con los IDs de tablas que tienen 'S'.
    """
    # Inicializar las listas para tablas pendientes y procesadas
    pendientes = []
    procesadas = []

    # Recorrer el DataFrame fila por fila
    for _, row in dataframe.iterrows():
        if row["Procesado (S/N)"] == "N":
            pendientes.append(row["Tabla"])
        elif row["Procesado (S/N)"] == "S":
            procesadas.append(row["Tabla"])

    return pendientes, procesadas
