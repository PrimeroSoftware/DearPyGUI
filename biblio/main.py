import dearpygui.dearpygui as dpg
from lib.myfunctions.myscreen import getPositionX

def main():
    # Crear el contexto de DearPyGUI
    dpg.create_context()
    
    # Configurar el viewport (ventana principal)
    dpg.create_viewport(
        title='Aplicación DearPyGUI',
        width=800,
        height=600,
        min_width=400,
        min_height=300,
        x_pos=getPositionX(),
        resizable=True,
        small_icon="logo.png",
        large_icon="logo.png"
    )
    
    # Crear la ventana principal
    with dpg.window(
        label="Ventana Principal",
        no_close=True,
        width=dpg.get_viewport_width(),
        height=dpg.get_viewport_height(),
        tag="main_window"
    ):
        dpg.add_text("¡Bienvenido a DearPyGUI!")
        dpg.add_separator()
        
        with dpg.group(horizontal=True):
            dpg.add_button(label="Botón 1", callback=lambda: print("Botón 1 presionado"))
            dpg.add_button(label="Botón 2", callback=lambda: print("Botón 2 presionado"))
        
        dpg.add_separator()
        dpg.add_text("Área de contenido:")
        
        # Agregar más elementos aquí según sea necesario
    
    # Configurar y mostrar la aplicación
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    
    # Limpiar recursos al cerrar
    dpg.destroy_context()

if __name__ == "__main__":
    main()
