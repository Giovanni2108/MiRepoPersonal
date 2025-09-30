# Documentación del Proyecto: Aplicación Demo con Tkinter

## Descripción General
Este proyecto es una aplicación de escritorio desarrollada en **Python** utilizando la librería **Tkinter**.  
El objetivo es demostrar diferentes componentes gráficos como ventanas, formularios, listas, tablas y canvas.  
Funciona como un **MVP (Minimum Viable Product)** para aprender y mostrar funcionalidades básicas de interfaces gráficas.

La aplicación principal abre un menú con botones que permiten navegar hacia diferentes módulos/ventanas.

---

## Estructura del Proyecto
```
/src/app/
    main.py
    win_home.py
    win_form.py
    win_list.py
    win_table.py
    win_canvas.py
/data/
    sample.csv
```

---

## Archivos y Funcionalidad

### 1. `main.py`
- Es el punto de entrada de la aplicación.
- Crea la ventana principal (`root`) con título y tamaño fijo.
- Contiene botones que abren otras ventanas:
  1. **Home** → `win_home.py`
  2. **Formulario** → `win_form.py`
  3. **Lista (CRUD)** → `win_list.py`
  4. **Tabla (Treeview)** → `win_table.py`
  5. **Canvas (Dibujo)** → `win_canvas.py`
- También tiene un botón de salida para cerrar la aplicación.

### 2. `win_home.py`
- Ventana de bienvenida con un mensaje.
- Botón que muestra un cuadro de diálogo (`messagebox.showinfo`).
- Botón para cerrar la ventana.

### 3. `win_form.py`
- Implementa un formulario con dos campos: **Nombre** y **Edad**.
- Valida que:
  - El nombre no esté vacío.
  - La edad sea un número entero.
- Permite guardar los datos en un archivo `.txt` usando `filedialog.asksaveasfilename`.
- Muestra mensajes de error o confirmación con `messagebox`.
- Incluye botón para cerrar la ventana.

### 4. `win_list.py`
- Ventana con una **Listbox** para simular operaciones CRUD básicas.
- Funcionalidades:
  - **Agregar** un ítem escrito en un campo de texto.
  - **Eliminar** un ítem seleccionado.
  - **Limpiar** todos los ítems de la lista.
- Incluye botón para cerrar.

### 5. `win_table.py`
- Muestra una tabla usando **Treeview** con tres columnas (`nombre`, `valor1`, `valor2`).
- Carga datos desde el archivo CSV `/data/sample.csv`.
- Si el archivo no existe, muestra una advertencia con `messagebox`.
- Incluye botón para cerrar.

### 6. `win_canvas.py`
- Ventana con un **Canvas** para dibujar figuras básicas.
- Ejemplos incluidos:
  - Rectángulo.
  - Óvalo con color de relleno.
  - Línea.
  - Texto centrado.
- Incluye botón para cerrar.

### 7. `data/sample.csv`
- Archivo de ejemplo que contiene datos en formato CSV:
  ```csv
  nombre,valor1,valor2
  A,10,20
  B,15,25
  C,12,30
  ```
- Es usado en `win_table.py` para poblar la tabla.

---

## Requisitos del Proyecto
- **Python 3.8+**
- Librerías estándar: `tkinter`, `csv`, `pathlib`.

No requiere instalación de librerías externas.

---

## Ejecución del Proyecto
1. Clonar o descargar el repositorio.
2. Asegurarse de que existe el archivo `data/sample.csv`.
3. Ejecutar el archivo principal:
   ```bash
   python src/app/main.py
   ```
4. Desde la ventana principal, navegar entre los distintos módulos.

---

## Posibles Mejoras Futuras
- Guardar y cargar datos dinámicamente desde la lista (CRUD completo).
- Validar datos más robustamente en el formulario.
- Agregar más dibujos y funcionalidades interactivas en el canvas.
- Implementar un menú de navegación en la parte superior en lugar de botones.

---

## Autor
Proyecto creado como demostración de **Tkinter** para un **MVP educativo**.
