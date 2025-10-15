import tkinter as tk
from tkinter import ttk, messagebox
import csv
from pathlib import Path

def open_win_table(parent: tk.Tk):
    for widget in parent.winfo_children():
        widget.destroy()
    frm = ttk.Frame(parent, padding=24, style="TFrame")
    frm.pack(fill="both", expand=True)

    cols = ("nombre", "valor1", "valor2")
    tv = ttk.Treeview(frm, columns=cols, show="headings", height=10, style="TButton")
    for c in cols:
        tv.heading(c, text=c.capitalize())
        tv.column(c, width=120, anchor="center")
    tv.pack(fill="both", expand=True)

    ruta = Path(__file__).resolve().parents[1] / "data" / "sample.csv"  # <repo>/data/sample.csv
    if not ruta.exists():
        messagebox.showwarning("Aviso", f"No se encontró {ruta}. Crea el archivo de ejemplo.")
        return

    with open(ruta, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tv.insert("", "end", values=(row["nombre"], row["valor1"], row["valor2"]))