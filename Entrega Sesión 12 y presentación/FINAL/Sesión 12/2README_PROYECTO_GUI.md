# 🖥️ Documentación del Proyecto GUI en Tkinter

Este proyecto es una aplicación gráfica desarrollada en Python utilizando la biblioteca estándar `tkinter`. Su objetivo es mostrar diferentes tipos de interfaces gráficas como formularios, listas, tablas y un canvas interactivo, todo gestionado desde una ventana principal.

## 📁 Archivos del Proyecto

### main.py

Este archivo es el **punto de entrada** del programa.

- Importa la función `main()` desde `win_home.py`.
- Al ejecutarlo, se lanza la ventana principal de la aplicación.

```python
from win_home import main

main()
```

### win_home.py

Contiene la **ventana principal** de la aplicación. Desde aquí se puede acceder a las demás secciones:

- 📄 Formulario (`win_form`)
- 📋 Lista (`win_list`)
- 📊 Tabla (`win_table`)
- 🎨 Canvas para dibujar (`win_canvas`)

Cada opción abre una nueva ventana. Está diseñado con `tkinter.Tk()` y botones de navegación.

### win_form.py

Implementa un **formulario de entrada de datos**:

- Campos: Nombre, Edad y Correo.
- Botón de "Guardar" que imprime los datos en consola.
- Usa `tkinter.Entry` y `tkinter.Label`.

Ideal para la simulación de formularios de registro o contacto.

### win_list.py

Ventana con una **lista interactiva** (`Listbox`):

- Lista de elementos predefinidos.
- Botón para mostrar el ítem seleccionado.

Útil para mostrar y seleccionar opciones.

### win_table.py

Crea una ventana con una **tabla estilo Excel** usando `ttk.Treeview`:

- Columnas: ID, Nombre y Edad.
- Datos de prueba insertados al abrirse.

Permite visualizar datos en formato tabular profesional.

### win_canvas.py

Ventana que abre un **canvas interactivo** para dibujar líneas con el mouse.

- Se dibujan trazos mientras se mantiene presionado el botón izquierdo del mouse.
- Implementado con eventos `<B1-Motion>` y `Canvas.create_line`.

Ideal para pruebas gráficas y funcionalidades artísticas simples.

### 🧩 Dependencias

Este proyecto utiliza exclusivamente **librerías estándar de Python**.

- No necesitas instalar paquetes externos.
- Principalmente usa: `tkinter`, `ttk`, `messagebox`.

Es compatible con cualquier instalación moderna de Python (3.6+).

### 🚀 Cómo ejecutar la aplicación

Para iniciar la aplicación:

```bash
python main.py
```

Esto abrirá la ventana principal donde podrás navegar a las demás funciones.

### 📌 Estructura del Proyecto

```
📦 GUI Project
 ┣ 📄 main.py           # Entrada del programa
 ┣ 📄 win_home.py       # Ventana principal
 ┣ 📄 win_form.py       # Formulario con campos de texto
 ┣ 📄 win_list.py       # Lista de selección
 ┣ 📄 win_table.py      # Tabla con Treeview
 ┗ 📄 win_canvas.py     # Dibujo interactivo en canvas
```

