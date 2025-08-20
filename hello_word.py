import dearpygui.dearpygui as dpg
from myfunctions.myscreen import getPositionX

from myfunctions import test_function

def click_button(sender, app_data):
    print("Button clicked!", sender)
    dpg.set_value("text_2", value="Nuevo texto para la ventana 2")
    dpg.set_value("input_text_2", value="Nuevo texto para el input")
    print("Cambio realizado en:", dpg.get_item_label("text_2"))

def abrir_ventana2(sender, app_data):
    dpg.configure_item("example_window_2", show=True)

# Marco de ejecucion de la aplicacion
dpg.create_context()
# Configuracion de la ventana principal
dpg.create_viewport(
    title='Titulo de la ventana principal', 
    width=600, 
    height=300, 
    min_width=400,
    min_height=200,
    x_pos=getPositionX(),
    )

# Ventana que depende del marco de ejecucion
with dpg.window(
    label="Example Window", 
    no_close=True,
    width=int(dpg.get_viewport_width()/2),
    height=200,
    ):
    dpg.add_text("Hello, world")
    dpg.add_button(label="Cambia el Texto del Label y del Input", callback=click_button)
    dpg.add_button(label="Abrir ventana 2", callback=abrir_ventana2)

with dpg.window(
    label="Example Window", 
    no_close=True,
    tag="example_window_2",
    width=int(dpg.get_viewport_width()/2),
    height=200,
    pos=(int(dpg.get_viewport_width()/2), 10),
    show=False,  # Esta ventana no se muestra inicialmente
    ):
    dpg.add_text("Hello, world")
    dpg.add_text(tag="text_2", default_value="Texto de la ventana 2")
    dpg.add_input_text(tag="input_text_2", label="")


# Mostrar la ventana, definir el loop de ejecucion 
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()

# Destruir el marco de ejecucion
dpg.destroy_context()