import tkinter as tk
from tkinter import ttk
from app.win_mod_finanzas import open_mod_finanzas
# Puedes agregar los otros módulos después:
# from app.win_mod_inversion import open_mod_inversion
# from app.win_mod_impuestos import open_mod_impuestos
# from app.win_mod_emprendimiento import open_mod_emprendimiento

def open_aprendizaje(root):
    ventana = tk.Toplevel(root)
    ventana.title("Aprendizaje - Selecciona un tema")
    ventana.geometry("400x300")

    frame = ttk.Frame(ventana, padding=20)
    frame.pack(expand=True)

    ttk.Label(frame, text="Selecciona un tema", font=("Segoe UI", 14, "bold")).pack(pady=(0, 20))

    ttk.Button(frame, text="📘 Finanzas Personales", command=lambda: open_mod_finanzas(ventana)).pack(fill="x", pady=5)
    ttk.Button(frame, text="📈 Inversiones", state="disabled").pack(fill="x", pady=5)
    ttk.Button(frame, text="💼 Emprendimiento", state="disabled").pack(fill="x", pady=5)
    ttk.Button(frame, text="💸 Impuestos", state="disabled").pack(fill="x", pady=5)

    ttk.Button(frame, text="Volver", command=ventana.destroy).pack(pady=(20, 0))