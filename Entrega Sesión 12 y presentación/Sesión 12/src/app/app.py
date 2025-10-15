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
    page_videos = ttk.Frame(main_frame, style="Page.TFrame")
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
            show_page(page_progreso)

        def start_quiz() -> None:
            def return_to_module() -> None:
                module_func(container, go_back, start_quiz)
                show_page(container)

            quiz_func(container, return_to_module)
            show_page(container)

        module_func(container, go_back, start_quiz)
        show_page(container)

    def open_url(url: str) -> None:
        if not url:
            return
        try:
            webbrowser.open_new_tab(url)
        except Exception as exc:  # pragma: no cover - solo logging
            print(f"No se pudo abrir el enlace {url}: {exc}")

    # Apartado de noticias
    news_loaded = {"done": False}
    news_status = tk.StringVar(value="Pulsa Actualizar para cargar noticias financieras.")

    news_header = ttk.Frame(page_noticias, style="Page.TFrame")
    news_header.pack(fill="x", padx=12, pady=(16, 8))
    ttk.Label(news_header, text="Noticias financieras", style="Page.TLabel").pack(side="left")
    news_refresh_btn = ttk.Button(
        news_header,
        text="Actualizar",
        command=lambda: queue_news_fetch(force=True),
    )
    news_refresh_btn.pack(side="right")

    news_status_label = ttk.Label(page_noticias, textvariable=news_status, style="PageText.TLabel")
    news_status_label.pack(fill="x", padx=12)

    news_wrapper = tk.Frame(page_noticias, bg="#fffbe6")
    news_wrapper.pack(fill="both", expand=True, padx=12, pady=(0, 12))

    news_canvas = tk.Canvas(news_wrapper, bg="#fffbe6", highlightthickness=0)
    news_scroll = ttk.Scrollbar(news_wrapper, orient="vertical", command=news_canvas.yview)
    news_list = tk.Frame(news_canvas, bg="#fffbe6")
    news_canvas.configure(yscrollcommand=news_scroll.set)
    news_canvas.pack(side="left", fill="both", expand=True)
    news_scroll.pack(side="right", fill="y")
    news_canvas.create_window((0, 0), window=news_list, anchor="nw")

    def _sync_news_scroll(event: tk.Event) -> None:
        news_canvas.configure(scrollregion=news_canvas.bbox("all"))

    news_list.bind("<Configure>", _sync_news_scroll)

    def render_news(items: list[dict[str, str]]) -> None:
        for child in news_list.winfo_children():
            child.destroy()
        if not items:
            ttk.Label(
                news_list,
                text="No se encontraron noticias en este momento.",
                style="PageText.TLabel",
                wraplength=320,
                justify="left",
            ).pack(anchor="w", pady=12, padx=4)
            return
        for item in items:
            card = tk.Frame(
                news_list,
                bg="#fffaf0",
                highlightbackground="#ffcc80",
                highlightthickness=1,
                bd=0,
            )
            card.pack(fill="x", padx=4, pady=8)
            tk.Label(
                card,
                text=item.get("title", ""),
                font=("Segoe UI", 12, "bold"),
                fg="#bf360c",
                bg="#fffaf0",
                wraplength=320,
                justify="left",
            ).pack(anchor="w", padx=12, pady=(12, 6))
            description = item.get("description") or ""
            if description:
                tk.Label(
                    card,
                    text=description,
                    font=("Segoe UI", 10),
                    fg="#5d4037",
                    bg="#fffaf0",
                    wraplength=320,
                    justify="left",
                ).pack(anchor="w", padx=12, pady=(0, 8))
            source_text = item.get("source") or ""
            if source_text:
                tk.Label(
                    card,
                    text=source_text,
                    font=("Segoe UI", 9, "italic"),
                    fg="#8d6e63",
                    bg="#fffaf0",
                ).pack(anchor="w", padx=12, pady=(0, 6))
            url = item.get("url")
            if url:
                tk.Button(
                    card,
                    text="Leer artículo",
                    command=lambda link=url: open_url(link),
                    bg="#ff9800",
                    fg="white",
                    activebackground="#fb8c00",
                    activeforeground="white",
                    bd=0,
                    padx=10,
                    pady=6,
                    cursor="hand2",
                ).pack(anchor="w", padx=12, pady=(0, 12))

    def queue_news_fetch(force: bool = False) -> None:
        if news_loaded["done"] and not force:
            return

        def apply_result(items: list[dict[str, str]], status: str) -> None:
            news_loaded["done"] = True
            news_status.set(status)
            render_news(items)

        def worker() -> None:
            config = load_news_config()
            base_url = os.getenv("FINANCE_NEWS_API_URL", "").strip() or str(config.get("api_url", "")).strip()
            token = os.getenv("FINANCE_NEWS_API_TOKEN", "").strip() or str(config.get("api_token", "")).strip()
            if not base_url:
                root.after(0, lambda: apply_result([], "Configura FINANCE_NEWS_API_URL para ver noticias."))
                return

            params_config = config.get("params", {}) if isinstance(config.get("params"), dict) else {}
            params: dict[str, str] = {
                "services": os.getenv("FINANCE_NEWS_SERVICES", str(params_config.get("services", "600,604,608,614,615,618,620,655"))),
                "filter": os.getenv("FINANCE_NEWS_FILTER", str(params_config.get("filter", "0"))),
                "period": os.getenv("FINANCE_NEWS_PERIOD", str(params_config.get("period", "0"))),
                "listType": os.getenv("FINANCE_NEWS_LISTTYPE", str(params_config.get("listType", "6"))),
                "rows": os.getenv("FINANCE_NEWS_ROWS", str(params_config.get("rows", "20"))),
                "includeBreaking": os.getenv("FINANCE_NEWS_INCLUDE_BREAKING", str(params_config.get("includeBreaking", "true"))),
                "excludeTables": os.getenv("FINANCE_NEWS_EXCLUDE_TABLES", str(params_config.get("excludeTables", "false"))),
                "page": os.getenv("FINANCE_NEWS_PAGE", str(params_config.get("page", "1"))),
            }

            optional = {
                "words": os.getenv("FINANCE_NEWS_WORDS", str(params_config.get("words", "")).strip()),
                "tag": os.getenv("FINANCE_NEWS_TAG", str(params_config.get("tag", "")).strip()),
                "sourcesId": os.getenv("FINANCE_NEWS_SOURCES", str(params_config.get("sourcesId", "")).strip()),
                "sectors": os.getenv("FINANCE_NEWS_SECTORS", str(params_config.get("sectors", "")).strip()),
                "ambit": os.getenv("FINANCE_NEWS_AMBIT", str(params_config.get("ambit", "")).strip()),
                "onlyTop": os.getenv("FINANCE_NEWS_ONLY_TOP", str(params_config.get("onlyTop", "")).strip()),
                "symbol": os.getenv("FINANCE_NEWS_SYMBOL", str(params_config.get("symbol", "")).strip()),
                "startDate": os.getenv("FINANCE_NEWS_START_DATE", str(params_config.get("startDate", "")).strip()),
                "endDate": os.getenv("FINANCE_NEWS_END_DATE", str(params_config.get("endDate", "")).strip()),
                "newsTypeId": os.getenv("FINANCE_NEWS_TYPES", str(params_config.get("newsTypeId", "")).strip()),
            }
            for key, value in optional.items():
                if value:
                    params[key] = value

            headers = {"Accept": "application/json"}
            if token:
                headers["Authorization"] = f"Bearer {token}"

            article_template = os.getenv("FINANCE_NEWS_ARTICLE_URL_TEMPLATE", "").strip() or str(config.get("article_url_template", "")).strip()

            try:
                response = requests.get(base_url, params=params, headers=headers, timeout=10)
                response.raise_for_status()
                payload = response.json()
                records = payload.get("data", []) if isinstance(payload, dict) else []
                items: list[dict[str, str]] = []
                for record in records:
                    if not isinstance(record, dict):
                        continue
                    title = record.get("header") or "Sin título"
                    summary = record.get("abstract") or ""
                    service = record.get("serviceId")
                    date_str = record.get("date") or ""
                    time_str = record.get("time") or ""
                    timestamp = " ".join(filter(None, [date_str, time_str])).strip()
                    source_bits = []
                    if service is not None:
                        source_bits.append(f"Servicio {service}")
                    if timestamp:
                        source_bits.append(timestamp)
                    source = " · ".join(source_bits)
                    url = record.get("url") or record.get("imageURL") or ""
                    news_id = record.get("newsId")
                    if article_template and news_id:
                        try:
                            url = article_template.format(newsId=news_id)
                        except Exception:
                            pass
                    items.append(
                        {
                            "title": title,
                            "description": summary,
                            "source": source,
                            "url": url,
                        }
                    )
                status_text = "" if items else "No se encontraron noticias en este momento."
                root.after(0, lambda: apply_result(items, status_text))
            except requests.RequestException as err:
                message = f"No se pudieron cargar noticias ({err})."
                root.after(0, lambda: apply_result([], message))

        news_loaded["done"] = False
        news_status.set("Cargando noticias...")
        threading.Thread(target=worker, daemon=True).start()

    # Apartado de videos
    video_loaded = {"done": False}
    video_status = tk.StringVar(value="Pulsa Actualizar para buscar concursos de finanzas.")

    video_header = ttk.Frame(page_videos, style="Page.TFrame")
    video_header.pack(fill="x", padx=12, pady=(16, 8))
    ttk.Label(video_header, text="Concursos de finanzas", style="Page.TLabel").pack(side="left")
    video_refresh_btn = ttk.Button(
        video_header,
        text="Actualizar",
        command=lambda: queue_videos_fetch(force=True),
    )
    video_refresh_btn.pack(side="right")

    video_status_label = ttk.Label(page_videos, textvariable=video_status, style="PageText.TLabel")
    video_status_label.pack(fill="x", padx=12)

    video_wrapper = tk.Frame(page_videos, bg="#fffbe6")
    video_wrapper.pack(fill="both", expand=True, padx=12, pady=(0, 12))

    video_canvas = tk.Canvas(video_wrapper, bg="#fffbe6", highlightthickness=0)
    video_scroll = ttk.Scrollbar(video_wrapper, orient="vertical", command=video_canvas.yview)
    video_list = tk.Frame(video_canvas, bg="#fffbe6")
    video_canvas.configure(yscrollcommand=video_scroll.set)
    video_canvas.pack(side="left", fill="both", expand=True)
    video_scroll.pack(side="right", fill="y")
    video_canvas.create_window((0, 0), window=video_list, anchor="nw")

    def _sync_video_scroll(event: tk.Event) -> None:
        video_canvas.configure(scrollregion=video_canvas.bbox("all"))

    video_list.bind("<Configure>", _sync_video_scroll)

    def _format_date(value: str) -> str:
        if not value:
            return ""
        try:
            dt = datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
            return dt.strftime("%d/%m/%Y")
        except Exception:
            return value.split("T")[0]

    def render_videos(items: list[dict[str, str]]) -> None:
        for child in video_list.winfo_children():
            child.destroy()
        if not items:
            ttk.Label(
                video_list,
                text="No se encontraron videos en este momento.",
                style="PageText.TLabel",
                wraplength=320,
                justify="left",
            ).pack(anchor="w", pady=12, padx=4)
            return
        for item in items:
            card = tk.Frame(
                video_list,
                bg="#fffaf0",
                highlightbackground="#c5e1a5",
                highlightthickness=1,
                bd=0,
            )
            card.pack(fill="x", padx=4, pady=8)
            tk.Label(
                card,
                text=item.get("title", ""),
                font=("Segoe UI", 12, "bold"),
                fg="#1b5e20",
                bg="#fffaf0",
                wraplength=320,
                justify="left",
            ).pack(anchor="w", padx=12, pady=(12, 6))
            channel = item.get("channel")
            if channel:
                tk.Label(
                    card,
                    text=f"Canal: {channel}",
                    font=("Segoe UI", 10),
                    fg="#33691e",
                    bg="#fffaf0",
                ).pack(anchor="w", padx=12)
            published = item.get("published")
            if published:
                tk.Label(
                    card,
                    text=f"Publicado: {published}",
                    font=("Segoe UI", 9),
                    fg="#558b2f",
                    bg="#fffaf0",
                ).pack(anchor="w", padx=12, pady=(0, 6))
            url = item.get("url")
            if url:
                tk.Button(
                    card,
                    text="Ver en YouTube",
                    command=lambda link=url: open_url(link),
                    bg="#43a047",
                    fg="white",
                    activebackground="#388e3c",
                    activeforeground="white",
                    bd=0,
                    padx=10,
                    pady=6,
                    cursor="hand2",
                ).pack(anchor="w", padx=12, pady=(0, 12))

    def queue_videos_fetch(force: bool = False) -> None:
        if video_loaded["done"] and not force:
            return

        def apply_result(items: list[dict[str, str]], status: str) -> None:
            video_loaded["done"] = True
            video_status.set(status)
            render_videos(items)

        def worker() -> None:
            api_key = os.getenv("YOUTUBE_API_KEY", "").strip()
            if not api_key:
                root.after(0, lambda: apply_result([], "Configura YOUTUBE_API_KEY para ver videos."))
                return
            params = {
                "part": "snippet",
                "maxResults": 8,
                "q": "concurso finanzas",
                "type": "video",
                "order": "relevance",
                "safeSearch": "moderate",
                "relevanceLanguage": "es",
                "key": api_key,
            }
            try:
                response = requests.get(
                    "https://www.googleapis.com/youtube/v3/search",
                    params=params,
                    timeout=10,
                )
                response.raise_for_status()
                payload = response.json()
                items: list[dict[str, str]] = []
                for entry in payload.get("items", []):
                    if not isinstance(entry, dict):
                        continue
                    id_info = entry.get("id") or {}
                    snippet = entry.get("snippet") or {}
                    video_id = id_info.get("videoId")
                    if not video_id:
                        continue
                    items.append(
                        {
                            "title": snippet.get("title", "Sin título"),
                            "channel": snippet.get("channelTitle", ""),
                            "published": _format_date(snippet.get("publishedAt", "")),
                            "url": f"https://www.youtube.com/watch?v={video_id}",
                        }
                    )
                status_text = "" if items else "No se encontraron videos en este momento."
                root.after(0, lambda: apply_result(items, status_text))
            except requests.RequestException as err:
                message = f"No se pudieron cargar videos ({err})."
                root.after(0, lambda: apply_result([], message))

        video_loaded["done"] = False
        video_status.set("Buscando videos...")
        threading.Thread(target=worker, daemon=True).start()

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
                        im.thumbnail((36,36), RESAMPLE)
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

    # Mascota pingüino (asegura que se muestre antes del canvas)
    try:
        penguin_img = Image.open("penguin.png").resize((80, 80))
        penguin_photo = ImageTk.PhotoImage(penguin_img)
        penguin_label = ttk.Label(page_progreso, image=penguin_photo, style="Page.TFrame")
        penguin_label.image = penguin_photo  # Mantener referencia
        penguin_label.pack(pady=(0, 10))
    except Exception:
        penguin_label = ttk.Label(page_progreso, text="🐧", font=("Segoe UI Emoji", 48), style="Page.TFrame")
        penguin_label.pack(pady=(0, 10))

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

    # Perfil funcional con correo y guardado de foto
    user_name = tk.StringVar()
    user_email = tk.StringVar()
    user_photo_path = tk.StringVar()
    user_logged = tk.BooleanVar(value=False)
    user_photo_img: list[Any] = [None]
    # Resample filter compatible con distintas versiones de Pillow
    try:
        RESAMPLE = Image.LANCZOS
    except Exception:
        try:
            RESAMPLE = Image.Resampling.LANCZOS
        except Exception:
            RESAMPLE = Image.BICUBIC
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
        img.thumbnail(size, RESAMPLE)
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
                photo_label.image = None
                return False
            imgtk = make_circle_image(path, size=(128,128))
            photo_label.config(image=imgtk)
            # Mantener referencia para evitar GC
            photo_label.image = imgtk
            user_photo_img[0] = imgtk
            return True
        except Exception as e:
            print(f"Error actualizando imagen de perfil: {e}")
            try:
                photo_label.config(image="")
                photo_label.image = None
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
                img.thumbnail((256,256), RESAMPLE)
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
        for p in (page_foros, page_progreso, page_perfil, page_noticias, page_videos, *bar_pages):
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
        for p in (page_foros, page_progreso, page_perfil, page_noticias, page_videos, *bar_pages):
            p.pack_forget()
        if page == page_perfil:
            show_profile()
        elif page == page_noticias:
            page.pack(fill="both", expand=True)
            queue_news_fetch()
        elif page == page_videos:
            page.pack(fill="both", expand=True)
            queue_videos_fetch()
        else:
            page.pack(fill="both", expand=True)

    shadow = tk.Frame(root, bg="#ffd180", height=6, width=width)
    shadow.place(relx=0, rely=1, anchor="sw")
    nav_bar = ttk.Frame(root, style="Nav.TFrame")
    nav_bar.place(relx=0, rely=1, anchor="sw", width=width, height=72)
    btn_foros = ttk.Button(nav_bar, text="🗨️", style="Nav.TButton", command=lambda: show_page(page_foros))
    btn_progreso = ttk.Button(nav_bar, text="📊", style="Nav.TButton", command=lambda: show_page(page_progreso))
    btn_noticias = ttk.Button(nav_bar, text="📰", style="Nav.TButton", command=lambda: show_page(page_noticias))
    btn_videos = ttk.Button(nav_bar, text="🎬", style="Nav.TButton", command=lambda: show_page(page_videos))
    btn_perfil = ttk.Button(nav_bar, text="🧑‍💼", style="Nav.TButton", command=lambda: show_page(page_perfil))
    btn_foros.place(relx=0.08, rely=0.5, anchor="w", width=72, height=52)
    btn_progreso.place(relx=0.3, rely=0.5, anchor="center", width=72, height=52)
    btn_noticias.place(relx=0.5, rely=0.5, anchor="center", width=72, height=52)
    btn_videos.place(relx=0.7, rely=0.5, anchor="center", width=72, height=52)
    btn_perfil.place(relx=0.92, rely=0.5, anchor="e", width=72, height=52)
    def on_enter(e): e.widget.configure(style="Nav.TButton")
    def on_leave(e): e.widget.configure(style="Nav.TButton")
    for btn in (btn_foros, btn_progreso, btn_noticias, btn_videos, btn_perfil):
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