# Documentación del Proyecto - Aplicación Demo con Tkinter

## Descripción General
Este proyecto es un **MVP (Producto Mínimo Viable)** desarrollado con **Python** y la librería **Tkinter** para crear interfaces gráficas de usuario (GUI).  
La aplicación presenta una ventana principal desde la cual se accede a diferentes módulos demostrativos:

1. **Home / Bienvenida**
2. **Formulario con validación y guardado en archivo**
3. **Lista con operaciones CRUD básicas**
4. **Tabla usando Treeview y datos CSV**
5. **Canvas para gráficos y dibujos**

El objetivo del proyecto es servir como ejemplo de integración de distintos elementos de Tkinter en un mismo entorno.

---

## Estructura del Proyecto

```
proyecto/
│
├── main.py               # Ventana principal de la aplicación
├── app/
│   ├── win_home.py       # Ventana de bienvenida
│   ├── win_form.py       # Ventana de formulario con validaciones
│   ├── win_list.py       # Ventana de lista con CRUD básico
│   ├── win_table.py      # Ventana de tabla con Treeview y CSV
│   ├── win_canvas.py     # Ventana de canvas con dibujos
│
└── data/
    └── sample.csv        # Archivo CSV de ejemplo para la tabla
```

---

## Archivos y Funcionalidad

### 1. `main.py`
- Crea la ventana principal de la aplicación.
- Define botones para abrir cada uno de los módulos.
- Configura la geometría y el estilo básico de la interfaz.
- Contiene la función principal `main()` y ejecuta el `mainloop()`.

### 2. `win_home.py`
- Ventana de bienvenida con mensajes iniciales.
- Permite mostrar un `messagebox` con información.
- Incluye botón para cerrar la ventana.

### 3. `win_form.py`
- Ventana de formulario con dos campos: **Nombre** y **Edad**.
- Validación de datos:
  - Nombre obligatorio.
  - Edad debe ser un número entero.
- Opción para guardar los datos en un archivo `.txt` usando `filedialog`.
- Uso de `messagebox` para retroalimentación al usuario.

### 4. `win_list.py`
- Ventana con un `Listbox` que implementa un CRUD básico:
  - **Agregar**: Inserta un nuevo elemento en la lista.
  - **Eliminar seleccionado**: Borra un elemento específico.
  - **Limpiar**: Elimina todos los elementos.
- Incluye validaciones simples (p. ej. no agregar vacío).
- Dispone de botón para cerrar la ventana.

### 5. `win_table.py`
- Ventana con un `Treeview` para mostrar datos tabulares.
- Lee información desde un archivo CSV (`sample.csv` en `data/`).
- Si no encuentra el archivo, muestra una advertencia al usuario.
- Presenta columnas **nombre**, **valor1** y **valor2**.

Ejemplo de archivo `sample.csv`:
```csv
nombre,valor1,valor2
A,10,20
B,15,25
C,12,30
```

### 6. `win_canvas.py`
- Ventana con un **Canvas** donde se dibujan figuras gráficas:
  - Rectángulo.
  - Óvalo.
  - Línea.
  - Texto.
- Ejemplo visual para mostrar el uso de `Canvas` en Tkinter.

---

## Tecnologías Utilizadas
- **Python 3.x**
- **Tkinter** (interfaz gráfica estándar de Python)
- **ttk** (temas y widgets mejorados para Tkinter)
- **csv y pathlib** (manejo de archivos en la tabla)
- **messagebox y filedialog** (interacción con el usuario)

---

## Ejecución del Proyecto
1. Clonar o descargar el proyecto.
2. Asegurarse de tener **Python 3.x** instalado.
3. Ejecutar el archivo principal:

```bash
python main.py
```

4. Desde la ventana principal, se podrá acceder a las distintas funcionalidades.

---

## Futuras Mejoras
- Agregar persistencia de datos más robusta (ej. SQLite en vez de CSV/txt).
- Mejorar la estética con librerías de estilos (ej. `ttkbootstrap`).
- Implementar pruebas automatizadas para validación de funciones.
- Soporte multi-idioma.

---

## Autor
Desarrollado como un **ejemplo educativo** de integración con Tkinter.  
