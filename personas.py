# CRUD DE PERSONAS
# Create, Read, Update, Delete


import dearpygui.dearpygui as dpg
from myfunctions.myscreen import getPositionX
import sqlite3

# Configuración de la base de datos
DB_NAME = "mydatabase.db"

tiposdoc = [
    (1, 'DNI', 'Documento Nacional de Identidad'),
    (2, 'LC', 'Libreta Cívica'),
    (3, 'LE', 'Libreta de Enrolamiento'),
    (4, 'CI', 'Cédula de Identidad'),
    (5, 'PAS', 'Pasaporte')
]

defaultcbo = f"{tiposdoc[0][1]} - {tiposdoc[0][2]}"

def create_table():
    # Crea la tabla 'personas' en la base de datos si no existe.
    # Esta función inicializa la estructura necesaria para almacenar los datos de las personas.
    cnx = sqlite3.connect(DB_NAME)
    c = cnx.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS personas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    edad INTEGER NOT NULL
                )''')
    cnx.commit()
    cnx.close()


def add_persona(nombre, apellido, edad):
    # Añade una nueva persona a la base de datos.
    # Recibe nombre, apellido y edad como parámetros y los inserta en la tabla personas.
    # Debería validar que la persona no exista
    cnx = sqlite3.connect(DB_NAME)
    c = cnx.cursor()
    c.execute("INSERT INTO personas (nombre, apellido, edad) VALUES (?, ?, ?)",
              (nombre, apellido, edad))
    cnx.commit()
    cnx.close()


def get_personas():
    """Obtiene la lista de todas las personas almacenadas en la base de datos. Devuelve una lista de tuplas con los datos de cada persona."""

    cnx = sqlite3.connect(DB_NAME)
    c = cnx.cursor()
    c.execute("SELECT * FROM personas")
    personas = c.fetchall()
    cnx.close()
    return personas


def delete_persona(persona_id):
    # Elimina una persona de la base de datos según su ID.
    # Recibe el ID de la persona a eliminar.

    cnx = sqlite3.connect(DB_NAME)
    c = cnx.cursor()
    c.execute("DELETE FROM personas WHERE id = ?", (persona_id,))
    # Validar que realmente se elimino
    cnx.commit()
    cnx.close()


def update_persona(persona_id, nombre, apellido, edad):
    # Actualiza los datos de una persona existente en la base de datos.
    # Recibe el ID de la persona y los nuevos valores de nombre, apellido y edad.
    cnx = sqlite3.connect(DB_NAME)
    c = cnx.cursor()
    c.execute("UPDATE personas SET nombre = ?, apellido = ?, edad = ? WHERE id = ?",
              (nombre, apellido, edad, persona_id))
    cnx.commit()
    cnx.close()

def search_person(idsearch):
    # Busca y devuelve una persona por su ID. Retorna una tupla con los datos si la persona existe, o None si no se encuentra.
    cnx = sqlite3.connect(DB_NAME)
    c = cnx.cursor()
    c.execute("SELECT * FROM personas WHERE id = ?", (idsearch,))
    persona = c.fetchone()
    cnx.close()
    return persona

# Funciones de Alta de Personas

def create_view(sender, app_data):
    # Muestra la ventana para agregar una nueva persona.
    dpg.configure_item("add_person", show=True)

def update_view(sender, app_data):
    # Muestra la ventana para actualizar los datos de una persona.
    dpg.configure_item("update_person", show=True)

def delete_view(sender, app_data):
    # (A implementar) Muestra la ventana para eliminar una persona.
    pass

def add_record(sender, app_data):
    # Obtiene los datos ingresados en la interfaz y agrega una nueva persona a la base de datos.
    # Luego oculta la ventana de alta y actualiza la tabla de personas.
    add_persona(
            dpg.get_value("input_nombre"),
            dpg.get_value("input_apellido"),
            dpg.get_value("input_edad")
        )
    dpg.configure_item("add_person", show=False)
    update_table()

def update_record(sender, app_data):
    # Obtiene los datos modificados en la interfaz y actualiza la persona correspondiente en la base de datos.
    # Luego oculta la ventana de modificación y actualiza la tabla de personas.
    update_persona(
            dpg.get_value("input_id_up"),  # Deberia obtener el ID de la persona a modificar
            dpg.get_value("input_nombre_up"),
            dpg.get_value("input_apellido_up"),
            dpg.get_value("input_edad_up")
        )
    dpg.configure_item("update_person", show=False)
    update_table()


def search_record(sender, app_data):
    # Busca una persona por ID usando el valor ingresado en la interfaz.
    # Si la encuentra, carga sus datos en los campos de edición; si no, limpia los campos y muestra un mensaje.
    persona = search_person(dpg.get_value("input_id_up"))
    if persona:
        dpg.set_value("input_nombre_up", persona[1])
        dpg.set_value("input_apellido_up", persona[2])
        dpg.set_value("input_edad_up", persona[3])
    else:
        dpg.set_value("input_nombre_up", "")
        dpg.set_value("input_apellido_up", "")
        dpg.set_value("input_edad_up", "")
        # Esta salida deberia estar en un TEXT
        print("Persona no encontrada")

def update_table():
    # Actualiza la tabla visual de personas en la interfaz gráfica.
    # Elimina las filas existentes y carga los datos actuales desde la base de datos.
    # Limpiamos la tabla
    # Devuelve la cantidad de filas que tiene la tabla
    rows = dpg.get_item_children("table_personas", 1)

    # Si hay filas, las eliminamos
    print("Filas a eliminar:", rows)
    if rows:
        for row in rows:
            dpg.delete_item(row)

    # Cargamos los datos de las personas
    personas = get_personas()
    for persona in personas:
        with dpg.table_row(parent="table_personas"):
            dpg.add_text(str(persona[0]))
            dpg.add_text(persona[1])
            dpg.add_text(persona[2])
            dpg.add_text(str(persona[3]))

def main():
    # Función principal que inicializa la base de datos y configura la interfaz gráfica.
    # Crea las ventanas, botones y tablas necesarias para el CRUD de personas.
    create_table()
    # Marco de ejecucion de la aplicacion
    dpg.create_context()
    # Configuracion de la ventana principal
    dpg.create_viewport(
        title='Titulo de la ventana principal',
        width=600,
        height=400,
        min_width=400,
        min_height=400,
        x_pos=getPositionX(),
        resizable=False,
        small_icon="logo.png",
        large_icon="logo.png"
        )

    # Ventana que depende del marco de ejecucion
    with dpg.window(
        label="CRUD de Personas",
        no_close=True,
        width=dpg.get_viewport_width(),
        height=400,
        ):
        
        with dpg.menu_bar():
            with dpg.menu(label="Archivo"):
                dpg.add_menu_item(label="Nuevo", callback=lambda: print("Nuevo archivo"))
                dpg.add_menu_item(label="Abrir", callback=lambda: print("Abrir archivo"))
                dpg.add_separator()
                dpg.add_menu_item(label="Salir", callback=lambda: dpg.stop_dearpygui())
            
            with dpg.menu(label="Operaciones"):
                dpg.add_menu_item(label="Alta", callback=lambda: print("Nueva Alta"), user_data="Alta")
                dpg.add_menu_item(label="Baja", callback=lambda: print("Nueva Baja"), user_data="Baja")
                dpg.add_menu_item(label="Modificación", callback=lambda: print("Nueva Modificacion"), user_data="Modificación")
            
            with dpg.menu(label="Ver"):
                dpg.add_menu_item(label="Actualizar Tabla", callback=lambda: update_table())
            
            with dpg.menu(label="Ayuda"):
                dpg.add_menu_item(label="Acerca de", callback=lambda: print("Gestor de Personas v1.0"))
                dpg.add_menu_item(label="Manual", callback=lambda: print("Seleccione una operación del menú"))
                
        with dpg.group(horizontal=True):
            dpg.add_button(label="Alta de Persona", callback=create_view)
            dpg.add_button(label="Baja de Persona", callback=delete_view)
            dpg.add_button(label="Modificar Persona", callback=update_view)   

        # Mostramos los datos de las personas que tenemos cargadas
        with dpg.table(header_row=True, resizable=True, borders_innerH=True, borders_outerH=True, tag="table_personas"):
            dpg.add_table_column(label="ID")
            dpg.add_table_column(label="Nombre")
            dpg.add_table_column(label="Apellido")
            dpg.add_table_column(label="Edad")
            
        # Con los Options Button o Ratio Button
        dpg.add_text("Tipo de Documento:")
        for tipo in tiposdoc:
            dpg.add_radio_button([f"{tipo[1]} - {tipo[2]}"], tag=f"radio_{tipo[0]}", callback=lambda: print("Tipo Doc"))
            
        # Con el Combo Box
        dpg.add_text("Tipo de Documento (Combo):")
        
        
        # Dependiendo de se genere la lista de valores del combo se necesita crear una lista 
        # aparte como el caso 1 o sino una variable aparte como el caso 2

        # Caso 1: Crear una lista aparte
        listdetipo = []
        for tipo in tiposdoc:
            listdetipo.append(f"{tipo[1]} - {tipo[2]}")
        print(listdetipo)
        dpg.add_combo(listdetipo, label="Tipo de Documento", tag="tipo_doc_combo", 
                                 width=250, default_value=listdetipo[0],
                                 callback=lambda: print(f"Tipo Doc Combo {dpg.get_value("tipo_doc_combo")}"))
        
        # Caso 2: Crear una variable aparte
        dpg.add_combo([f"{tipo[1]} - {tipo[2]}" for tipo in tiposdoc], tag="combo_tiposdoc", default_value=defaultcbo, callback=lambda: print(dpg.get_value("combo_tiposdoc")))
        
    with dpg.window(
        label="Agregar Persona",
        tag="add_person",
        width=int(dpg.get_viewport_width()/2),
        height=200,
        pos=(int(dpg.get_viewport_width()/2), 10),
        show=False,  # Esta ventana no se muestra inicialmente
        ):
        with dpg.group(horizontal=True):
            dpg.add_text("Nombre:")
            dpg.add_input_text(tag="input_nombre", label="")
        with dpg.group(horizontal=True):
            dpg.add_text("Apellido:")
            dpg.add_input_text(tag="input_apellido", label="")
        with dpg.group(horizontal=True):
            dpg.add_text("Edad:")
            dpg.add_input_text(tag="input_edad", label="")
        
        dpg.add_button(label="Guardar", callback=add_record)

    with dpg.window(
        label="Actualizar Persona",
        tag="update_person",
        width=int(dpg.get_viewport_width()/2),
        height=200,
        pos=(int(dpg.get_viewport_width()/2), 10),
        show=False,  # Esta ventana no se muestra inicialmente
        ):
        with dpg.group(horizontal=True):
            dpg.add_text("Indique el ID:")
            dpg.add_input_text(tag="input_id_up", label="")
        dpg.add_button(label="Buscar", callback=search_record)
        with dpg.group(horizontal=True):
            dpg.add_text("Nombre:")
            dpg.add_input_text(tag="input_nombre_up", label="")
        with dpg.group(horizontal=True):
            dpg.add_text("Apellido:")
            dpg.add_input_text(tag="input_apellido_up", label="")
        with dpg.group(horizontal=True):
            dpg.add_text("Edad:")
            dpg.add_input_text(tag="input_edad_up", label="")
        
        dpg.add_button(label="Guardar", callback=update_record)


    # Mostrar la ventana, definir el loop de ejecucion 
    dpg.setup_dearpygui()
    dpg.show_viewport()
    update_table()
    dpg.start_dearpygui()

    # Destruir el marco de ejecucion
    dpg.destroy_context()

if __name__ == "__main__":
    main()