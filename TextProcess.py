import tkinter as tk
from tkinter import scrolledtext
import pyperclip

def eliminar_saltos(texto_con_saltos):
    texto_sin_saltos = texto_con_saltos.replace('\n', ' ')
    return texto_sin_saltos

def procesar_texto():
    texto_entrada = entrada_texto.get("1.0", tk.END)
    texto_procesado = eliminar_saltos(texto_entrada)
    mostrar_resultado(texto_procesado)

def copiar_al_portapapeles(texto):
    pyperclip.copy(texto)
    tk.messagebox.showinfo("Copiado", "Texto copiado al portapapeles")

def mostrar_resultado(texto_procesado):
    ventana_resultado = tk.Toplevel(ventana_principal)
    ventana_resultado.title("Texto Procesado")

    etiqueta_resultado = tk.Label(ventana_resultado, text="Texto sin saltos de línea:")
    etiqueta_resultado.pack(pady=10)

    texto_resultado = scrolledtext.ScrolledText(ventana_resultado, wrap=tk.WORD, width=40, height=10)
    texto_resultado.insert(tk.END, texto_procesado)
    texto_resultado.pack(padx=10, pady=10)

    # Botón para copiar al portapapeles
    boton_copiar = tk.Button(ventana_resultado, text="Copiar al Portapapeles", command=lambda: copiar_al_portapapeles(texto_procesado))
    boton_copiar.pack(pady=10)

# Crear la ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Eliminador de Saltos de Línea")

# Crear un widget de entrada de texto con desplazamiento
entrada_texto = scrolledtext.ScrolledText(ventana_principal, wrap=tk.WORD, width=40, height=10)
entrada_texto.pack(padx=10, pady=10)

# Botón para procesar el texto
boton_procesar = tk.Button(ventana_principal, text="Procesar Texto", command=procesar_texto)
boton_procesar.pack(pady=10)

# Iniciar el bucle principal de la interfaz gráfica
ventana_principal.mainloop()
