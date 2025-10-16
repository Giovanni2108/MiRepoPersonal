"""Shared components for quiz windows with consistent styling."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Callable, Iterable, List

import tkinter as tk

# ---------- Estilos comunes -----------
BASE_BG = "#fff6e5"
CARD_BG = "#fffbe6"
ACCENT_COLOR = "#ff9800"
TEXT_COLOR = "#5d4037"
DETAIL_COLOR = "#8d6e63"
CORRECT_COLOR = "#2e7d32"
WRONG_COLOR = "#c62828"
FONT = ("Segoe UI", 12)
TITLE_FONT = ("Segoe UI", 18, "bold")
BUTTON_FONT = ("Segoe UI", 12, "bold")
PROGRESS_FILE = "progreso.json"


@dataclass
class Pregunta:
    """Modelo base de pregunta para los distintos quizzes."""

    enunciado: str
    tipo: str  # opcion, multiple, columnas, enlazar
    opciones: List[Any]
    respuesta_correcta: Any


def load_preguntas_from_file(path: str, fallback: Iterable[Pregunta]) -> List[Pregunta]:
    """Carga preguntas desde JSON o devuelve un fallback predefinido."""

    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as fichero:
                data = json.load(fichero)
            return [
                Pregunta(
                    enunciado=item.get("enunciado", ""),
                    tipo=item.get("tipo", "opcion"),
                    opciones=item.get("opciones", []),
                    respuesta_correcta=item.get("respuesta_correcta"),
                )
                for item in data
            ]
        except (json.JSONDecodeError, OSError):
            return list(fallback)
    return list(fallback)


def save_progress(progress_key: str, puntaje: int, total: int) -> None:
    """Actualiza el archivo de progreso con el resultado del quiz."""

    data: dict[str, Any] = {}
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as fichero:
                data = json.load(fichero)
        except (json.JSONDecodeError, OSError):
            data = {}
    data[progress_key] = {"puntaje": puntaje, "total": total, "completado": True}
    with open(PROGRESS_FILE, "w", encoding="utf-8") as fichero:
        json.dump(data, fichero, ensure_ascii=False, indent=2)


class QuizPage:
    """Componente interactivo para mostrar un quiz dentro de un contenedor."""

    def __init__(
        self,
        container: tk.Misc,
        titulo: str,
        emoji: str,
        progress_key: str,
        preguntas: List[Pregunta],
        on_exit: Callable[[], None],
    ) -> None:
        if not preguntas:
            raise ValueError("Se requiere al menos una pregunta para iniciar el quiz.")

        self.container = container
        self.titulo = titulo
        self.emoji = emoji
        self.progress_key = progress_key
        self.preguntas = preguntas
        self.on_exit = on_exit

        self.indice = 0
        self.correctas = 0
        self.respuesta_usuario: Any = None
        self.respuestas_multiples: List[str] = []
        self.respuestas_enlazadas: dict[str, str] = {}
        self._option_vars: List[tk.Variable] = []

        for child in self.container.winfo_children():
            child.destroy()

        outer = tk.Frame(self.container, bg=BASE_BG)
        outer.pack(fill="both", expand=True, padx=16, pady=16)

        self.header = tk.Label(
            outer,
            text=f"{self.emoji} {self.titulo}",
            font=TITLE_FONT,
            fg=ACCENT_COLOR,
            bg=BASE_BG,
        )
        self.header.pack(pady=(0, 12))

        self.card = tk.Frame(
            outer,
            bg=CARD_BG,
            padx=20,
            pady=20,
            highlightbackground="#ffcc80",
            highlightthickness=1,
        )
        self.card.pack(fill="both", expand=True)

        self.label_pregunta = tk.Label(
            self.card,
            text="",
            wraplength=340,
            font=FONT,
            bg=CARD_BG,
            fg=TEXT_COLOR,
            justify="left",
        )
        self.label_pregunta.pack(anchor="w", pady=(0, 12))

        self.opciones_frame = tk.Frame(self.card, bg=CARD_BG)
        self.opciones_frame.pack(anchor="w", fill="x")

        self.feedback_label = tk.Label(
            self.card,
            text="",
            font=FONT,
            bg=CARD_BG,
            fg=DETAIL_COLOR,
        )
        self.feedback_label.pack(anchor="w", pady=(16, 0))

        self.next_button = tk.Button(
            outer,
            text="Siguiente",
            command=self._siguiente,
            bg=ACCENT_COLOR,
            fg="white",
            activebackground="#fb8c00",
            activeforeground="white",
            font=BUTTON_FONT,
            padx=14,
            pady=8,
            bd=0,
            highlightthickness=0,
            cursor="hand2",
        )
        self.next_button.pack(pady=(12, 0))

        self._cargar_pregunta()

    # ---------- Construcción de opciones ----------
    def _limpiar_opciones(self) -> None:
        for widget in self.opciones_frame.winfo_children():
            widget.destroy()
        self._option_vars.clear()

    def _cargar_pregunta(self) -> None:
        self._limpiar_opciones()
        self.feedback_label.config(text="", fg=DETAIL_COLOR)

        pregunta = self.preguntas[self.indice]
        total = len(self.preguntas)
        self.label_pregunta.config(text=f"({self.indice + 1}/{total}) {pregunta.enunciado}")

        boton_texto = "Finalizar" if self.indice == total - 1 else "Siguiente"
        self.next_button.config(state="normal", text=boton_texto)

        self.respuesta_usuario = None
        self.respuestas_multiples.clear()
        self.respuestas_enlazadas.clear()

        if pregunta.tipo == "opcion":
            var = tk.StringVar(value="")
            self._option_vars.append(var)
            for opcion in pregunta.opciones:
                boton = tk.Radiobutton(
                    self.opciones_frame,
                    text=opcion,
                    variable=var,
                    value=opcion,
                    font=FONT,
                    anchor="w",
                    fg=TEXT_COLOR,
                    bg=CARD_BG,
                    selectcolor="#ffe0b2",
                    command=lambda value=opcion: self._seleccionar_respuesta(value),
                )
                boton.pack(fill="x", pady=4)
        elif pregunta.tipo == "multiple":
            for opcion in pregunta.opciones:
                var = tk.IntVar(value=0)
                self._option_vars.append(var)
                chk = tk.Checkbutton(
                    self.opciones_frame,
                    text=opcion,
                    variable=var,
                    font=FONT,
                    anchor="w",
                    fg=TEXT_COLOR,
                    bg=CARD_BG,
                    selectcolor="#ffe0b2",
                    command=lambda value=opcion, variable=var: self._toggle_multiple(value, variable),
                )
                chk.pack(fill="x", pady=4)
        elif pregunta.tipo == "columnas":
            var = tk.StringVar(value="Selecciona una opción")
            self._option_vars.append(var)
            menu = tk.OptionMenu(self.opciones_frame, var, *pregunta.opciones)
            menu.configure(bg=CARD_BG, fg=TEXT_COLOR, font=FONT, highlightthickness=0)
            menu.pack(fill="x", pady=8)
            menu["menu"].configure(bg="#fffaf0", fg=TEXT_COLOR, activebackground="#ffe0b2")
            var.trace_add("write", lambda *_: self._seleccionar_respuesta(var.get()))
        elif pregunta.tipo == "enlazar":
            for izquierda, _ in pregunta.opciones:
                etiqueta = tk.Label(
                    self.opciones_frame,
                    text=izquierda,
                    font=FONT,
                    bg=CARD_BG,
                    fg=TEXT_COLOR,
                )
                etiqueta.pack(anchor="w", pady=(4, 0))
                var = tk.StringVar(value="Selecciona")
                self._option_vars.append(var)
                menu = tk.OptionMenu(
                    self.opciones_frame,
                    var,
                    *[derecha for _, derecha in pregunta.opciones],
                )
                menu.configure(bg=CARD_BG, fg=TEXT_COLOR, font=FONT, highlightthickness=0)
                menu.pack(fill="x", pady=4)
                menu["menu"].configure(bg="#fffaf0", fg=TEXT_COLOR, activebackground="#ffe0b2")
                var.trace_add(
                    "write",
                    lambda *_ , key=izquierda, variable=var: self.respuestas_enlazadas.update({key: variable.get()}),
                )

    def _seleccionar_respuesta(self, valor: Any) -> None:
        self.respuesta_usuario = valor

    def _toggle_multiple(self, opcion: str, variable: tk.IntVar) -> None:
        if variable.get():
            if opcion not in self.respuestas_multiples:
                self.respuestas_multiples.append(opcion)
        elif opcion in self.respuestas_multiples:
            self.respuestas_multiples.remove(opcion)

    # ---------- Flujo ----------
    def _procesar_respuesta(self) -> None:
        pregunta = self.preguntas[self.indice]
        correcta = False

        if pregunta.tipo == "multiple":
            correcta = set(pregunta.respuesta_correcta) == set(self.respuestas_multiples)
        elif pregunta.tipo == "enlazar":
            correcta = all(
                (izquierda, derecha) in pregunta.respuesta_correcta
                for izquierda, derecha in self.respuestas_enlazadas.items()
            ) and len(self.respuestas_enlazadas) == len(pregunta.respuesta_correcta)
        else:
            correcta = self.respuesta_usuario == pregunta.respuesta_correcta

        if correcta:
            self.correctas += 1
            self.feedback_label.config(text="🟢 ¡Correcto!", fg=CORRECT_COLOR)
        else:
            respuesta_texto = pregunta.respuesta_correcta
            if isinstance(respuesta_texto, (list, tuple)):
                respuesta_texto = ", ".join(map(str, respuesta_texto))
            self.feedback_label.config(
                text=f"🔴 Incorrecto. Respuesta correcta: {respuesta_texto}",
                fg=WRONG_COLOR,
            )

    def _siguiente(self) -> None:
        self._procesar_respuesta()
        if self.indice < len(self.preguntas) - 1:
            self.indice += 1
            self.next_button.config(state="disabled")
            self.container.after(900, self._cargar_pregunta)
        else:
            self.next_button.config(state="disabled")
            self.container.after(900, self._mostrar_resultado)

    def _mostrar_resultado(self) -> None:
        for widget in self.container.winfo_children():
            widget.destroy()

        score = self.correctas
        total = len(self.preguntas)
        save_progress(self.progress_key, score, total)

        outer = tk.Frame(self.container, bg=BASE_BG)
        outer.pack(fill="both", expand=True, padx=16, pady=16)

        tk.Label(
            outer,
            text="🎉 ¡Nivel completado!",
            font=TITLE_FONT,
            bg=BASE_BG,
            fg=ACCENT_COLOR,
        ).pack(pady=(40, 12))
        tk.Label(
            outer,
            text=f"Tu puntaje fue: {score}/{total}",
            font=FONT,
            bg=BASE_BG,
            fg=TEXT_COLOR,
        ).pack(pady=(0, 24))

        tk.Button(
            outer,
            text="Volver",
            command=self.on_exit,
            bg=ACCENT_COLOR,
            fg="white",
            activebackground="#fb8c00",
            activeforeground="white",
            font=BUTTON_FONT,
            padx=16,
            pady=8,
            bd=0,
            highlightthickness=0,
            cursor="hand2",
        ).pack()


def render_quiz_page(
    container: tk.Misc,
    titulo: str,
    emoji: str,
    progress_key: str,
    preguntas: List[Pregunta],
    on_exit: Callable[[], None],
) -> None:
    QuizPage(container, titulo, emoji, progress_key, preguntas, on_exit)


__all__ = [
    "Pregunta",
    "load_preguntas_from_file",
    "save_progress",
    "render_quiz_page",
]
