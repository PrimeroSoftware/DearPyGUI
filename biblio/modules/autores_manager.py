# autores_manager.py - Módulo para la gestión de autores

import dearpygui.dearpygui as dpg
from .database_manager import DatabaseManager
from . import sqlstatement as sql

class AutoresManager(DatabaseManager):
    """Clase para manejar todas las operaciones relacionadas con autores"""
    
    def __init__(self, db_name="biblioteca.db"):
        super().__init__(db_name)
    
    # ================================
    # OPERACIONES CRUD - AUTORES
    # ================================
    
    def agregar_autor(self, sender=None, app_data=None):
        """Agregar un nuevo autor a la base de datos"""
        nombre = dpg.get_value("input_autor_nombre")
        apellido = dpg.get_value("input_autor_apellido")
        nacionalidad = dpg.get_value("input_autor_nacionalidad")
        fecha_nacimiento = dpg.get_value("input_autor_fecha")
        
        if not nombre or not apellido:
            self._set_status("Error: Nombre y apellido son obligatorios")
            return
        
        try:
            rows_affected = self.execute_command(
                sql.INSERT_AUTOR, 
                (nombre, apellido, nacionalidad, fecha_nacimiento)
            )
            
            if rows_affected > 0:
                # Limpiar campos
                dpg.set_value("input_autor_nombre", "")
                dpg.set_value("input_autor_apellido", "")
                dpg.set_value("input_autor_nacionalidad", "")
                dpg.set_value("input_autor_fecha", "")
                
                self._set_status(f"Autor '{nombre} {apellido}' agregado exitosamente")
                self.cargar_autores()
                
                # Notificar a otros módulos si es necesario
                if hasattr(self, 'on_autor_added'):
                    self.on_autor_added()
            else:
                self._set_status("Error al agregar autor")
                
        except Exception as e:
            self._set_status(f"Error al agregar autor: {e}")
    
    def cargar_autores(self, sender=None, app_data=None):
        """Cargar la lista de autores en la tabla"""
        print("📥 Cargando autores...")
        
        try:
            # Verificar que la tabla existe
            if not dpg.does_item_exist("table_autores"):
                print("❌ ERROR: table_autores no existe!")
                self._set_status("Error: Tabla no disponible")
                return
            
            # Obtener autores de la base de datos
            autores = self.execute_query(sql.SELECT_ALL_AUTORES)
            
            print(f"📊 Encontrados {len(autores)} autores en la BD")
            
            # Limpiar solo las filas de datos, preservando las columnas
            # Primero obtenemos todos los hijos de la tabla
            children = dpg.get_item_children("table_autores", slot=1)  # slot 1 contiene las filas
            if children:
                for child in children:
                    if dpg.get_item_type(child) == "mvAppItemType::mvTableRow":
                        dpg.delete_item(child)
            
            # Agregar datos (sin encabezados, ya están definidos en las columnas)
            for autor in autores:
                with dpg.table_row(parent="table_autores"):
                    dpg.add_text(str(autor[0]))
                    dpg.add_text(autor[1])
                    dpg.add_text(autor[2])
                    dpg.add_text(autor[3] or "")
                    dpg.add_text(autor[4] or "")
                    with dpg.group(horizontal=True):
                        dpg.add_button(
                            label=f"Eliminar##del_autor_{autor[0]}", 
                            callback=lambda s, a, u=autor[0]: self.eliminar_autor(u),
                            width=80
                        )
            
            print(f"✅ Cargados {len(autores)} autores correctamente")
            self._set_status(f"Cargados {len(autores)} autores")
                        
        except Exception as e:
            print(f"❌ Error al cargar autores: {e}")
            self._set_status(f"Error: {e}")
    
    def eliminar_autor(self, autor_id):
        """Eliminar un autor (solo si no tiene libros asociados)"""
        try:
            # Verificar si tiene libros asociados
            count_result = self.execute_query(sql.CHECK_AUTOR_HAS_BOOKS, (autor_id,))
            count = count_result[0][0] if count_result else 0
            
            if count > 0:
                self._set_status("No se puede eliminar: el autor tiene libros asociados")
                return
            
            # Eliminar autor
            rows_affected = self.execute_command(sql.DELETE_AUTOR, (autor_id,))
            
            if rows_affected > 0:
                self._set_status("Autor eliminado exitosamente")
                self.cargar_autores()
                
                # Notificar a otros módulos si es necesario
                if hasattr(self, 'on_autor_deleted'):
                    self.on_autor_deleted()
            else:
                self._set_status("Error: No se pudo eliminar el autor")
            
        except Exception as e:
            self._set_status(f"Error al eliminar autor: {e}")
    
    def obtener_autores_para_combo(self):
        """Obtener lista de autores para usar en combo boxes"""
        try:
            autores = self.execute_query(sql.SELECT_AUTORES_FOR_COMBO)
            
            # Crear lista para el combo
            items = ["Sin autor"]
            valores = [None]
            
            for autor in autores:
                items.append(autor[1])  # nombre_completo
                valores.append(autor[0])  # id
            
            return items, valores
            
        except Exception as e:
            print(f"❌ Error al obtener autores para combo: {e}")
            return ["Sin autor"], [None]
    
    def actualizar_combo_autores(self, combo_tag="combo_autor_libro"):
        """Actualizar el combo box de autores"""
        try:
            items, valores = self.obtener_autores_para_combo()
            
            if dpg.does_item_exist(combo_tag):
                dpg.configure_item(combo_tag, items=items)
                # Guardar los valores para uso posterior
                setattr(self, f"{combo_tag}_valores", valores)
            
        except Exception as e:
            print(f"❌ Error al actualizar combo autores: {e}")
    
    def obtener_id_autor_seleccionado(self, combo_selection, combo_tag="combo_autor_libro"):
        """Obtener el ID del autor seleccionado en un combo"""
        try:
            valores = getattr(self, f"{combo_tag}_valores", [None])
            items, _ = self.obtener_autores_para_combo()
            
            if combo_selection in items:
                index = items.index(combo_selection)
                return valores[index] if index < len(valores) else None
            
            return None
            
        except Exception as e:
            print(f"❌ Error al obtener ID de autor: {e}")
            return None
    
    # ================================
    # INTERFAZ DE USUARIO
    # ================================
    
    def crear_interfaz_autores(self, parent_tab):
        """Crear la interfaz de la pestaña de autores"""
        dpg.add_text("Gestión de Autores", color=(0, 255, 0), parent=parent_tab)
        dpg.add_separator(parent=parent_tab)
        
        # Botón de control
        dpg.add_button(label="🔄 Recargar Autores", callback=self.cargar_autores, parent=parent_tab)
        dpg.add_separator(parent=parent_tab)
        
        # Formulario para agregar autores
        with dpg.group(horizontal=True, parent=parent_tab):
            with dpg.child_window(width=400, height=300):
                dpg.add_text("Agregar Nuevo Autor:")
                dpg.add_input_text(label="Nombre", tag="input_autor_nombre", width=200)
                dpg.add_input_text(label="Apellido", tag="input_autor_apellido", width=200)
                dpg.add_input_text(label="Nacionalidad", tag="input_autor_nacionalidad", width=200)
                dpg.add_input_text(label="Fecha Nac. (YYYY-MM-DD)", tag="input_autor_fecha", width=200)
                dpg.add_button(label="Agregar Autor", callback=self.agregar_autor)
                dpg.add_text("", tag="status_autores", color=(255, 255, 0))
            
            # Lista de autores
            with dpg.child_window():
                dpg.add_text("Lista de Autores:")
                with dpg.table(tag="table_autores"):
                    dpg.add_table_column(label="ID")
                    dpg.add_table_column(label="Nombre")
                    dpg.add_table_column(label="Apellido")
                    dpg.add_table_column(label="Nacionalidad")
                    dpg.add_table_column(label="Fecha Nac.")
                    dpg.add_table_column(label="Acciones")
    
    # ================================
    # MÉTODOS AUXILIARES
    # ================================
    
    def _set_status(self, mensaje):
        """Establecer mensaje de estado"""
        if dpg.does_item_exist("status_autores"):
            dpg.set_value("status_autores", mensaje)
        print(f"📝 Status Autores: {mensaje}")
    
    # ================================
    # CALLBACKS PARA OTROS MÓDULOS
    # ================================
    
    def set_callbacks(self, on_autor_added=None, on_autor_deleted=None):
        """Establecer callbacks para notificar a otros módulos"""
        if on_autor_added:
            self.on_autor_added = on_autor_added
        if on_autor_deleted:
            self.on_autor_deleted = on_autor_deleted