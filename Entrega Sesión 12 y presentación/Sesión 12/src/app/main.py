import tkinter as tk
from tkinter import ttk
import os
import subprocess
import sys

# Try to import Pillow for proper image resizing; if not available we'll fall back to PhotoImage subsample
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

def main():
    root = tk.Tk()
    root.title("FININGO")
    width = 420
    height = int(width * 16 / 9)
    root.geometry(f"{width}x{height}")
    root.minsize(width, height)
    root.maxsize(width, height)
    root.resizable(False, False)
    root.configure(bg="#fff6e5")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Main.TFrame", background="#fff6e5")
    style.configure("Title.TLabel", background="#fff6e5", font=("Segoe UI", 28, "bold"), foreground="#fb8c00")
    style.configure("Btn.TButton", background="#ff9800", foreground="#fff", font=("Segoe UI", 16, "bold"), borderwidth=0)
    style.map("Btn.TButton",
        background=[("active", "#fb8c00"), ("pressed", "#fb8c00")],
        foreground=[("active", "#fff"), ("pressed", "#fff")]
    )

    frame = ttk.Frame(root, style="Main.TFrame")
    frame.pack(fill="both", expand=True)

    # Título superior
    ttk.Label(frame, text="FININGO", style="Title.TLabel").pack(pady=(32, 24))

    # Contenedor para la imagen/pingüino
    img_container = ttk.Frame(frame, style="Main.TFrame")
    img_container.pack(expand=True)
    canvas_size = 220
    penguin_canvas = tk.Canvas(img_container, width=canvas_size, height=canvas_size, bg="#fff6e5", highlightthickness=0)
    penguin_canvas.pack(expand=True)

    def draw_penguin(c, size):
        """Dibuja un pingüino estilizado en el canvas c con tamaño dado (fallback)."""
        cx = cy = size / 2
        body_w = size * 0.5
        body_h = size * 0.6

        # Cuerpo (óvalo negro)
        c.create_oval(cx - body_w/2, cy - body_h/2, cx + body_w/2, cy + body_h/2, fill="#000", outline="")

        # Panza (óvalo blanco)
        belly_w = body_w * 0.65
        belly_h = body_h * 0.7
        c.create_oval(cx - belly_w/2, cy - belly_h/2 + size*0.05, cx + belly_w/2, cy + belly_h/2 + size*0.05, fill="#fff", outline="")

        # Ojos
        eye_offset_x = body_w * 0.18
        eye_offset_y = -body_h * 0.15
        eye_r = size * 0.04
        c.create_oval(cx - eye_offset_x - eye_r, cy + eye_offset_y - eye_r, cx - eye_offset_x + eye_r, cy + eye_offset_y + eye_r, fill="#fff", outline="")
        c.create_oval(cx + eye_offset_x - eye_r, cy + eye_offset_y - eye_r, cx + eye_offset_x + eye_r, cy + eye_offset_y + eye_r, fill="#fff", outline="")
        pupil_r = eye_r * 0.45
        c.create_oval(cx - eye_offset_x - pupil_r, cy + eye_offset_y - pupil_r, cx - eye_offset_x + pupil_r, cy + eye_offset_y + pupil_r, fill="#000", outline="")
        c.create_oval(cx + eye_offset_x - pupil_r, cy + eye_offset_y - pupil_r, cx + eye_offset_x + pupil_r, cy + eye_offset_y + pupil_r, fill="#000", outline="")

        # Pico (triángulo naranja)
        beak_y = cy + size*0.02
        c.create_polygon(cx, beak_y - size*0.03, cx - size*0.04, beak_y + size*0.03, cx + size*0.04, beak_y + size*0.03, fill="#ff8c00", outline="")

        # Patas (óvalos naranja)
        foot_y = cy + body_h/2 - size*0.04
        foot_w = size * 0.12
        foot_h = size * 0.06
        c.create_oval(cx - body_w*0.25 - foot_w/2, foot_y, cx - body_w*0.25 + foot_w/2, foot_y + foot_h, fill="#ff8c00", outline="")
        c.create_oval(cx + body_w*0.25 - foot_w/2, foot_y, cx + body_w*0.25 + foot_w/2, foot_y + foot_h, fill="#ff8c00", outline="")

    # Intentar cargar `aa.png` desde el mismo directorio o desde profile_photos
    candidates = [
        os.path.join(os.path.dirname(__file__), 'aa.png'),
        os.path.join(os.path.dirname(__file__), 'profile_photos', 'aa.png'),
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'profile_photos', 'aa.png'),
    ]
    image_path = None
    for p in candidates:
        if os.path.exists(p):
            image_path = p
            break

    if image_path:
        try:
            if PIL_AVAILABLE:
                # Usar Pillow para abrir y redimensionar manteniendo aspecto
                pil_img = Image.open(image_path)
                # Calcular tamaño objetivo manteniendo aspecto
                max_dim = canvas_size - 8  # pequeño padding
                w, h = pil_img.size
                scale = min(max_dim / w, max_dim / h, 1.0)
                new_w = max(1, int(w * scale))
                new_h = max(1, int(h * scale))
                resized = pil_img.resize((new_w, new_h), Image.LANCZOS)
                tk_img = ImageTk.PhotoImage(resized)
                penguin_canvas.create_image(canvas_size/2, canvas_size/2, image=tk_img)
                penguin_canvas.image = tk_img
            else:
                # Fallback sin Pillow: intentar cargar con PhotoImage y usar subsample (enteros)
                img = tk.PhotoImage(file=image_path)
                w, h = img.width(), img.height()
                if w > canvas_size or h > canvas_size:
                    # factor entero aproximado para reducir tamaño
                    ratio = max(w / (canvas_size - 8), h / (canvas_size - 8))
                    factor = int(ratio) if ratio == int(ratio) else int(ratio) + 1
                    if factor < 1:
                        factor = 1
                    try:
                        img = img.subsample(factor, factor)
                    except Exception:
                        pass
                penguin_canvas.create_image(canvas_size/2, canvas_size/2, image=img)
                penguin_canvas.image = img
        except Exception:
            # Si algo sale mal al cargar la imagen, usar el dibujo como fallback
            draw_penguin(penguin_canvas, canvas_size)
    else:
        # Fallback: dibujar pingüino si no se encuentra archivo
        draw_penguin(penguin_canvas, canvas_size)

    # Botón inferior para redireccionar a app.py
    def open_app_py():
        app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'app.py'))
        subprocess.Popen([sys.executable, app_path], cwd=os.path.dirname(app_path))
        # No se cierra la ventana principal

    ttk.Button(frame, text="Entrar", style="Btn.TButton", command=open_app_py).pack(side="bottom", pady=32, ipadx=24, ipady=8)

    root.mainloop()

if __name__ == "__main__":
    main()
