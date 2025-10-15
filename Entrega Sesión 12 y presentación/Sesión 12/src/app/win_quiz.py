from win_quiz_common import (
    Pregunta,
    load_preguntas_from_file,
    render_quiz_page,
)


FALLBACK_PREGUNTAS = [
    Pregunta(
        "¿Es recomendable ahorrar el 10% de tus ingresos mensuales?",
        "opcion",
        ["Verdadero", "Falso"],
        "Verdadero",
    ),
    Pregunta(
        "Selecciona las buenas prácticas financieras",
        "multiple",
        ["Ahorrar", "Endeudarse", "Llevar presupuesto", "Evitar ingresos"],
        ["Ahorrar", "Llevar presupuesto"],
    ),
    Pregunta(
        "¿Cuál es un ingreso fijo?",
        "opcion",
        ["Salario mensual", "Venta ocasional", "Premio de lotería"],
        "Salario mensual",
    ),
    Pregunta(
        "Relaciona: Activo -",
        "columnas",
        ["Bien con valor económico", "Pasivo", "Ingreso"],
        "Bien con valor económico",
    ),
    Pregunta(
        "¿Qué representa una inversión inteligente?",
        "opcion",
        ["Comprar un auto nuevo", "Invertir en un fondo indexado", "Ir de vacaciones"],
        "Invertir en un fondo indexado",
    ),
    Pregunta(
        "Selecciona elementos de un buen presupuesto mensual",
        "multiple",
        ["Renta", "Comida", "Regalos impulsivos", "Ahorro"],
        ["Renta", "Comida", "Ahorro"],
    ),
    Pregunta(
        "Relaciona los conceptos con su definición:",
        "enlazar",
        [("Activo", "Bien con valor económico"), ("Pasivo", "Deuda"), ("Ingreso", "Entrada de dinero")],
        [("Activo", "Bien con valor económico"), ("Pasivo", "Deuda"), ("Ingreso", "Entrada de dinero")],
    ),
]


def cargar_preguntas() -> list[Pregunta]:
    return load_preguntas_from_file("preguntas_nivel1.json", FALLBACK_PREGUNTAS)


def open_win_quiz(container, on_exit) -> None:
    preguntas = cargar_preguntas()
    render_quiz_page(container, "Nivel 1 - Finanzas Personales", "💰", "nivel_1_finanzas", preguntas, on_exit)