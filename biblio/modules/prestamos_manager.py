# prestamos_manager.py - Módulo para la gestión de préstamos

import dearpygui.dearpygui as dpg
from .database_manager import DatabaseManager
from .libros_manager import LibrosManager
from . import sqlstatement as sql
from datetime import datetime, date

class PrestamosManager(DatabaseManager):
    """Clase para manejar todas las operaciones relacionadas con préstamos"""
    
    def __init__(self, db_name="biblioteca.db"):
        super().__init__(db_name)
        self.libros_manager = LibrosManager(db_name)
    
    # ================================
    # OPERACIONES CRUD - PRÉSTAMOS
    # ================================
    
    def registrar_prestamo(self, sender=None, app_data=None):
        """Registrar un nuevo préstamo"""
        isbn = dpg.get_value("input_prestamo_isbn")
        nombre_usuario = dpg.get_value("input_prestamo_usuario")
        
        if not isbn or not nombre_usuario:
            self._set_status("Error: ISBN y nombre de usuario son obligatorios")
            return
        
        # Verificar que el libro existe y está disponible
        libros_disponibles = self.execute_query(sql.CHECK_LIBRO_DISPONIBLE, (isbn,))
        
        if not libros_disponibles:
            self._set_status("Error: El libro no existe o no está disponible")
            return
        
        try:
            fecha_prestamo = datetime.now().strftime('%Y-%m-%d')
            
            # Registrar préstamo
            rows_affected = self.execute_command(
                sql.INSERT_PRESTAMO, 
                (isbn, nombre_usuario, fecha_prestamo)
            )
            
            if rows_affected > 0:
                # Cambiar estado del libro a "Prestado"
                self.libros_manager.cambiar_estado_libro(isbn, "Prestado")
                
                # Limpiar campos
                dpg.set_value("input_prestamo_isbn", "")
                dpg.set_value("input_prestamo_usuario", "")
                
                self._set_status(f"Préstamo registrado exitosamente para '{nombre_usuario}'")
                self.cargar_prestamos()
                
                # Notificar a otros módulos si es necesario
                if hasattr(self, 'on_prestamo_added'):
                    self.on_prestamo_added()
            else:
                self._set_status("Error al registrar préstamo")
                
        except Exception as e:
            self._set_status(f"Error al registrar préstamo: {e}")
    
    def cargar_prestamos(self, sender=None, app_data=None):
        """Cargar la lista de préstamos activos en la tabla"""
        print("📥 Cargando préstamos...")
        
        try:
            # Verificar que la tabla existe
            if not dpg.does_item_exist("table_prestamos"):
                print("❌ ERROR: table_prestamos no existe!")
                self._set_status("Error: Tabla no disponible")
                return
            
            # Obtener préstamos con información de libros
            prestamos = self.execute_query(sql.SELECT_PRESTAMOS_WITH_BOOKS)
            
            print(f"📊 Encontrados {len(prestamos)} préstamos en la BD")
            
            # Limpiar solo las filas de datos, preservando las columnas (igual que autores)
            # Primero obtenemos todos los hijos de la tabla
            children = dpg.get_item_children("table_prestamos", slot=1)  # slot 1 contiene las filas
            if children:
                for child in children:
                    if dpg.get_item_type(child) == "mvAppItemType::mvTableRow":
                        dpg.delete_item(child)
            
            # Agregar datos (sin encabezados, ya están definidos en las columnas)
            for prestamo in prestamos:
                with dpg.table_row(parent="table_prestamos"):
                    dpg.add_text(str(prestamo[0]))  # id_prestamo
                    dpg.add_text(prestamo[1])  # isbn_libro
                    dpg.add_text(prestamo[6] or "Sin título")  # titulo
                    dpg.add_text(prestamo[2])  # nombre_usuario
                    dpg.add_text(prestamo[3] or "")  # fecha_prestamo
                    dpg.add_text(prestamo[4] or "Pendiente")  # fecha_devolucion
                    with dpg.group(horizontal=True):
                        if not prestamo[4]:  # Si no hay fecha de devolución
                            dpg.add_button(
                                label=f"Devolver##dev_prestamo_{prestamo[0]}", 
                                callback=self.devolver_libro,
                                user_data=(prestamo[0], prestamo[1]),
                                width=80
                            )
                        else:
                            dpg.add_text("Devuelto", color=(0, 255, 0))
            
            print(f"✅ Cargados {len(prestamos)} préstamos correctamente")
            self._set_status(f"Cargados {len(prestamos)} préstamos")
                        
        except Exception as e:
            print(f"❌ Error al cargar préstamos: {e}")
            self._set_status(f"Error: {e}")
    
    def devolver_libro(self, sender=None, app_data=None, user_data=None):
        """Registrar la devolución de un libro"""
        # Manejar diferentes formas de llamar al método
        if user_data is not None:
            if isinstance(user_data, tuple):
                id_prestamo, isbn_libro = user_data
            else:
                id_prestamo = user_data
                isbn_libro = app_data
        else:
            # Llamada directa con parámetros (para compatibilidad)
            id_prestamo = sender
            isbn_libro = app_data
        
        try:
            fecha_devolucion = datetime.now().strftime('%Y-%m-%d')
            
            # Actualizar el préstamo con fecha de devolución
            rows_affected = self.execute_command(
                sql.UPDATE_PRESTAMO_DEVOLUCION, 
                (fecha_devolucion, id_prestamo)
            )
            
            # En SQLite, rowcount puede ser -1 para UPDATE, así que verificamos de otra manera
            # Verificar que la actualización fue exitosa consultando el registro
            prestamo_actualizado = self.execute_query(
                "SELECT fecha_devolucion FROM prestamos WHERE id = ?", 
                (id_prestamo,)
            )
            
            if prestamo_actualizado and prestamo_actualizado[0][0] == fecha_devolucion:
                # Cambiar estado del libro a "Disponible"
                self.libros_manager.cambiar_estado_libro(isbn_libro, "Disponible")
                
                self._set_status("Libro devuelto exitosamente")
                self.cargar_prestamos()
                
                # Notificar a otros módulos si es necesario
                if hasattr(self, 'on_prestamo_returned'):
                    self.on_prestamo_returned()
            else:
                self._set_status("Error: No se pudo registrar la devolución")
            
        except Exception as e:
            self._set_status(f"Error al devolver libro: {e}")
    
    def cargar_historial_prestamos(self, sender=None, app_data=None):
        """Cargar el historial completo de préstamos"""
        print("📥 Cargando historial de préstamos...")
        
        try:
            # Verificar cuál tabla usar (main.py usa "table_historial", ventana separada usa "table_historial_prestamos")
            table_tag = "table_historial" if dpg.does_item_exist("table_historial") else "table_historial_prestamos"
            
            if not dpg.does_item_exist(table_tag):
                print(f"❌ ERROR: {table_tag} no existe!")
                self._set_status("Error: Tabla no disponible")
                return
            
            # Obtener historial completo
            prestamos = self.execute_query(sql.SELECT_HISTORIAL_PRESTAMOS)
            
            print(f"📊 Encontrados {len(prestamos)} préstamos en el historial")
            
            # Limpiar solo las filas de datos, preservando las columnas (igual que autores)
            # Primero obtenemos todos los hijos de la tabla
            children = dpg.get_item_children(table_tag, slot=1)  # slot 1 contiene las filas
            if children:
                for child in children:
                    if dpg.get_item_type(child) == "mvAppItemType::mvTableRow":
                        dpg.delete_item(child)
            
            # Agregar datos (sin encabezados, ya están definidos en las columnas)
            for prestamo in prestamos:
                with dpg.table_row(parent=table_tag):
                    dpg.add_text(str(prestamo[0]))  # id_prestamo
                    dpg.add_text(prestamo[1])  # isbn_libro
                    dpg.add_text(prestamo[6] or "Sin título")  # titulo
                    dpg.add_text(prestamo[2])  # nombre_usuario
                    dpg.add_text(prestamo[3] or "")  # fecha_prestamo
                    dpg.add_text(prestamo[4] or "Pendiente")  # fecha_devolucion
                    
                    # Estado
                    if prestamo[4]:  # Si hay fecha de devolución
                        dpg.add_text("Devuelto", color=(0, 255, 0))
                    else:
                        dpg.add_text("Activo", color=(255, 255, 0))
            
            print(f"✅ Cargados {len(prestamos)} préstamos del historial")
            self._set_status(f"Cargados {len(prestamos)} préstamos en el historial")
                        
        except Exception as e:
            print(f"❌ Error al cargar historial: {e}")
            self._set_status(f"Error: {e}")
    
    def buscar_prestamos_por_usuario(self, sender=None, app_data=None):
        """Buscar préstamos por nombre de usuario"""
        termino = dpg.get_value("input_buscar_prestamos")
        
        if not termino:
            self.cargar_prestamos()
            return
        
        try:
            # Verificar que la tabla existe
            if not dpg.does_item_exist("table_prestamos"):
                self._set_status("Error: Tabla no disponible")
                return
            
            # Buscar préstamos por usuario
            prestamos = self.execute_query(sql.SEARCH_PRESTAMOS_BY_USER, (f'%{termino}%',))
            
            print(f"📊 Encontrados {len(prestamos)} préstamos para '{termino}'")
            
            # Limpiar solo las filas de datos, preservando las columnas (igual que cargar_prestamos)
            children = dpg.get_item_children("table_prestamos", slot=1)  # slot 1 contiene las filas
            if children:
                for child in children:
                    if dpg.get_item_type(child) == "mvAppItemType::mvTableRow":
                        dpg.delete_item(child)
            
            # Agregar datos filtrados (sin encabezados, ya están definidos en las columnas)
            for prestamo in prestamos:
                with dpg.table_row(parent="table_prestamos"):
                    dpg.add_text(str(prestamo[0]))  # id_prestamo
                    dpg.add_text(prestamo[1])  # isbn_libro
                    dpg.add_text(prestamo[6] or "Sin título")  # titulo
                    dpg.add_text(prestamo[2])  # nombre_usuario
                    dpg.add_text(prestamo[3] or "")  # fecha_prestamo
                    dpg.add_text(prestamo[4] or "Pendiente")  # fecha_devolucion
                    with dpg.group(horizontal=True):
                        if not prestamo[4]:  # Si no hay fecha de devolución
                            dpg.add_button(
                                label=f"Devolver##dev_prestamo_{prestamo[0]}", 
                                callback=self.devolver_libro,
                                user_data=(prestamo[0], prestamo[1]),
                                width=80
                            )
                        else:
                            dpg.add_text("Devuelto", color=(0, 255, 0))
            
            self._set_status(f"Encontrados {len(prestamos)} préstamos para '{termino}'")
            
        except Exception as e:
            print(f"❌ Error al buscar préstamos: {e}")
            self._set_status(f"Error al buscar: {e}")
    
    def buscar_prestamos_por_titulo(self, sender=None, app_data=None):
        """Buscar préstamos por título de libro"""
        termino = dpg.get_value("input_buscar_titulo")
        
        if not termino:
            self.cargar_prestamos()
            return
        
        try:
            # Verificar que la tabla existe
            if not dpg.does_item_exist("table_prestamos"):
                self._set_status("Error: Tabla no disponible")
                return
            
            # Buscar préstamos por título
            prestamos = self.execute_query(sql.SEARCH_PRESTAMOS_BY_TITLE, (f'%{termino}%',))
            
            print(f"📊 Encontrados {len(prestamos)} préstamos para el título '{termino}'")
            
            # Limpiar solo las filas de datos, preservando las columnas
            children = dpg.get_item_children("table_prestamos", slot=1)  # slot 1 contiene las filas
            if children:
                for child in children:
                    if dpg.get_item_type(child) == "mvAppItemType::mvTableRow":
                        dpg.delete_item(child)
            
            # Agregar datos filtrados (sin encabezados, ya están definidos en las columnas)
            for prestamo in prestamos:
                with dpg.table_row(parent="table_prestamos"):
                    dpg.add_text(str(prestamo[0]))  # id_prestamo
                    dpg.add_text(prestamo[1])  # isbn_libro
                    dpg.add_text(prestamo[6] or "Sin título")  # titulo
                    dpg.add_text(prestamo[2])  # nombre_usuario
                    dpg.add_text(prestamo[3] or "")  # fecha_prestamo
                    dpg.add_text(prestamo[4] or "Pendiente")  # fecha_devolucion
                    with dpg.group(horizontal=True):
                        if not prestamo[4]:  # Si no hay fecha de devolución
                            dpg.add_button(
                                label=f"Devolver##dev_prestamo_{prestamo[0]}", 
                                callback=self.devolver_libro,
                                user_data=(prestamo[0], prestamo[1]),
                                width=80
                            )
                        else:
                            dpg.add_text("Devuelto", color=(0, 255, 0))
            
            self._set_status(f"Encontrados {len(prestamos)} préstamos para el título '{termino}'")
            
        except Exception as e:
            print(f"❌ Error al buscar préstamos por título: {e}")
            self._set_status(f"Error al buscar por título: {e}")
    
    # ================================
    # INTERFAZ DE USUARIO
    # ================================
    
    def crear_interfaz_prestamos(self, parent_tab):
        """Crear la interfaz de la pestaña de préstamos"""
        dpg.add_text("Gestión de Préstamos", color=(0, 255, 0), parent=parent_tab)
        dpg.add_separator(parent=parent_tab)
        
        # Botones de control
        with dpg.group(horizontal=True, parent=parent_tab):
            dpg.add_button(label="Recargar Préstamos", callback=self.cargar_prestamos)
            dpg.add_button(label="Ver Historial", callback=self._mostrar_historial)
        dpg.add_separator(parent=parent_tab)
        
        # Formulario para registrar préstamos
        with dpg.group(horizontal=True, parent=parent_tab):
            with dpg.child_window(width=400, height=300):
                dpg.add_text("Registrar Nuevo Préstamo:")
                dpg.add_input_text(label="ISBN del Libro", tag="input_prestamo_isbn", width=200)
                dpg.add_input_text(label="Nombre Usuario", tag="input_prestamo_usuario", width=200)
                dpg.add_button(label="Registrar Préstamo", callback=self.registrar_prestamo)
                dpg.add_separator()
                dpg.add_text("Buscar Préstamos:")
                dpg.add_input_text(label="Usuario", tag="input_buscar_prestamos", width=200)
                dpg.add_button(label="Buscar Usuario", callback=self.buscar_prestamos_por_usuario, width=110)
                dpg.add_input_text(label="Título del Libro", tag="input_buscar_titulo", width=200)
                dpg.add_button(label="Buscar Título", callback=self.buscar_prestamos_por_titulo, width=110)
                dpg.add_text("", tag="status_prestamos", color=(255, 255, 0))
                dpg.add_button(label="Mostrar Todos", callback=self.cargar_prestamos, width=100)
            
            # Lista de préstamos activos
            with dpg.child_window():
                dpg.add_text("Préstamos Activos:")
                with dpg.table(tag="table_prestamos"):
                    dpg.add_table_column(label="ID")
                    dpg.add_table_column(label="ISBN")
                    dpg.add_table_column(label="Título")
                    dpg.add_table_column(label="Usuario")
                    dpg.add_table_column(label="Fecha Préstamo")
                    dpg.add_table_column(label="Fecha Devolución")
                    dpg.add_table_column(label="Acciones")
    
    def _mostrar_historial(self, sender=None, app_data=None):
        """Mostrar ventana con el historial completo de préstamos"""
        try:
            # Crear ventana de historial si no existe
            if dpg.does_item_exist("historial_window"):
                dpg.delete_item("historial_window")
                
            with dpg.window(label="Historial de Préstamos", tag="historial_window", 
                          width=800, height=600, pos=(100, 100)):
                dpg.add_text("Historial Completo de Préstamos", color=(0, 255, 255))
                dpg.add_separator()
                
                dpg.add_button(label="Actualizar Historial", callback=self.cargar_historial_prestamos)
                dpg.add_separator()
                
                with dpg.table(tag="table_historial_prestamos"):
                    dpg.add_table_column(label="ID")
                    dpg.add_table_column(label="ISBN")
                    dpg.add_table_column(label="Título")
                    dpg.add_table_column(label="Usuario")
                    dpg.add_table_column(label="Fecha Préstamo")
                    dpg.add_table_column(label="Fecha Devolución")
                    dpg.add_table_column(label="Estado")
                
                # Cargar datos del historial
                self.cargar_historial_prestamos()
            
        except Exception as e:
            self._set_status(f"Error al mostrar historial: {e}")
    
    # ================================
    # MÉTODOS AUXILIARES
    # ================================
    
    def _set_status(self, mensaje):
        """Establecer mensaje de estado"""
        if dpg.does_item_exist("status_prestamos"):
            dpg.set_value("status_prestamos", mensaje)
        print(f"📝 Status Préstamos: {mensaje}")
    
    # ================================
    # CALLBACKS PARA OTROS MÓDULOS
    # ================================
    
    def set_callbacks(self, on_prestamo_added=None, on_prestamo_returned=None):
        """Establecer callbacks para notificar a otros módulos"""
        if on_prestamo_added:
            self.on_prestamo_added = on_prestamo_added
        if on_prestamo_returned:
            self.on_prestamo_returned = on_prestamo_returned