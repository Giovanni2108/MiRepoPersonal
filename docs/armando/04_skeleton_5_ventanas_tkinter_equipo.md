# Documentación del Proyecto – Sesión 3  
**Esqueleto con 5 ventanas tkinter y navegación desde la ventana principal**  

---

## 🎯 Objetivo  
Construir un **esqueleto mínimo viable** en Python usando **tkinter**, con una ventana principal y 5 subventanas integradas, cada una realizada por un integrante del equipo. La aplicación se ejecuta desde Visual Studio Code con configuración de depuración (`launch.json`).  

---

## 📂 Estructura del proyecto  
```
/data
  sample.csv
/src
  /app
    main.py
    win_home.py
    win_form.py
    win_list.py
    win_table.py
    win_canvas.py
  /core
    helpers.py
/.vscode
  launch.json
/docs
  04_skeleton_5_ventanas_tkinter_equipo.md
README.md
```

---

## 📝 Análisis de archivos  

### `main.py` — Ventana principal  
Este archivo es el **punto de entrada** de la aplicación.  
- Crea la ventana principal (`Tk()`).  
- Contiene botones que permiten abrir cada subventana:  
  1. Home / Bienvenida  
  2. Formulario  
  3. Lista (CRUD básico)  
  4. Tabla (Treeview)  
  5. Canvas (Dibujo)  
- Incluye un botón **Salir** para cerrar la aplicación.  

> **Rol:** Coordina la navegación entre todas las ventanas del proyecto.  

---

### `win_home.py` — Ventana 1 (Home / Bienvenida)  
- Muestra un mensaje de bienvenida con `Label`.  
- Incluye un botón que dispara un `messagebox.showinfo`.  
- Tiene botón para cerrar la ventana.  

> **Rol:** Pantalla de inicio, primera interacción con el usuario.  

---

### `win_form.py` — Ventana 2 (Formulario con validación)  
- Permite ingresar **nombre** y **edad** en `Entry`.  
- Validaciones implementadas:  
  - El nombre no puede estar vacío.  
  - La edad debe ser un número entero (`isdigit`).  
- Si los datos son válidos, se guardan en un archivo `.txt` seleccionado con `filedialog.asksaveasfilename`.  
- Se usan `messagebox` para mostrar mensajes de error o éxito.  

> **Rol:** Ejemplo de captura de datos y persistencia en archivo.  

---

### `win_list.py` — Ventana 3 (Listbox con CRUD básico)  
- Implementa un `Listbox` para mostrar elementos.  
- Operaciones disponibles:  
  - **Agregar**: inserta el texto de un `Entry`.  
  - **Eliminar seleccionado**: borra el ítem resaltado.  
  - **Limpiar**: vacía toda la lista.  
- Previene agregar valores vacíos con un `messagebox.showwarning`.  

> **Rol:** Ejemplo de manejo de listas dinámicas en memoria.  

---

### `win_table.py` — Ventana 4 (Tabla con Treeview)  
- Usa un `ttk.Treeview` con columnas: `nombre`, `valor1`, `valor2`.  
- Los datos provienen del archivo CSV `data/sample.csv`.  
- Si el archivo no existe, muestra un aviso con `messagebox.showwarning`.  
- Ejemplo de cómo mostrar información tabular en tkinter.  

#### `sample.csv`  
```csv
nombre,valor1,valor2
A,10,20
B,15,25
C,12,30
```

> **Rol:** Ejemplo de integración de datos externos (CSV) en la UI.  

---

### `win_canvas.py` — Ventana 5 (Canvas de dibujo básico)  
- Muestra un área de dibujo (`Canvas`).  
- Incluye ejemplos:  
  - Rectángulo.  
  - Óvalo.  
  - Línea.  
  - Texto con fuente personalizada.  
- Sirve como introducción a gráficos en tkinter.  

> **Rol:** Ejemplo de renderizado gráfico y uso de coordenadas.  

---

### `.vscode/launch.json` — Configuración de ejecución  
- Permite depurar la aplicación en **VS Code**.  
- Especifica que el programa a ejecutar es `src/app/main.py`.  
- Ajusta `cwd` y `PYTHONPATH` para que funcionen las rutas relativas.  
- Usa la terminal integrada (`integratedTerminal`).  

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Programa con PYTHONPATH=src",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/src/app/main.py",
      "cwd": "${workspaceFolder}",
      "env": { "PYTHONPATH": "${workspaceFolder}/src" },
      "console": "integratedTerminal",
      "justMyCode": true
    }
  ]
}
```

---

## 📸 Evidencias sugeridas  
Se recomienda incluir capturas de pantalla de:  
1. La ventana principal.  
2. Cada una de las 5 subventanas.  

---

## ✅ Conclusión  
El proyecto demuestra:  
- **Modularidad:** cada ventana en su propio archivo.  
- **Integración:** todas conectadas a través de la ventana principal.  
- **Validación y persistencia:** manejo de entradas de usuario y guardado en archivo.  
- **CRUD básico:** manipulación de listas dinámicas.  
- **Datos externos:** lectura y despliegue de CSV en tabla.  
- **Gráficos:** uso de `Canvas` para dibujo básico.  
- **Depuración profesional:** configuración con `launch.json` en VS Code.  

Este esqueleto constituye la base para agregar funcionalidades más avanzadas y trabajar de manera colaborativa en equipo.  
