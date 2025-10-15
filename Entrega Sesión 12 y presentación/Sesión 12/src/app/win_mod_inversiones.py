from win_mod_common import (
    add_back_button,
    add_module_button,
    add_note_label,
    render_module_page,
)


def open_mod_inversiones(container, on_back, start_quiz):
    card = render_module_page(
        container,
        "Inversiones",
        "Selecciona un módulo para profundizar en tus estrategias de inversión.",
    )

    add_module_button(card, "Módulo 1: Introducción", command=start_quiz)
    for idx in range(2, 6):
        add_module_button(card, f"Módulo {idx}", enabled=False)

    add_note_label(card, "Pronto añadiremos nuevos módulos con estrategias y ejercicios.")
    add_back_button(card, on_back)
