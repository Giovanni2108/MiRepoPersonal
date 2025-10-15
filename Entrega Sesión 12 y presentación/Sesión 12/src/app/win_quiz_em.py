from win_quiz_common import (
    Pregunta,
    load_preguntas_from_file,
    render_quiz_page,
)


FALLBACK_PREGUNTAS = [
    Pregunta(
        "¿Qué es el emprendimiento?",
        "opcion",
        ["Crear un negocio propio", "Buscar empleo", "Ahorrar dinero"],
        "Crear un negocio propio",
    ),
    Pregunta(
        "Selecciona características de un emprendedor",
        "multiple",
        ["Creatividad", "Pasividad", "Resiliencia", "Miedo al cambio"],
        ["Creatividad", "Resiliencia"],
    ),
    Pregunta(
        "¿Cuál es un riesgo de emprender?",
        "opcion",
        ["Fracaso", "Éxito garantizado", "No hay riesgo"],
        "Fracaso",
    ),
    Pregunta(
        "Relaciona: Innovación -",
        "columnas",
        ["Crear algo nuevo", "Copiar ideas", "Evitar cambios"],
        "Crear algo nuevo",
    ),
    Pregunta(
        "¿Qué representa una oportunidad de negocio?",
        "opcion",
        ["Detectar una necesidad", "Ignorar el mercado", "Evitar clientes"],
        "Detectar una necesidad",
    ),
    Pregunta(
        "Selecciona ventajas de emprender",
        "multiple",
        ["Independencia", "Estancamiento", "Potencial de crecimiento", "Evitar aprendizaje"],
        ["Independencia", "Potencial de crecimiento"],
    ),
    Pregunta(
        "Relaciona los conceptos con su definición:",
        "enlazar",
        [("Emprendedor", "Persona que inicia un negocio"), ("Innovación", "Crear algo nuevo"), ("Riesgo", "Posibilidad de pérdida")],
        [("Emprendedor", "Persona que inicia un negocio"), ("Innovación", "Crear algo nuevo"), ("Riesgo", "Posibilidad de pérdida")],
    ),
]


def cargar_preguntas_empr() -> list[Pregunta]:
    return load_preguntas_from_file("preguntas_nivel1_empr.json", FALLBACK_PREGUNTAS)


def open_win_quiz_empr(container, on_exit) -> None:
    preguntas = cargar_preguntas_empr()
    render_quiz_page(container, "Nivel 1 - Emprendimiento", "💼", "nivel_1_emprendimiento", preguntas, on_exit)
