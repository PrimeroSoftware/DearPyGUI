# DearPyGUI

DearPyGUI entorno para desarrollo de App en Python para Desktop

[Documentacion](https://dearpygui.readthedocs.io/en/latest/index.html# "Docu")

## **1. Introducción a Dear PyGui**

🔹 **¿Qué es?**

* Biblioteca GUI rápida y moderna para Python.
* Orientada a aplicaciones con alto rendimiento.
* Alternativa a Tkinter, PyQt y Kivy.

🔹 **Ventajas:**
✔️ Fácil de aprender
✔️ Renderizado GPU (rápido)
✔️ Temas personalizables
✔️ Soporte para gráficos y visualización

🔹 **Casos de uso:**

* Herramientas internas
* Paneles de control
* Visualización de datos
* Prototipado rápido

## **2. Instalación y Configuración**

```
pip install dearpygui
```

Verificación:

```
import dearpygui.dearpygui as dpg
print("Versión:", dpg.get_version())  # Debe mostrar la versión instalada
```

## **3. Estructura Básica de un Programa**

```
import dearpygui.dearpygui as dpg

# 1. Crear contexto y ventana
dpg.create_context()
dpg.create_viewport(title="Mi App", width=600, height=400)

# 2. Añadir widgets dentro de una ventana
with dpg.window(label="Ventana Principal"):
    dpg.add_text("¡Hola, mundo!")
    dpg.add_button(label="Click aquí", callback=lambda: print("Botón presionado"))

# 3. Iniciar la aplicación
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()  # Limpiar al finalizar
```

## **4. Widgets Básicos**

| **Widget**       | **Descripción**        | **Ejemplo**                                    |
| ---------------------- | ----------------------------- | ---------------------------------------------------- |
| `add_text()`         | Muestra texto                 | `dpg.add_text("Hola")`                             |
| `add_button()`       | Botón clickeable             | `dpg.add_button("Aceptar", callback=func)`         |
| `add_input_text()`   | Campo de texto editable       | `dpg.add_input_text("Nombre")`                     |
| `add_slider_int()`   | Control deslizante (números) | `dpg.add_slider_int("Edad", 0, 100)`               |
| `add_checkbox()`     | Casilla de verificación      | `dpg.add_checkbox("Acepto términos")`             |
| `add_radio_button()` | Botones de opción única     | `dpg.add_radio_button(["Opción 1", "Opción 2"])` |

## **5. Diseño y Organización**

🔹 **Agrupar elementos:**

```
with dpg.group(horizontal=True):  # Organiza en fila
    dpg.add_button("Botón 1")
    dpg.add_button("Botón 2")
```

🔹 **Pestañas:**

```
with dpg.tab_bar():
    with dpg.tab(label="Pestaña 1"):
        dpg.add_text("Contenido 1")
    with dpg.tab(label="Pestaña 2"):
        dpg.add_text("Contenido 2")
```

## **6. Manejo de Eventos (Callbacks)**

```
def mi_callback(sender, app_data, user_data):
    print(f"Botón {sender} presionado")
    print(f"Datos extra: {user_data}")

dpg.add_button(
    label="Presionar",
    callback=mi_callback,
    user_data="Información adicional"
)
```

## **7. Temas y Estilos**

```
with dpg.theme() as mi_tema:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 0, 0))  # Botón rojo
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10)    # Bordes redondeados

dpg.bind_item_theme("mi_boton", mi_tema)  # Aplicar tema a un widget
```
