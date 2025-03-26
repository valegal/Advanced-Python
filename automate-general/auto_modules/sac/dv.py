if __name__ == "__main__":
    root = tk.Tk()
    root.title("    SAC Process")
    root.geometry("500x350")
    root.configure(bg="white")
    root.resizable(False, False)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coord = (screen_width - 500) // 2
    y_coord = (screen_height - 350) // 2
    root.geometry(f"500x350+{x_coord}+{y_coord}")

    try:
        root.iconbitmap("logo.ico")
    except:
        print("No se encontró el archivo logo.ico")

    style = ttk.Style()
    style.configure("TLabel", font=("Arial", 14, "bold"), background="white", foreground="#01085A")
    style.configure("TButton", font=("Arial", 12), padding=6, background="#264796", foreground="#01085A")
    style.configure("TEntry", font=("Arial", 12))

    label_fecha = ttk.Label(root, text="Seleccione la fecha:")
    label_fecha.pack(pady=(40, 5))

    label_desc = ttk.Label(root, text="Primero escriba la fecha del día que desea generar las 5 fases para ejecutar el proceso de Interfaz de facturación en SAC:",
                            font=("Arial", 9), wraplength=450, justify="center")
    label_desc.pack(pady=(0, 10))

    fecha_selector = DateEntry(root, width=18, background="#01085A", foreground="white",
                               borderwidth=3, date_pattern="dd/mm/yyyy", font=("Arial", 12))
    fecha_selector.pack(pady=10)

    btn_ejecutar = ttk.Button(root, text="Ejecutar")
    btn_ejecutar.pack(pady=20)

    def open_config_window():
        config_window = Toplevel(root)
        config_window.title("Configurar Fases")
        config_window.geometry("500x350")
        config_window.configure(bg="white")
        config_window.resizable(False, False)

        x_coord = (screen_width - 500) // 2
        y_coord = (screen_height - 350) // 2
        config_window.geometry(f"500x350+{x_coord}+{y_coord}")

        ttk.Label(config_window, text="Seleccione la fecha:").pack(pady=(40, 5))

        date_entry = ttk.Combobox(config_window, font=("Arial", 12), width=18)
        date_entry.pack(pady=5)
        date_entry.insert(0, "26/03/2025")

        ttk.Label(config_window, text="Para generar fases individuales ingrese la fecha y seleccione el botón correspondiente.",
                  font=("Arial", 9), wraplength=450, justify="center").pack(pady=5)

        button_frame = tk.Frame(config_window, bg="white")
        button_frame.pack(pady=10)

        fases = ["Fase 1", "Fase 2", "Fase 3", "Fase 4", "Fase 5"]
        for i, fase in enumerate(fases):
            btn = ttk.Button(button_frame, text=fase)
            btn.grid(row=i//3, column=i%3, padx=10, pady=10)

    config_button = ttk.Button(root, text="⚙", command=open_config_window)
    config_button.pack(pady=5)

    root.mainloop()