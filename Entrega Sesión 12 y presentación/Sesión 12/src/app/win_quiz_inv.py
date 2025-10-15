from win_quiz_common import (
    Pregunta,
    load_preguntas_from_file,
    render_quiz_page,
)


FALLBACK_PREGUNTAS = [
    Pregunta(
        "¿Qué es una inversión?",
        "opcion",
        ["Comprar activos para obtener ganancias", "Gastar en ocio", "Ahorrar bajo el colchón"],
        "Comprar activos para obtener ganancias",
    ),
    Pregunta(
        "Selecciona instrumentos de inversión",
        "multiple",
        ["Acciones", "Bonos", "Ropa", "Fondos de inversión"],
        ["Acciones", "Bonos", "Fondos de inversión"],
    ),
    Pregunta(
        "¿Cuál es un riesgo de invertir?",
        "opcion",
        ["Pérdida de valor", "Garantía de ganancia", "No hay riesgo"],
        "Pérdida de valor",
    ),
    Pregunta(
        "Relaciona: Diversificación -",
        "columnas",
        ["Reducir riesgo", "Aumentar riesgo", "Invertir en un solo activo"],
        "Reducir riesgo",
    ),
    Pregunta(
        "¿Qué representa una inversión inteligente?",
        "opcion",
        ["Invertir en pirámides", "Diversificar en fondos indexados", "Gastar todo en ocio"],
        "Diversificar en fondos indexados",
    ),
    Pregunta(
        "Selecciona ventajas de invertir",
        "multiple",
        ["Generar rendimientos", "Perder dinero", "Aumentar patrimonio", "No hacer nada"],
        ["Generar rendimientos", "Aumentar patrimonio"],
    ),
    Pregunta(
        "Relaciona los conceptos con su definición:",
        "enlazar",
        [("Acción", "Parte de una empresa"), ("Bono", "Deuda emitida"), ("Diversificación", "Reducir riesgo")],
        [("Acción", "Parte de una empresa"), ("Bono", "Deuda emitida"), ("Diversificación", "Reducir riesgo")],
    ),
]


def cargar_preguntas_inv() -> list[Pregunta]:
    return load_preguntas_from_file("preguntas_nivel1_inversiones.json", FALLBACK_PREGUNTAS)


def open_win_quiz_inv(container, on_exit) -> None:
    preguntas = cargar_preguntas_inv()
    render_quiz_page(container, "Nivel 1 - Inversiones", "📈", "nivel_1_inversiones", preguntas, on_exit)