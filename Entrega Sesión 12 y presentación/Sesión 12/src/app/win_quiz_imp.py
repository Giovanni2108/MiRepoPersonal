from win_quiz_common import (
    Pregunta,
    load_preguntas_from_file,
    render_quiz_page,
)


FALLBACK_PREGUNTAS = [
    Pregunta(
        "¿Qué es un impuesto?",
        "opcion",
        ["Pago obligatorio al Estado", "Donación voluntaria", "Compra de bienes"],
        "Pago obligatorio al Estado",
    ),
    Pregunta(
        "Selecciona tipos de impuestos",
        "multiple",
        ["IVA", "ISR", "Renta", "Regalo"],
        ["IVA", "ISR"],
    ),
    Pregunta(
        "¿Cuál es el objetivo de los impuestos?",
        "opcion",
        ["Financiar servicios públicos", "Enriquecer a particulares", "Evitar el ahorro"],
        "Financiar servicios públicos",
    ),
    Pregunta(
        "Relaciona: IVA -",
        "columnas",
        ["Impuesto al valor agregado", "Impuesto sobre renta", "Impuesto a la propiedad"],
        "Impuesto al valor agregado",
    ),
    Pregunta(
        "¿Qué representa el ISR?",
        "opcion",
        ["Impuesto sobre la renta", "Impuesto sobre regalos", "Impuesto sobre ventas"],
        "Impuesto sobre la renta",
    ),
    Pregunta(
        "Selecciona obligaciones fiscales",
        "multiple",
        ["Declarar ingresos", "Evitar pagos", "Pagar impuestos", "Ignorar leyes"],
        ["Declarar ingresos", "Pagar impuestos"],
    ),
    Pregunta(
        "Relaciona los conceptos con su definición:",
        "enlazar",
        [("IVA", "Impuesto al valor agregado"), ("ISR", "Impuesto sobre la renta"), ("Declaración", "Informe de ingresos")],
        [("IVA", "Impuesto al valor agregado"), ("ISR", "Impuesto sobre la renta"), ("Declaración", "Informe de ingresos")],
    ),
]


def cargar_preguntas_imp() -> list[Pregunta]:
    return load_preguntas_from_file("preguntas_nivel1_imp.json", FALLBACK_PREGUNTAS)


def open_win_quiz_imp(container, on_exit) -> None:
    preguntas = cargar_preguntas_imp()
    render_quiz_page(container, "Nivel 1 - Impuestos", "💸", "nivel_1_impuestos", preguntas, on_exit)
