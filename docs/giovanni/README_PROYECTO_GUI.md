# Documentación del Proyecto Python GUI

Este proyecto parece ser una aplicación gráfica basada en `tkinter` para la manipulación visual de objetos y datos mediante ventanas especializadas como formularios, listas, tablas y un canvas interactivo.

## Archivos del Proyecto

### main.py

Archivo principal que lanza la aplicación. Importa `win_home` y ejecuta la función `main()` desde allí.

### win_canvas.py

Ventana que utiliza `Canvas` de `tkinter` para permitir al usuario dibujar líneas en tiempo real con el mouse. Es una funcionalidad visual/interactiva.

### win_form.py

Define una ventana con un formulario de entrada donde se pueden introducir datos como nombre, edad y correo. Al presionar el botón 'Guardar', los datos se imprimen en consola. Ideal como entrada de datos estructurados.

### win_home.py

Contiene la ventana principal de la aplicación. Presenta un menú con botones que permiten acceder a otras ventanas: formulario (`win_form`), lista (`win_list`), tabla (`win_table`) y canvas (`win_canvas`). Usa `tkinter` como framework gráfico.

### win_list.py

Muestra una ventana con una lista (`Listbox`) de elementos. Se puede seleccionar un elemento y mostrarlo mediante un botón.

### win_table.py

Muestra una ventana que simula una tabla con `Treeview` de `ttk`, con columnas como ID, Nombre y Edad. Se pueden insertar datos ficticios.

### Dependencias

Este proyecto utiliza únicamente la biblioteca estándar de Python, en particular el módulo `tkinter`. No se requieren librerías externas para su ejecución.

### Ejecución

Para ejecutar la aplicación, simplemente ejecuta el archivo `main.py`:

```bash
python main.py
```

Esto abrirá la ventana principal desde donde puedes navegar a las otras vistas.

### Estructura General

```
📦 Proyecto GUI
 ┣ 📄 main.py           # Punto de entrada
 ┣ 📄 win_home.py       # Ventana principal (Home)
 ┣ 📄 win_form.py       # Formulario de entrada
 ┣ 📄 win_list.py       # Lista de elementos
 ┣ 📄 win_table.py      # Tabla con datos
 ┗ 📄 win_canvas.py     # Canvas para dibujo interactivo
```

