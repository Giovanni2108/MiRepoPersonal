from win_mod_common import (
    add_back_button,
    add_module_button,
    add_note_label,
    render_module_page,
)


def open_mod_imp(container, on_back, start_quiz):
    card = render_module_page(
        container,
        "Impuestos",
        "Selecciona un módulo para reforzar tus conocimientos fiscales.",
    )

    add_module_button(card, "Módulo 1: Introducción", command=start_quiz)
    for idx in range(2, 6):
        add_module_button(card, f"Módulo {idx}", enabled=False)

    add_note_label(card, "Estamos preparando más módulos con casos prácticos.")
    add_back_button(card, on_back)
