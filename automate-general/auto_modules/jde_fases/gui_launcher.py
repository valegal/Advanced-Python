import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import threading
from datetime import datetime

# Importa tu script principal y config
import main  # Asegúrate de que tu script se llame main.py o cambia el nombre aquí
import config

def ejecutar_script():
    # Actualiza los valores en config.py con lo ingresado
    config.fecha_con = fecha_entry.get().replace("-", "")
    config.fecha_con_lib = f"*{config.fecha_con}*"
    config.USER = user_entry.get()
    config.PASS = pass_entry.get()

    # Inicia el proceso principal en un hilo aparte para no congelar la GUI
    thread = threading.Thread(target=main.main)
    thread.start()

# Crear ventana principal
root = tk.Tk()
root.title("Lanzador Interfaz Facturación ESSA")
root.geometry("400x300")
root.resizable(False, False)

# Estilos
style = ttk.Style()
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10, "bold"))
style.configure("TEntry", font=("Segoe UI", 10))

# Usuario
ttk.Label(root, text="Usuario:").pack(pady=(20, 0))
user_entry = ttk.Entry(root, width=30)
user_entry.insert(0, config.USER)
user_entry.pack()

# Contraseña
ttk.Label(root, text="Contraseña:").pack(pady=(10, 0))
pass_entry = ttk.Entry(root, width=30, show="*")
pass_entry.insert(0, config.PASS)
pass_entry.pack()

# Fecha de contabilización
ttk.Label(root, text="Fecha de contabilización:").pack(pady=(10, 0))
fecha_entry = DateEntry(root, width=27, date_pattern="yyyy-mm-dd")
fecha_entry.set_date(datetime.strptime(config.fecha_con, "%Y%m%d"))
fecha_entry.pack()

# Botón para ejecutar
ttk.Button(root, text="Ejecutar Script", command=ejecutar_script).pack(pady=(20, 10))

# Iniciar GUI
root.mainloop()
