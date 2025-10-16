import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
from typing import Any
import requests
import webbrowser
import json
import os
import datetime
import threading
import importlib.util
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from finanzasApi import fetch_stock
from win_mod_finanzas import open_mod_finanzas
from win_mod_inversiones import open_mod_inversiones
from win_mod_imp import open_mod_imp
from win_mod_empre import open_mod_empre
from win_quiz import open_win_quiz
from win_quiz_inv import open_win_quiz_inv
from win_quiz_imp import open_win_quiz_imp
from win_quiz_em import open_win_quiz_empr

def main():
    root = tk.Tk()
    root.title("Proyecto Integrador - MVP")
    width = 420
    height = int(width * 16 / 9)  # Relación de aspecto 16:9 en vertical
    root.geometry(f"{width}x{height}")
    root.minsize(width, height)
    root.maxsize(width, height)
    root.resizable(False, False)
    root.configure(bg="#fff6e5")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#fff6e5")
    style.configure("Nav.TFrame", background="#ff9800")
    style.configure("Nav.TButton", background="#ff9800", foreground="#fff", font=("Segoe UI", 18, "bold"), borderwidth=0, relief="flat")
    style.map("Nav.TButton",
        background=[("active", "#fb8c00"), ("pressed", "#fb8c00")],
        foreground=[("active", "#fff"), ("pressed", "#fff")]
    )
    style.configure("Page.TFrame", background="#fffbe6", relief="flat", borderwidth=0)
    style.configure("Page.TLabel", background="#fffbe6", font=("Segoe UI", 20, "bold"), foreground="#fb8c00")
    style.configure("PageText.TLabel", background="#fffbe6", font=("Segoe UI", 13), foreground="#ff9800")
    # Estilo para Combobox acorde a la paleta
    try:
        style.configure(
            "Page.TCombobox",
            fieldbackground="#ffffff",
            background="#fffaf0",
            foreground="#5d4037",
            bordercolor="#ffcc80",
            lightcolor="#ffcc80",
            darkcolor="#ffcc80",
            arrowsize=14,
        )
        style.map(
            "Page.TCombobox",
            fieldbackground=[("readonly", "#ffffff"), ("focus", "#ffffff")],
            foreground=[("disabled", "#8d6e63")],
            arrowcolor=[("active", "#fb8c00"), ("!active", "#ff9800")],
            bordercolor=[("focus", "#ff9800"), ("!focus", "#ffcc80")],
        )
    except Exception:
        pass

    # Fondo degradado simulado
    bg_canvas = tk.Canvas(root, width=width-32, height=height-100, highlightthickness=0)
    for i in range(height-100):
        color = "#ffe0b2" if i < (height-100)//2 else "#fff6e5"
        bg_canvas.create_line(0, i, width-32, i, fill=color)
    bg_canvas.place(relx=0.5, rely=0.5, anchor="center")

    main_frame = ttk.Frame(root, padding=0, style="TFrame")
    main_frame.place(relx=0.5, rely=0.5, anchor="center", width=width-32, height=height-100)

    # Páginas
    page_foros = ttk.Frame(main_frame, style="Page.TFrame")
    page_progreso = ttk.Frame(main_frame, style="Page.TFrame")
    page_perfil = ttk.Frame(main_frame, style="Page.TFrame")
    page_noticias = ttk.Frame(main_frame, style="Page.TFrame")
    module_keys = ["finanzas", "inversiones", "impuestos", "emprende"]
    module_pages = {key: tk.Frame(main_frame, bg="#fffbe6") for key in module_keys}
    bar_pages = [module_pages[key] for key in module_keys]

    module_configs = {
        "finanzas": (open_mod_finanzas, open_win_quiz),
        "inversiones": (open_mod_inversiones, open_win_quiz_inv),
        "impuestos": (open_mod_imp, open_win_quiz_imp),
        "emprende": (open_mod_empre, open_win_quiz_empr),
    }

    news_config_cache: dict[str, Any] = {}

    def load_news_config() -> dict[str, Any]:
        if news_config_cache:
            return news_config_cache
        path = os.path.join(os.path.dirname(__file__), "news_config.json")
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as cfg:
                    data = json.load(cfg)
                if isinstance(data, dict):
                    news_config_cache.update(data)
            except Exception as exc:  # pragma: no cover - logging
                print(f"No se pudo leer news_config.json: {exc}")
        return news_config_cache

    def activate_module(key: str) -> None:
        module_func, quiz_func = module_configs[key]
        container = module_pages[key]

        def go_back() -> None:
            # Mostrar página de progreso directamente
            for p in (page_foros, page_progreso, page_perfil, page_noticias, *bar_pages):
                p.pack_forget()
            page_progreso.pack(fill="both", expand=True)

        def start_quiz() -> None:
            def return_to_module() -> None:
                module_func(container, go_back, start_quiz)
                for p in (page_foros, page_progreso, page_perfil, page_noticias, *bar_pages):
                    p.pack_forget()
                container.pack(fill="both", expand=True)

            quiz_func(container, return_to_module)
            for p in (page_foros, page_progreso, page_perfil, page_noticias, *bar_pages):
                p.pack_forget()
            container.pack(fill="both", expand=True)

        module_func(container, go_back, start_quiz)
        for p in (page_foros, page_progreso, page_perfil, page_noticias, *bar_pages):
            p.pack_forget()
        container.pack(fill="both", expand=True)

    def open_url(url: str) -> None:
        if not url:
            return
        try:
            webbrowser.open_new_tab(url)
        except Exception as exc:  # pragma: no cover - solo logging
            print(f"No se pudo abrir el enlace {url}: {exc}")

    # Apartado de acciones (gráfica)
    stock_loaded = {"done": False}
    symbol_var = tk.StringVar(value="MSFT")
    stock_status = tk.StringVar(value="Selecciona un símbolo del menú para actualizar la gráfica.")

    stock_header = ttk.Frame(page_noticias, style="Page.TFrame")
    stock_header.pack(fill="x", padx=12, pady=(16, 8))
    ttk.Label(stock_header, text="Acciones", style="Page.TLabel").pack(side="left")
    # Menú desplegable de símbolos
    symbols = ["MSFT","BTDR","NVTS","NVDA","PLUG","RXRX","BITF","DOW","AAPL"]
    symbol_combo = ttk.Combobox(
        stock_header,
        textvariable=symbol_var,
        values=symbols,
        width=10,
        state="readonly",
        style="Page.TCombobox",
    )
    symbol_combo.pack(side="right", padx=(0,6), pady=2)
    ttk.Label(stock_header, text="Símbolo:", style="PageText.TLabel").pack(side="right", padx=(0,6))
    # Actualizar automáticamente al seleccionar opción
    def _on_symbol_change(event=None):
        queue_stock_fetch(force=True)
    symbol_combo.bind('<<ComboboxSelected>>', _on_symbol_change)

    stock_status_label = ttk.Label(page_noticias, textvariable=stock_status, style="PageText.TLabel")
    stock_status_label.pack(fill="x", padx=12)

    chart_container = tk.Frame(page_noticias, bg="#fffbe6")
    chart_container.pack(fill="both", expand=True, padx=12, pady=(0, 12))

    chart_state: dict[str, Any] = {"canvas": None, "figure": None}

    def render_stock_chart(dates, prices, symbol: str) -> None:
        # Limpiar gráfico anterior
        try:
            if chart_state["canvas"] is not None:
                chart_state["canvas"].get_tk_widget().destroy()
            if chart_state["figure"] is not None:
                plt.close(chart_state["figure"])
        except Exception:
            pass

        # Paleta y estilo de la app
        page_bg = "#fffbe6"     # fondo página
        card_bg = "#fffaf0"     # fondo tarjeta
        accent = "#ff9800"      # naranja principal
        accent_dark = "#fb8c00" # naranja activo
        border = "#ffcc80"      # borde suave
        text_muted = "#8d6e63"  # texto tenue
        text_body = "#5d4037"   # texto principal

        fig, ax = plt.subplots(figsize=(3.9, 3.0), dpi=120)
        try:
            fig.patch.set_facecolor(page_bg)
            ax.set_facecolor(card_bg)
        except Exception:
            pass

        # Línea y marcadores
        ax.plot(
            dates,
            prices,
            marker="o",
            markersize=3,
            markerfacecolor="#ffb74d",
            markeredgecolor=accent_dark,
            markeredgewidth=0.6,
            linewidth=2.0,
            color=accent,
            solid_capstyle="round",
            antialiased=True,
        )
        # Área sutil bajo la curva
        try:
            ax.fill_between(dates, prices, color=accent, alpha=0.08, zorder=0)
        except Exception:
            pass

        # Títulos y etiquetas
        ax.set_title(
            f"Evolución de {symbol} (último mes)",
            color=accent_dark,
            fontsize=10,
            fontweight="bold",
            pad=8,
        )
        ax.set_ylabel("Precio de cierre", color=text_body)

        # Ejes, rejilla y estilos
        for spine in ax.spines.values():
            spine.set_color(border)
            spine.set_linewidth(1.0)
        ax.grid(True, linestyle=":", color="#ffe0b2", alpha=0.7)
        ax.tick_params(axis="x", colors=text_muted, rotation=0)
        ax.tick_params(axis="y", colors=text_muted)
        ax.yaxis.label.set_color(text_body)

        # Formato de fechas en eje X
        try:
            ax.xaxis.set_major_locator(mdates.AutoDateLocator())
            ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(mdates.AutoDateLocator()))
        except Exception:
            pass
        fig.autofmt_xdate(rotation=30, ha="right")
        ax.margins(x=0)

        # Anotación del último valor
        try:
            if len(prices) > 0:
                x_last = dates[-1]
                y_last = float(prices[-1])
                ax.scatter([x_last], [y_last], color=accent_dark, s=18, zorder=3)
                ax.annotate(
                    f"{y_last:,.2f}",
                    xy=(x_last, y_last),
                    xytext=(6, -10),
                    textcoords="offset points",
                    color=text_body,
                    fontsize=9,
                    bbox=dict(boxstyle="round,pad=0.2", fc=card_bg, ec=border, lw=0.8),
                )
        except Exception:
            pass

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=chart_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        chart_state["canvas"] = canvas
        chart_state["figure"] = fig

    def queue_stock_fetch(force: bool = False) -> None:
        if stock_loaded["done"] and not force:
            return

        def apply_result(dates, prices, status: str) -> None:
            stock_loaded["done"] = True
            stock_status.set(status)
            if dates is not None and prices is not None and len(prices) > 0:
                try:
                    render_stock_chart(dates, prices, symbol_var.get().strip() or "MSFT")
                except Exception as e:
                    stock_status.set(f"Error al renderizar la gráfica: {e}")
            else:
                # limpiar gráfico
                try:
                    if chart_state["canvas"] is not None:
                        chart_state["canvas"].get_tk_widget().destroy()
                    if chart_state["figure"] is not None:
                        plt.close(chart_state["figure"])
                except Exception:
                    pass

        def worker() -> None:
            symbol = symbol_var.get().strip() or "MSFT"
            try:
                dates, prices = fetch_stock(symbol)
                if prices is None or len(prices) == 0:
                    root.after(0, lambda: apply_result(None, None, f"No hay datos para {symbol}."))
                else:
                    root.after(0, lambda: apply_result(dates, prices, ""))
            except Exception as err:
                root.after(0, lambda: apply_result(None, None, f"Error al obtener datos: {err}"))

        stock_loaded["done"] = False
        stock_status.set("Cargando datos...")
        threading.Thread(target=worker, daemon=True).start()

    # (Se eliminó el apartado de videos para dejar solo noticias)

    # Foros — mejora estética
    header_frame = ttk.Frame(page_foros, style="Page.TFrame")
    header_frame.pack(fill="x", padx=12, pady=(12,6))
    ttk.Label(header_frame, text="Foros", style="Page.TLabel").pack(side="left")
    ttk.Label(header_frame, text="Comparte, pregunta y aprende con la comunidad", style="PageText.TLabel").pack(side="left", padx=(12,0))

    # Contenedor principal del chat con fondo suave y padding
    chat_outer = tk.Frame(page_foros, bg="#fbf7f0", bd=0)
    chat_outer.pack(fill="both", expand=True, padx=12, pady=(0,8))

    # Canvas + scrollbar para mensajes (dentro de un frame con padding)
    inner_frame = tk.Frame(chat_outer, bg="#ffffff", bd=0)
    inner_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.98, relheight=0.86)

    chat_canvas = tk.Canvas(inner_frame, bg="#ffffff", highlightthickness=0)
    chat_scroll = ttk.Scrollbar(inner_frame, orient="vertical", command=chat_canvas.yview)
    messages_frame = tk.Frame(chat_canvas, bg="#ffffff")
    chat_canvas.configure(yscrollcommand=chat_scroll.set)
    chat_canvas.pack(side="left", fill="both", expand=True, padx=(8,0), pady=8)
    chat_scroll.pack(side="right", fill="y", padx=(0,8), pady=8)
    chat_canvas.create_window((0,0), window=messages_frame, anchor="nw")

    def _on_frame_configure(e):
        chat_canvas.configure(scrollregion=chat_canvas.bbox("all"))
        chat_canvas.yview_moveto(1.0)
    messages_frame.bind("<Configure>", _on_frame_configure)

    # Estilos de burbuja y fuentes
    user_bg = "#ff9800"
    user_fg = "#ffffff"
    other_bg = "#f3f4f6"
    other_fg = "#2d3436"
    bubble_font = ("Segoe UI", 10)
    # cache de avatares pequeños para mensajes
    message_avatar_cache: dict[str, Any] = {}

    def add_message(sender, text, when=None):
        when = when or datetime.datetime.now().strftime("%H:%M")
        row = tk.Frame(messages_frame, bg="#ffffff")

        # avatar: si hay foto de perfil disponible, usar versión pequeña
        avatar_widget = None
        if sender == "Tú" and user_photo_img and user_photo_img[0]:
            # intentar usar la ruta guardada si existe
            p = user_photo_path.get() if user_photo_path.get() else None
            if p:
                key = f"msg_{os.path.basename(p)}"
                if key not in message_avatar_cache:
                    try:
                        im = Image.open(p).convert('RGBA')
                        im.thumbnail((36,36), RESAMPLE)  # type: ignore[arg-type]
                        # circular mask
                        mask = Image.new('L', im.size, 0)
                        draw = ImageDraw.Draw(mask)
                        draw.ellipse((0,0,im.size[0], im.size[1]), fill=255)
                        im.putalpha(mask)
                        tkav = ImageTk.PhotoImage(im)
                        message_avatar_cache[key] = tkav
                    except Exception:
                        message_avatar_cache[key] = None
                if message_avatar_cache.get(key):
                    avatar_widget = tk.Label(row, image=message_avatar_cache[key], bg="#ffffff")
                else:
                    avatar_widget = tk.Label(row, text="🧑", bg="#ffffff", font=("Segoe UI Emoji", 14))
            else:
                avatar_widget = tk.Label(row, text="🧑", bg="#ffffff", font=("Segoe UI Emoji", 14))
        else:
            avatar_text = "📢" if sender == "Sistema" else "�"
            avatar_widget = tk.Label(row, text=avatar_text, bg="#ffffff", font=("Segoe UI Emoji", 14))

        # burbuja (label con padding y ligero borde redondeado simulado)
        bubble_bg = user_bg if sender == "Tú" else other_bg
        bubble_fg = user_fg if sender == "Tú" else other_fg
        bubble = tk.Label(row, text=text, bg=bubble_bg, fg=bubble_fg, wraplength=300, justify="left",
                          font=bubble_font, padx=12, pady=8, bd=0)
        ts = tk.Label(row, text=when, bg="#ffffff", fg="#888888", font=("Segoe UI", 8))

        # layout según remitente: avatar + burbuja
        if sender == "Tú":
            # Empujar la burbuja a la derecha
            avatar_widget.pack(side="right", padx=(6,12))
            bubble.pack(side="right", padx=(6,12))
            ts.pack(side="right", padx=(6,12), pady=(2,0))
            row.pack(fill="x", pady=8, anchor="e")
        else:
            avatar_widget.pack(side="left", padx=(12,6))
            bubble.pack(side="left", padx=(12,6))
            ts.pack(side="left", padx=(12,6), pady=(2,0))
            row.pack(fill="x", pady=8, anchor="w")

        # Forzar scroll abajo
        chat_canvas.update_idletasks()
        chat_canvas.yview_moveto(1.0)

    # Envía al chatbot de forma asíncrona y muestra la respuesta en el chat
    def request_and_show_response(user_text):
        # carga dinámica del módulo chatbot desde el mismo folder para evitar import circular
        try:
            # intenta import normal (si ya está en sys.modules)
            import chatbot as _chatbot
        except Exception:
            try:
                # carga por ruta absoluta
                chatbot_path = os.path.join(os.path.dirname(__file__), "chatbot.py")
                spec = importlib.util.spec_from_file_location("chatbot_local", chatbot_path)
                if spec is None or spec.loader is None:
                    raise ImportError("No se pudo cargar el módulo chatbot")
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                _chatbot = module
            except Exception as e:
                # fallback local si no se pudo cargar el módulo
                resp_text = f"(error cargando chatbot) {e}"
                root.after(0, lambda: add_message("Sistema", resp_text))
                return

        try:
            resp_text = _chatbot.get_response(user_text)
        except Exception as e:
            resp_text = f"(error en chatbot) {e}"
        root.after(0, lambda: add_message("Sistema", resp_text))

    # Entrada de texto y botón
    # Área de entrada mejorada: Text multiline para permitir saltos de línea
    entry_frame = tk.Frame(page_foros, bg="#fff6e5")
    entry_frame.pack(fill="x", padx=12, pady=(8,12))
    msg_text = tk.Text(entry_frame, height=3, font=("Segoe UI", 11), bd=0, relief="flat", wrap="word")
    msg_text.pack(side="left", fill="x", expand=True, padx=(8,8), pady=8)
    msg_text.configure(highlightthickness=1, highlightbackground="#e0e0e0", highlightcolor="#e0e0e0")

    # Enviar con Enter, Shift+Enter inserta nueva línea
    def send_message(event=None):
        content = msg_text.get("1.0", "end").strip()
        if not content:
            return "break"
        add_message("Tú", content)
        msg_text.delete("1.0", "end")
        # llamar a la API en hilo separado
        threading.Thread(target=request_and_show_response, args=(content,), daemon=True).start()
        return "break"

    def handle_key(event):
        if event.keysym == 'Return' and not (event.state & 0x0001):
            # Enter without Shift -> send
            return send_message()
        # Shift+Enter or others -> default behavior (insert newline)

    msg_text.bind('<KeyPress-Return>', handle_key)

    # Botones (adjuntar y enviar)
    btns_frame = tk.Frame(entry_frame, bg="#fff6e5")
    btns_frame.pack(side="right", padx=(0,6), pady=6)
    def attach_file():
        p = filedialog.askopenfilename(title="Adjuntar archivo", filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.gif"), ("Todos", "*")])
        if p:
            add_message("Tú", "[Archivo adjunto] " + os.path.basename(p))

    attach_btn = tk.Button(btns_frame, text="📎", bg="#ffffff", bd=0, font=("Segoe UI", 12), cursor="hand2", command=attach_file)
    attach_btn.pack(side="top", pady=(2,4))
    send_btn = tk.Button(btns_frame, text="Enviar", bg="#ff9800", fg="#ffffff", bd=0, activebackground="#fb8c00",
                         font=("Segoe UI", 10, "bold"), padx=10, pady=6, cursor="hand2", relief="flat", command=send_message)
    send_btn.pack(side="top")
    # hover visual
    def _on_enter_btn(e): e.widget.configure(bg="#fb8c00")
    def _on_leave_btn(e): e.widget.configure(bg="#ff9800")
    send_btn.bind('<Enter>', _on_enter_btn)
    send_btn.bind('<Leave>', _on_leave_btn)

    # mensajes iniciales de ejemplo
    add_message("Sistema", "Bienvenido al foro. Aquí puedes preguntar o compartir ideas.")
    add_message("Ana", "Hola! ¿Alguien tiene recursos sobre finanzas personales?")

    # Progreso con gráfica de barras
    ttk.Label(page_progreso, text="Progreso", style="Page.TLabel").pack(pady=(30,10))
    ttk.Label(page_progreso, text="Tu avance en 4 áreas:", style="PageText.TLabel").pack(pady=(0,20))

    bar_canvas = tk.Canvas(page_progreso, width=360, height=760, bg="#fffbe6", highlightthickness=0)
    bar_canvas.pack(pady=10)
    bar_colors = ["#ff9800", "#43a047", "#1e88e5", "#d81b60"]
    bar_labels = ["Finanzas", "Inversiones", "Impuestos", "Emprende"]
    bar_values = [180, 120, 220, 160]
    bar_btns = []
    bar_width = 60
    spacing = 30
    total_width = 4 * bar_width + 3 * spacing
    # centrar horizontalmente y desplazar ligeramente a la izquierda
    x0 = max(10, int((360 - total_width) / 2) - 20)
    y_base = 220
    def bar_callback(idx):
        try:
            key = module_keys[idx]
        except IndexError:
            return
        activate_module(key)
    for i in range(4):
        x = x0 + i * (bar_width + spacing)
        y = y_base - bar_values[i]
        bar_canvas.create_rectangle(x, y, x+bar_width, y_base, fill=bar_colors[i], outline="", width=0)
        bar_canvas.create_text(x+bar_width/2, y_base+22, text=bar_labels[i], font=("Segoe UI", 10, "bold"), fill=bar_colors[i])
        btn = tk.Button(bar_canvas, bg=bar_colors[i], activebackground=bar_colors[i], bd=0, highlightthickness=0, cursor="hand2",
                        command=lambda idx=i: bar_callback(idx))
        bar_canvas.create_window(x+bar_width/2, (y+y_base)/2, window=btn, width=bar_width, height=bar_values[i])
        bar_btns.append(btn)

    # Mascota pingüino (debajo de las gráficas de barras)
    penguin_photo_ref: list[Any] = [None]
    try:
        penguin_path = os.path.join(os.path.dirname(__file__), "aa.png")
        penguin_img = Image.open(penguin_path).resize((80, 80))
        penguin_photo = ImageTk.PhotoImage(penguin_img)
        penguin_photo_ref[0] = penguin_photo  # Mantener referencia para evitar GC
        penguin_label = ttk.Label(page_progreso, image=penguin_photo, style="Page.TFrame")
        penguin_label.pack(pady=(10, 6))
    except Exception:
        penguin_label = ttk.Label(page_progreso, text="🐧", font=("Segoe UI Emoji", 48), style="Page.TFrame")
        penguin_label.pack(pady=(10, 6))

    # Perfil funcional con correo y guardado de foto
    user_name = tk.StringVar()
    user_email = tk.StringVar()
    user_photo_path = tk.StringVar()
    user_logged = tk.BooleanVar(value=False)
    user_photo_img: list[Any] = [None]
    # Resample filter compatible con distintas versiones de Pillow
    try:
        from PIL.Image import Resampling as _Resampling  # type: ignore
        RESAMPLE = _Resampling.LANCZOS
    except Exception:
        # Fallbacks si el stub no define los atributos
        try:
            from PIL.Image import NEAREST as _NEAREST  # type: ignore
        except Exception:
            _NEAREST = 0  # type: ignore
        RESAMPLE = getattr(Image, "LANCZOS", getattr(Image, "BICUBIC", _NEAREST))
    # carpeta local donde se guardarán fotos (ruta absoluta para evitar problemas de cwd)
    PROFILE_PHOTOS_DIR = os.path.join(os.path.dirname(__file__), '..', 'profile_photos')
    PROFILE_PHOTOS_DIR = os.path.normpath(PROFILE_PHOTOS_DIR)
    os.makedirs(PROFILE_PHOTOS_DIR, exist_ok=True)
    PROFILE_DATA_FILE = os.path.join(PROFILE_PHOTOS_DIR, 'profile.json')

    def save_profile_data():
        # Guarda nombre, email y ruta de foto en un archivo JSON (documento de texto)
        try:
            photo_val = user_photo_path.get() or ""
            # almacenar solo basename para portabilidad
            if photo_val:
                photo_val = os.path.basename(photo_val)
            data = {
                'name': user_name.get(),
                'email': user_email.get(),
                'photo': photo_val
            }
            with open(PROFILE_DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Profile saved to {PROFILE_DATA_FILE}: {data}")
        except Exception as e:
            # no bloqueante; mostrar error si es crítico
            print(f"Error guardando profile data: {e}")

    def load_profile_data():
        # Carga los datos de perfil desde el JSON si existe
        try:
            if os.path.exists(PROFILE_DATA_FILE):
                with open(PROFILE_DATA_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    name = data.get('name', '').strip()
                    email = data.get('email', '').strip()
                    photo = data.get('photo', '')
                    print(f"Loaded profile data: name={name}, email={email}, photo={photo}")
                    if name:
                        user_name.set(name)
                    if email:
                        user_email.set(email)
                    if photo:
                        # normalizar ruta: si es relativa buscar en PROFILE_PHOTOS_DIR
                        if not os.path.isabs(photo):
                            candidate = os.path.join(PROFILE_PHOTOS_DIR, os.path.basename(photo))
                        else:
                            candidate = photo
                        if os.path.exists(candidate):
                            user_photo_path.set(candidate)
                            user_logged.set(True)
        except Exception as e:
            print(f"Error cargando profile data: {e}")

    # (Nota: carga de datos de perfil se hace más abajo, una vez que
    # las funciones UI como show_profile() están definidas.)

    def make_circle_image(img_path, size=(128,128)):
        # Cargar imagen y crear versión circular con buen antialiasing
        img = Image.open(img_path).convert("RGBA")
        # Escalar manteniendo aspecto para que quepa en size
        img.thumbnail(size, RESAMPLE)  # type: ignore[arg-type]
        # Crear lienzo cuadrado transparente
        canvas = Image.new('RGBA', size, (255,255,255,0))
        x = (size[0] - img.width) // 2
        y = (size[1] - img.height) // 2
        canvas.paste(img, (x, y), img)
        # Máscara circular
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0], size[1]), fill=255)
        canvas.putalpha(mask)
        return ImageTk.PhotoImage(canvas)

    def update_profile_image(path: str | None):
        """Crea la imagen circular y la asigna al label de perfil de forma segura.
        Devuelve True si se actualizó correctamente, False si hubo error.
        """
        try:
            if not path or not os.path.exists(path):
                # limpiar
                photo_label.config(image="")
                return False
            imgtk = make_circle_image(path, size=(128,128))
            photo_label.config(image=imgtk)
            # Mantener referencia para evitar GC
            user_photo_img[0] = imgtk
            return True
        except Exception as e:
            print(f"Error actualizando imagen de perfil: {e}")
            try:
                photo_label.config(image="")
            except Exception:
                pass
            return False

    def select_photo():
        path = filedialog.askopenfilename(
            title="Selecciona tu foto de perfil",
            filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.gif")]
        )
        if path:
            user_photo_path.set(path)
            try:
                # Mostrar inmediatamente en el UI usando helper
                ok = update_profile_image(path)
                if not ok:
                    messagebox.showwarning("Aviso", "La imagen fue seleccionada pero no se pudo mostrar correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la imagen:\n{e}")

    def save_profile():
        name = user_name.get().strip()
        email = user_email.get().strip()
        if not name or not email:
            messagebox.showwarning("Faltan datos", "Por favor ingresa tu nombre y correo electrónico.")
            return
        # Guardar foto en carpeta profile_photos
        if user_photo_path.get():
            ext = os.path.splitext(user_photo_path.get())[-1]
            save_path = os.path.join(PROFILE_PHOTOS_DIR, f"{email.replace('@','_at_')}{ext}")
            try:
                # Guardar una copia redimensionada y optimizada en la carpeta de la app
                img = Image.open(user_photo_path.get()).convert('RGBA')
                img.thumbnail((256,256), RESAMPLE)  # type: ignore[arg-type]
                img.save(save_path)
                user_photo_path.set(save_path)
                # Actualizar UI usando helper
                ok = update_profile_image(save_path)
                if not ok:
                    messagebox.showwarning("Aviso", "La foto se guardó pero no se pudo mostrar en el perfil.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar la imagen:\n{e}")
                return
        user_logged.set(True)
        # Persistir datos en JSON
        # Guardar foto como basename para mayor portabilidad
        if user_photo_path.get():
            try:
                save_profile_data()
            except Exception:
                pass
        show_profile()

    def show_profile():
        for p in (page_foros, page_progreso, page_perfil, page_noticias, *bar_pages):
            p.pack_forget()
        page_perfil.pack(fill="both", expand=True)
        if user_logged.get():
            name_display.config(text=f"👤 {user_name.get()}")
            email_display.config(text=f"📧 {user_email.get()}")
            if user_photo_path.get():
                try:
                    # Si se guarda una ruta relativa o en otra carpeta, intentar varios candidatos
                    candidates = [
                        user_photo_path.get(),
                        os.path.join(PROFILE_PHOTOS_DIR, os.path.basename(user_photo_path.get())),
                        os.path.join(os.path.dirname(__file__), os.path.basename(user_photo_path.get())),
                    ]
                    found = None
                    for c in candidates:
                        if c and os.path.exists(c):
                            found = c
                            break
                    if found:
                        ok = update_profile_image(found)
                        if not ok:
                            print("Perfil: no se pudo actualizar imagen desde", found)
                    else:
                        update_profile_image(None)
                except:
                    update_profile_image(None)
            else:
                update_profile_image(None)
            login_frame.pack_forget()
            profile_frame.pack(pady=30)
        else:
            profile_frame.pack_forget()
            login_frame.pack(pady=30)

    # Frame de login/registro
    login_frame = ttk.Frame(page_perfil, style="Page.TFrame")
    ttk.Label(login_frame, text="Registro / Login", style="Page.TLabel").pack(pady=(0,10))
    ttk.Label(login_frame, text="Nombre:", style="PageText.TLabel").pack(anchor="w")
    name_entry = ttk.Entry(login_frame, textvariable=user_name, font=("Segoe UI", 13))
    name_entry.pack(fill="x", padx=10, pady=6)
    ttk.Label(login_frame, text="Correo electrónico:", style="PageText.TLabel").pack(anchor="w")
    email_entry = ttk.Entry(login_frame, textvariable=user_email, font=("Segoe UI", 13))
    email_entry.pack(fill="x", padx=10, pady=6)
    ttk.Button(login_frame, text="Seleccionar foto", command=select_photo).pack(pady=6)
    ttk.Button(login_frame, text="Guardar perfil", command=save_profile).pack(pady=10)

    # Frame de perfil mostrado
    profile_frame = ttk.Frame(page_perfil, style="Page.TFrame")
    # placeholder frame para el avatar (mantiene tamaño incluso sin imagen)
    avatar_holder = tk.Frame(profile_frame, width=140, height=140, bg="#fffbe6")
    avatar_holder.pack_propagate(False)
    avatar_holder.pack(pady=6)
    # Use tk.Label for image compatibility and to avoid ttk image handling issues
    photo_label = tk.Label(avatar_holder, bg="#fffbe6")
    photo_label.pack(expand=True)
    name_display = ttk.Label(profile_frame, text="", style="Page.TLabel")
    name_display.pack(pady=6)
    email_display = ttk.Label(profile_frame, text="", style="PageText.TLabel")
    email_display.pack(pady=6)
    ttk.Button(profile_frame, text="Editar perfil", command=lambda: user_logged.set(False) or show_profile()).pack(pady=10)

    # Navegación y barra inferior
    def show_page(page):
        for p in (page_foros, page_progreso, page_perfil, page_noticias, *bar_pages):
            p.pack_forget()
        if page == page_perfil:
            show_profile()
        elif page == page_noticias:
            page.pack(fill="both", expand=True)
            queue_stock_fetch()
        else:
            page.pack(fill="both", expand=True)

    shadow = tk.Frame(root, bg="#ffd180", height=6, width=width)
    shadow.place(relx=0, rely=1, anchor="sw")
    nav_bar = ttk.Frame(root, style="Nav.TFrame")
    nav_bar.place(relx=0, rely=1, anchor="sw", width=width, height=72)
    btn_foros = ttk.Button(nav_bar, text="🗨️", style="Nav.TButton", command=lambda: show_page(page_foros))
    btn_progreso = ttk.Button(nav_bar, text="📊", style="Nav.TButton", command=lambda: show_page(page_progreso))
    btn_noticias = ttk.Button(nav_bar, text="📰", style="Nav.TButton", command=lambda: show_page(page_noticias))
    btn_perfil = ttk.Button(nav_bar, text="🧑‍💼", style="Nav.TButton", command=lambda: show_page(page_perfil))
    # Reposicionar para 4 botones (sin videos)
    btn_foros.place(relx=0.12, rely=0.5, anchor="center", width=72, height=52)
    btn_progreso.place(relx=0.38, rely=0.5, anchor="center", width=72, height=52)
    btn_noticias.place(relx=0.62, rely=0.5, anchor="center", width=72, height=52)
    btn_perfil.place(relx=0.88, rely=0.5, anchor="center", width=72, height=52)
    def on_enter(e): e.widget.configure(style="Nav.TButton")
    def on_leave(e): e.widget.configure(style="Nav.TButton")
    for btn in (btn_foros, btn_progreso, btn_noticias, btn_perfil):
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
    # Cargar datos de perfil al iniciar y mostrar si existe
    try:
        load_profile_data()
        if user_logged.get():
            show_profile()
            # Debug: report photo path and whether image was set
            print("Startup: user_logged=True, user_photo_path=", user_photo_path.get())
            has_img = getattr(photo_label, 'image', None) is not None
            print("Startup: photo_label has image?", has_img)
    except Exception as e:
        print("Error during startup profile load:", e)

    show_page(page_progreso)
    root.mainloop()

if __name__ == "__main__":
    main()