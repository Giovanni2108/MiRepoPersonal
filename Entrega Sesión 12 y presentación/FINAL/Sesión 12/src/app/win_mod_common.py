"""Helpers to render module selector pages with a consistent style."""

from typing import Callable, Optional
import tkinter as tk
from tkinter import ttk

BASE_BG = "#fff6e5"
CARD_BG = "#fffbe6"
PRIMARY_COLOR = "#ff9800"
TEXT_COLOR = "#5d4037"
NOTE_COLOR = "#8d6e63"
DISABLED_BG = "#ffe0b2"
DISABLED_TEXT = "#bfae9f"


def _ensure_styles(master: tk.Misc) -> ttk.Style:
    style = ttk.Style(master)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure("Module.Card.TFrame", background=CARD_BG)
    style.configure(
        "Module.Header.TLabel",
        background=CARD_BG,
        foreground=PRIMARY_COLOR,
        font=("Segoe UI", 18, "bold"),
    )
    style.configure(
        "Module.Subtitle.TLabel",
        background=CARD_BG,
        foreground=TEXT_COLOR,
        font=("Segoe UI", 12),
    )
    style.configure(
        "Module.Detail.TLabel",
        background=CARD_BG,
        foreground=NOTE_COLOR,
        font=("Segoe UI", 10),
    )
    style.configure(
        "Module.Button.TButton",
        background=PRIMARY_COLOR,
        foreground="#ffffff",
        font=("Segoe UI", 12, "bold"),
        padding=(12, 10),
        borderwidth=0,
        relief="flat",
    )
    style.map(
        "Module.Button.TButton",
        background=[("active", "#fb8c00"), ("pressed", "#f57c00")],
        foreground=[("active", "#ffffff")],
    )
    style.configure(
        "Module.Disabled.TButton",
        background=DISABLED_BG,
        foreground=DISABLED_TEXT,
        font=("Segoe UI", 12),
        padding=(12, 10),
        borderwidth=0,
        relief="flat",
    )
    style.map(
        "Module.Disabled.TButton",
        background=[("disabled", DISABLED_BG)],
        foreground=[("disabled", DISABLED_TEXT)],
    )
    style.configure(
        "Module.Back.TButton",
        background="#fff3e0",
        foreground=PRIMARY_COLOR,
        font=("Segoe UI", 11, "bold"),
        padding=(10, 8),
        borderwidth=0,
        relief="flat",
    )
    style.map(
        "Module.Back.TButton",
        background=[("active", "#ffe0b2"), ("pressed", "#ffe0b2")],
        foreground=[("active", PRIMARY_COLOR)],
    )
    style.configure("Module.Separator.TSeparator", background="#ffe0b2")
    return style


def render_module_page(
    parent: tk.Misc,
    header_text: str,
    intro_text: Optional[str] = None,
) -> ttk.Frame:
    for child in parent.winfo_children():
        child.destroy()

    _ensure_styles(parent)

    outer = tk.Frame(parent, bg=BASE_BG)
    outer.pack(fill="both", expand=True, padx=12, pady=12)

    card = ttk.Frame(outer, style="Module.Card.TFrame", padding=(24, 24, 24, 16))
    card.pack(fill="both", expand=True)
    card.columnconfigure(0, weight=1)

    header = ttk.Label(card, text=header_text, style="Module.Header.TLabel")
    header.pack(anchor="w")

    if intro_text:
        ttk.Label(
            card,
            text=intro_text,
            style="Module.Subtitle.TLabel",
            wraplength=320,
            justify="left",
        ).pack(anchor="w", pady=(8, 18))

    return card


def add_module_button(
    parent: ttk.Frame,
    text: str,
    command: Optional[Callable[[], None]] = None,
    enabled: bool = True,
) -> ttk.Button:
    style_name = "Module.Button.TButton" if enabled and command else "Module.Disabled.TButton"
    button = ttk.Button(parent, text=text, style=style_name)
    button.pack(fill="x", pady=6)
    if enabled and command:
        button.configure(command=command, cursor="hand2")
    else:
        button.state(["disabled"])
    return button


def add_note_label(parent: ttk.Frame, text: str) -> ttk.Label:
    note = ttk.Label(
        parent,
        text=text,
        style="Module.Detail.TLabel",
        wraplength=320,
        justify="left",
    )
    note.pack(anchor="w", pady=(16, 0))
    return note


def add_back_button(parent: ttk.Frame, command: Callable[[], None], text: str = "Volver") -> ttk.Button:
    ttk.Separator(parent, orient="horizontal", style="Module.Separator.TSeparator").pack(
        fill="x", pady=(18, 14)
    )
    button = ttk.Button(parent, text=text, style="Module.Back.TButton", command=command)
    button.pack(pady=(0, 4))
    button.configure(cursor="hand2")
    return button


__all__ = [
    "render_module_page",
    "add_module_button",
    "add_note_label",
    "add_back_button",
]
