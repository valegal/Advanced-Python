

def verificar_carga_en_sidebar(lista):
    """
    Verifica si alguno de los últimos cinco elementos de la lista contiene la palabra 'Carga'.
    Retorna True si la encuentra, False en caso contrario.
    """
    ultimos_cinco = lista[-5:]  # Obtener los últimos 5 elementos
    for item in ultimos_cinco:
        if 'Carga' in item:
            print("Encontrado un valor con 'Carga':", item)
            return True
    print("Ninguno de los últimos cinco valores contiene 'Carga'.")
    return False
