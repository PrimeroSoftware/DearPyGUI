# libros_manager.py - Módulo para la gestión de libros

import dearpygui.dearpygui as dpg
from .database_manager import DatabaseManager
from .autores_manager import AutoresManager
from . import sqlstatement as sql

class LibrosManager(DatabaseManager):
    """Clase para manejar todas las operaciones relacionadas con libros"""
    
    def __init__(self, db_name="biblioteca.db"):
        super().__init__(db_name)
        self.autores_manager = AutoresManager(db_name)
    
    # ================================
    # OPERACIONES CRUD - LIBROS
    # ================================
    
    def agregar_libro(self, sender=None, app_data=None):
        """Agregar un nuevo libro a la base de datos"""
        isbn = dpg.get_value("input_libro_isbn")
        titulo = dpg.get_value("input_libro_titulo")
        combo_selection = dpg.get_value("combo_autor_libro")
        año = dpg.get_value("input_libro_año")
        editorial = dpg.get_value("input_libro_editorial")
        genero = dpg.get_value("input_libro_genero")
        
        if not isbn or not titulo:
            self._set_status("Error: ISBN y título son obligatorios")
            return
        
        # Obtener ID del autor seleccionado
        autor_id = self.autores_manager.obtener_id_autor_seleccionado(combo_selection, "combo_autor_libro")
        
        try:
            rows_affected = self.execute_command(
                sql.INSERT_LIBRO, 
                (isbn, titulo, autor_id, año, editorial, genero, "Disponible")
            )
            
            if rows_affected > 0:
                # Limpiar campos
                dpg.set_value("input_libro_isbn", "")
                dpg.set_value("input_libro_titulo", "")
                dpg.set_value("combo_autor_libro", "Sin autor")
                dpg.set_value("input_libro_año", "")
                dpg.set_value("input_libro_editorial", "")
                dpg.set_value("input_libro_genero", "")
                
                self._set_status(f"Libro '{titulo}' agregado exitosamente")
                self.cargar_libros()
                
                # Notificar a otros módulos si es necesario
                if hasattr(self, 'on_libro_added'):
                    self.on_libro_added()
            else:
                self._set_status("Error al agregar libro")
                
        except Exception as e:
            self._set_status(f"Error al agregar libro: {e}")
    
    def cargar_libros(self, sender=None, app_data=None):
        """Cargar la lista de libros en la tabla"""
        print("📥 Cargando libros...")
        
        try:
            # Verificar que la tabla existe
            if not dpg.does_item_exist("table_libros"):
                print("❌ ERROR: table_libros no existe!")
                self._set_status("Error: Tabla no disponible")
                return
            
            # Obtener libros con información de autores
            libros = self.execute_query(sql.SELECT_LIBROS_WITH_AUTHORS)
            
            print(f"📊 Encontrados {len(libros)} libros en la BD")
            
            # Limpiar solo las filas de datos, preservando las columnas (igual que autores)
            # Primero obtenemos todos los hijos de la tabla
            children = dpg.get_item_children("table_libros", slot=1)  # slot 1 contiene las filas
            if children:
                for child in children:
                    if dpg.get_item_type(child) == "mvAppItemType::mvTableRow":
                        dpg.delete_item(child)
            
            # Agregar datos (sin encabezados, ya están definidos en las columnas)
            for libro in libros:
                with dpg.table_row(parent="table_libros"):
                    dpg.add_text(libro[0])  # isbn
                    dpg.add_text(libro[1])  # titulo
                    dpg.add_text(libro[7] or "Sin autor")  # nombre_autor
                    dpg.add_text(str(libro[3]) if libro[3] else "")  # año
                    dpg.add_text(libro[4] or "")  # editorial
                    dpg.add_text(libro[5] or "")  # genero
                    dpg.add_text(libro[6] or "")  # estado
                    with dpg.group(horizontal=True):
                        dpg.add_button(
                            label=f"Eliminar##del_libro_{libro[0]}", 
                            callback=lambda s, a, isbn=libro[0]: self.eliminar_libro(isbn),
                            width=80
                        )
            
            print(f"✅ Cargados {len(libros)} libros correctamente")
            self._set_status(f"Cargados {len(libros)} libros")
                        
        except Exception as e:
            print(f"❌ Error al cargar libros: {e}")
            self._set_status(f"Error: {e}")
    
    def eliminar_libro(self, isbn):
        """Eliminar un libro (solo si no tiene préstamos activos)"""
        try:
            # Verificar si tiene préstamos activos
            count_result = self.execute_query(sql.CHECK_LIBRO_HAS_ACTIVE_LOANS, (isbn,))
            count = count_result[0][0] if count_result else 0
            
            if count > 0:
                self._set_status("No se puede eliminar: el libro tiene préstamos activos")
                return
            
            # Eliminar libro
            rows_affected = self.execute_command(sql.DELETE_LIBRO, (isbn,))
            
            if rows_affected > 0:
                self._set_status("Libro eliminado exitosamente")
                self.cargar_libros()
                
                # Notificar a otros módulos si es necesario
                if hasattr(self, 'on_libro_deleted'):
                    self.on_libro_deleted()
            else:
                self._set_status("Error: No se pudo eliminar el libro")
            
        except Exception as e:
            self._set_status(f"Error al eliminar libro: {e}")
    
    def obtener_libros_disponibles_para_combo(self):
        """Obtener lista de libros disponibles para usar en combo boxes"""
        try:
            libros = self.execute_query(sql.SELECT_LIBROS_DISPONIBLES_FOR_COMBO)
            
            # Crear lista para el combo
            items = ["Seleccionar libro..."]
            valores = [None]
            
            for libro in libros:
                items.append(f"{libro[1]} - {libro[0]}")  # titulo - isbn
                valores.append(libro[0])  # isbn
            
            return items, valores
            
        except Exception as e:
            print(f"❌ Error al obtener libros para combo: {e}")
            return ["Seleccionar libro..."], [None]
    
    def actualizar_combo_libros(self, combo_tag="combo_libro_prestamo"):
        """Actualizar el combo box de libros disponibles"""
        try:
            items, valores = self.obtener_libros_disponibles_para_combo()
            
            if dpg.does_item_exist(combo_tag):
                dpg.configure_item(combo_tag, items=items)
                # Guardar los valores para uso posterior
                setattr(self, f"{combo_tag}_valores", valores)
            
        except Exception as e:
            print(f"❌ Error al actualizar combo libros: {e}")
    
    def obtener_isbn_libro_seleccionado(self, combo_selection, combo_tag="combo_libro_prestamo"):
        """Obtener el ISBN del libro seleccionado en un combo"""
        try:
            valores = getattr(self, f"{combo_tag}_valores", [None])
            items, _ = self.obtener_libros_disponibles_para_combo()
            
            if combo_selection in items:
                index = items.index(combo_selection)
                return valores[index] if index < len(valores) else None
            
            return None
            
        except Exception as e:
            print(f"❌ Error al obtener ISBN de libro: {e}")
            return None
    
    def cambiar_estado_libro(self, isbn, nuevo_estado):
        """Cambiar el estado de un libro (Disponible, Prestado, etc.)"""
        try:
            rows_affected = self.execute_command(sql.UPDATE_LIBRO_ESTADO, (nuevo_estado, isbn))
            
            if rows_affected > 0:
                print(f"✅ Estado del libro {isbn} cambiado a '{nuevo_estado}'")
                self.cargar_libros()
                self.actualizar_combo_libros()
                return True
            else:
                print(f"❌ No se pudo cambiar el estado del libro {isbn}")
                return False
            
        except Exception as e:
            print(f"❌ Error al cambiar estado del libro: {e}")
            return False
    
    # ================================
    # INTERFAZ DE USUARIO
    # ================================
    
    def crear_interfaz_libros(self, parent_tab):
        """Crear la interfaz de la pestaña de libros"""
        dpg.add_text("Gestión de Libros", color=(0, 255, 0), parent=parent_tab)
        dpg.add_separator(parent=parent_tab)
        
        # Botón de control
        with dpg.group(horizontal=True, parent=parent_tab):
            dpg.add_button(label="🔄 Recargar Libros", callback=self.cargar_libros)
            dpg.add_button(label="🔄 Actualizar Autores", callback=self._actualizar_combo_autores_libros)
        dpg.add_separator(parent=parent_tab)
        
        # Formulario para agregar libros
        with dpg.group(horizontal=True, parent=parent_tab):
            with dpg.child_window(width=400, height=400):
                dpg.add_text("Agregar Nuevo Libro:")
                dpg.add_input_text(label="ISBN", tag="input_libro_isbn", width=200)
                dpg.add_input_text(label="Título", tag="input_libro_titulo", width=200)
                dpg.add_combo(label="Autor", tag="combo_autor_libro", items=["Sin autor"], width=200)
                dpg.add_input_text(label="Año", tag="input_libro_año", width=200)
                dpg.add_input_text(label="Editorial", tag="input_libro_editorial", width=200)
                dpg.add_input_text(label="Género", tag="input_libro_genero", width=200)
                dpg.add_button(label="Agregar Libro", callback=self.agregar_libro)
                dpg.add_text("", tag="status_libros", color=(255, 255, 0))
            
            # Lista de libros
            with dpg.child_window():
                dpg.add_text("Lista de Libros:")
                with dpg.table(tag="table_libros"):
                    dpg.add_table_column(label="ISBN")
                    dpg.add_table_column(label="Título")
                    dpg.add_table_column(label="Autor")
                    dpg.add_table_column(label="Año")
                    dpg.add_table_column(label="Editorial")
                    dpg.add_table_column(label="Género")
                    dpg.add_table_column(label="Estado")
                    dpg.add_table_column(label="Acciones")
    
    # ================================
    # MÉTODOS AUXILIARES
    # ================================
    
    def _set_status(self, mensaje):
        """Establecer mensaje de estado"""
        if dpg.does_item_exist("status_libros"):
            dpg.set_value("status_libros", mensaje)
        print(f"📝 Status Libros: {mensaje}")
    
    def _actualizar_combo_autores_libros(self, sender=None, app_data=None):
        """Actualizar el combo de autores en la interfaz de libros"""
        self.autores_manager.actualizar_combo_autores("combo_autor_libro")
        self._set_status("Combo de autores actualizado")
    
    # ================================
    # CALLBACKS PARA OTROS MÓDULOS
    # ================================
    
    def set_callbacks(self, on_libro_added=None, on_libro_deleted=None):
        """Establecer callbacks para notificar a otros módulos"""
        if on_libro_added:
            self.on_libro_added = on_libro_added
        if on_libro_deleted:
            self.on_libro_deleted = on_libro_deleted