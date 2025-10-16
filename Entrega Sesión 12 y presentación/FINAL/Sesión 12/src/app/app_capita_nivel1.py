
import tkinter as tk
from tkinter import messagebox
import json
import os

# ---------- Estilos ----------
PRIMARY_BG = "#e6f0fa"
QUESTION_BG = "#ffffff"
PRIMARY_COLOR = "#1e88e5"
CORRECT_COLOR = "#2ecc71"
WRONG_COLOR = "#e74c3c"
TEXT_COLOR = "#1b1b1b"
FONT = ("Segoe UI", 12)
TITLE_FONT = ("Segoe UI", 16, "bold")

# ---------- Clase Pregunta ----------
class Pregunta:
    def __init__(self, enunciado, tipo, opciones, respuesta_correcta):
        self.enunciado = enunciado
        self.tipo = tipo
        self.opciones = opciones
        self.respuesta_correcta = respuesta_correcta

# ---------- Cargar preguntas ----------
def cargar_preguntas():
    ruta = "preguntas_nivel1.json"
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Pregunta(p["enunciado"], p["tipo"], p["opciones"], p["respuesta_correcta"]) for p in data]
    else:
        return []

# ---------- Guardar progreso ----------
def guardar_progreso(puntaje, total):
    progreso = {"nivel_1_finanzas": {"puntaje": puntaje, "total": total, "completado": True}}
    with open("progreso.json", "w", encoding="utf-8") as f:
        json.dump(progreso, f, indent=4, ensure_ascii=False)

# ---------- Ventana del Quiz ----------
def open_win_quiz(root):
    preguntas = cargar_preguntas()
    if not preguntas:
        messagebox.showerror("Error", "No se encontraron preguntas.")
        return

    ventana = tk.Toplevel(root)
    ventana.title("Nivel 1 - Finanzas Personales")
    ventana.geometry("620x520")
    ventana.configure(bg=PRIMARY_BG)

    indice_actual = [0]
    respuestas_correctas = [0]
    respuesta_usuario = [None]
    respuestas_multiples = []

    # Widgets
    tk.Label(ventana, text="💰 Nivel 1 - Finanzas Personales", font=TITLE_FONT,
             fg=PRIMARY_COLOR, bg=PRIMARY_BG).pack(pady=12)

    card = tk.Frame(ventana, bg=QUESTION_BG, padx=20, pady=20, relief="ridge", bd=2)
    card.pack(padx=30, pady=10, fill="both", expand=True)

    label_pregunta = tk.Label(card, text="", wraplength=500, font=FONT,
                               bg=QUESTION_BG, fg=TEXT_COLOR, justify="left")
    label_pregunta.pack(pady=10, anchor="w")

    opciones_frame = tk.Frame(card, bg=QUESTION_BG)
    opciones_frame.pack(anchor="w")

    feedback_label = tk.Label(card, text="", font=FONT, bg=QUESTION_BG)
    feedback_label.pack(pady=10)

    # Funciones
    def cargar_pregunta():
        for widget in opciones_frame.winfo_children():
            widget.destroy()
        feedback_label.config(text="")

        pregunta = preguntas[indice_actual[0]]
        label_pregunta.config(text=f"({indice_actual[0]+1}/{len(preguntas)}) {pregunta.enunciado}")
        respuesta_usuario[0] = None
        respuestas_multiples.clear()

        if pregunta.tipo == "opcion":
            var = tk.StringVar()
            for opcion in pregunta.opciones:
                b = tk.Radiobutton(opciones_frame, text=opcion, variable=var, value=opcion,
                                   font=FONT, anchor="w", fg=TEXT_COLOR, bg=QUESTION_BG,
                                   selectcolor="#dfefff", indicatoron=True,
                                   command=lambda op=opcion: seleccionar_respuesta(op))
                b.pack(fill="x", pady=4)
        elif pregunta.tipo == "multiple":
            for opcion in pregunta.opciones:
                var = tk.IntVar()
                chk = tk.Checkbutton(opciones_frame, text=opcion, variable=var,
                                     font=FONT, anchor="w", fg=TEXT_COLOR, bg=QUESTION_BG,
                                     selectcolor="#dfefff",
                                     command=lambda op=opcion, v=var: toggle_multiple(op, v))
                chk.pack(fill="x", pady=4)
        elif pregunta.tipo == "columnas":
            var = tk.StringVar()
            var.set("Selecciona una opción")
            menu = tk.OptionMenu(opciones_frame, var, *pregunta.opciones)
            var.trace_add("write", lambda *args: seleccionar_respuesta(var.get()))
            menu.pack(fill="x", pady=10)

    def seleccionar_respuesta(valor):
        respuesta_usuario[0] = valor

    def toggle_multiple(opcion, var):
        if var.get():
            if opcion not in respuestas_multiples:
                respuestas_multiples.append(opcion)
        else:
            if opcion in respuestas_multiples:
                respuestas_multiples.remove(opcion)

    def procesar_respuesta():
        pregunta = preguntas[indice_actual[0]]
        correcta = False

        if pregunta.tipo == "multiple":
            correcta = set(pregunta.respuesta_correcta) == set(respuestas_multiples)
        else:
            correcta = respuesta_usuario[0] == pregunta.respuesta_correcta

        if correcta:
            respuestas_correctas[0] += 1
            feedback_label.config(text="🟢 ¡Correcto!", fg=CORRECT_COLOR)
        else:
            feedback_label.config(text=f"🔴 Incorrecto. Correcta: {pregunta.respuesta_correcta}", fg=WRONG_COLOR)

    def siguiente():
        procesar_respuesta()
        if indice_actual[0] < len(preguntas) - 1:
            indice_actual[0] += 1
            ventana.after(1200, cargar_pregunta)
        else:
            ventana.after(1200, mostrar_resultado)

    def mostrar_resultado():
        for widget in ventana.winfo_children():
            widget.destroy()
        score = respuestas_correctas[0]
        total = len(preguntas)
        guardar_progreso(score, total)

        ventana.configure(bg=PRIMARY_BG)
        tk.Label(ventana, text="🎉 ¡Nivel completado!", font=TITLE_FONT,
                 bg=PRIMARY_BG, fg=PRIMARY_COLOR).pack(pady=20)
        tk.Label(ventana, text=f"Tu puntaje fue: {score}/{total}",
                 font=FONT, bg=PRIMARY_BG, fg=TEXT_COLOR).pack(pady=10)
        tk.Button(ventana, text="Volver al menú", command=ventana.destroy,
                  bg=PRIMARY_COLOR, fg="white", font=FONT).pack(pady=30)

    # Botón siguiente
    tk.Button(ventana, text="Siguiente", command=siguiente,
              bg=PRIMARY_COLOR, fg="white", font=FONT, padx=10, pady=5).pack(pady=20)

    cargar_pregunta()

# ---------- Menú Principal ----------
def main():
    root = tk.Tk()
    root.title("App Cápita - Finanzas Gamificadas")
    root.geometry("400x300")
    root.configure(bg=PRIMARY_BG)

    tk.Label(root, text="🌟 Bienvenido a Cápita", font=TITLE_FONT,
             fg=PRIMARY_COLOR, bg=PRIMARY_BG).pack(pady=30)

    tk.Button(root, text="Iniciar Nivel 1", command=lambda: open_win_quiz(root),
              bg=PRIMARY_COLOR, fg="white", font=FONT, padx=10, pady=5).pack(pady=10)

    tk.Button(root, text="Salir", command=root.quit,
              bg=WRONG_COLOR, fg="white", font=FONT, padx=10, pady=5).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
