from win_mod_common import (
    add_back_button,
    add_module_button,
    add_note_label,
    render_module_page,
)


def open_mod_finanzas(container, on_back, start_quiz):
    card = render_module_page(
        container,
        "Finanzas personales",
        "Selecciona un módulo para continuar tu aprendizaje.",
    )

    add_module_button(card, "Módulo 1: Fundamentos", command=start_quiz)
    for idx in range(2, 6):
        add_module_button(card, f"Módulo {idx}", enabled=False)

    add_note_label(card, "Los módulos restantes estarán disponibles próximamente.")
    add_back_button(card, on_back)