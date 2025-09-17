import dearpygui.dearpygui as dpg
import sqlite3
import sys
import os
from datetime import datetime, date

# Agregar el directorio padre al path para importar lib
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.myfunctions.myscreen import getPositionX
import modules.sqlstatement as sql

# Importar módulos de gestión
from modules.database_manager import DatabaseManager
from modules.autores_manager import AutoresManager
from modules.libros_manager import LibrosManager
from modules.prestamos_manager import PrestamosManager

class BibliotecaApp:
    def __init__(self):
        self.db_name = "biblioteca.db"
        
        # Inicializar managers
        self.db_manager = DatabaseManager(self.db_name)
        self.autores_manager = AutoresManager(self.db_name)
        self.libros_manager = LibrosManager(self.db_name)
        self.prestamos_manager = PrestamosManager(self.db_name)
        
        # Configurar callbacks entre módulos
        self.autores_manager.set_callbacks(
            on_autor_added=self.actualizar_combo_autores,
            on_autor_deleted=self.actualizar_combo_autores
        )
        
        self.libros_manager.set_callbacks(
            on_libro_added=self.actualizar_combo_libros,
            on_libro_deleted=self.actualizar_combo_libros
        )
        
        self.prestamos_manager.set_callbacks(
            on_prestamo_added=self.actualizar_combo_libros,
            on_prestamo_returned=self.actualizar_combo_libros
        )
        
        # Inicializar base de datos
        self.init_database()
        
    def init_database(self):
        """Inicializar la base de datos usando el manager"""
        self.db_manager.init_database()
    
    # ================================
    # FUNCIONES DELEGADAS - AUTORES
    # ================================
    
    def agregar_autor(self):
        """Delegar al módulo de autores"""
        self.autores_manager.agregar_autor()
    
    def cargar_autores(self, sender=None, app_data=None):
        """Delegar al módulo de autores"""
        self.autores_manager.cargar_autores(sender, app_data)
    
    def eliminar_autor(self, autor_id):
        """Delegar al módulo de autores"""
        self.autores_manager.eliminar_autor(autor_id)
    
    def actualizar_combo_autores(self):
        """Delegar al módulo de autores"""
        self.autores_manager.actualizar_combo_autores("combo_autor_libro")
        
    def actualizar_combo_libros(self):
        """Delegar al módulo de libros"""
        self.libros_manager.actualizar_combo_libros("combo_libro_prestamo")
    
    # ================================
    # FUNCIONES CRUD - LIBROS
    # ================================
    # FUNCIONES DELEGADAS - LIBROS
    # ================================
    
    def agregar_libro(self):
        """Delegar al módulo de libros"""
        self.libros_manager.agregar_libro()
    
    def cargar_libros(self, sender=None, app_data=None):
        """Delegar al módulo de libros"""
        self.libros_manager.cargar_libros(sender, app_data)
    
    def eliminar_libro(self, isbn):
        """Delegar al módulo de libros"""
        self.libros_manager.eliminar_libro(isbn)
    
    def buscar_libros(self):
        """Buscar libros por título o género"""
        termino = dpg.get_value("input_buscar_libro")
        
        if not termino:
            self.cargar_libros()
            return
        
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Buscar por título
            cursor.execute(sql.SEARCH_LIBROS_BY_TITLE, (f"%{termino}%",))
            libros_titulo = cursor.fetchall()
            
            # Buscar por género
            cursor.execute(sql.SEARCH_LIBROS_BY_GENRE, (f"%{termino}%",))
            libros_genero = cursor.fetchall()
            
            conn.close()
            
            # Combinar resultados y eliminar duplicados
            libros = libros_titulo + [libro for libro in libros_genero if libro not in libros_titulo]
            
            # Limpiar tabla
            dpg.delete_item("table_libros", children_only=True)
            
            # Agregar encabezados
            with dpg.table_row(parent="table_libros"):
                dpg.add_text("ISBN")
                dpg.add_text("Título")
                dpg.add_text("Autor")
                dpg.add_text("Año")
                dpg.add_text("Editorial")
                dpg.add_text("Género")
                dpg.add_text("Estado")
                dpg.add_text("Acciones")
            
            # Agregar datos
            for libro in libros:
                with dpg.table_row(parent="table_libros"):
                    dpg.add_text(libro[0])
                    dpg.add_text(libro[1])
                    dpg.add_text(libro[2])
                    dpg.add_text(str(libro[3]) if libro[3] else "")
                    dpg.add_text(libro[4] or "")
                    dpg.add_text(libro[5] or "")
                    dpg.add_text(libro[6])
                    with dpg.group(horizontal=True):
                        dpg.add_button(
                            label=f"Eliminar##del_libro_{libro[0]}", 
                            callback=lambda s, a, u=libro[0]: self.eliminar_libro(u),
                            width=80
                        )
                        
        except Exception as e:
            dpg.set_value("status_libros", f"Error al buscar libros: {e}")
    
    # ================================
    # FUNCIONES DELEGADAS - PRÉSTAMOS
    # ================================
    
    def registrar_prestamo(self):
        """Delegar al módulo de préstamos"""
        self.prestamos_manager.registrar_prestamo()
    
    def cargar_prestamos(self, sender=None, app_data=None):
        """Delegar al módulo de préstamos"""
        self.prestamos_manager.cargar_prestamos(sender, app_data)
    
    def registrar_devolucion(self, prestamo_id, isbn):
        """Delegar al módulo de préstamos"""
        self.prestamos_manager.devolver_libro(prestamo_id, isbn)
    
    def cargar_historial_prestamos(self, sender=None, app_data=None):
        """Delegar al módulo de préstamos"""
        self.prestamos_manager.cargar_historial_prestamos(sender, app_data)
    
    def mostrar_reportes(self):
        """Mostrar reportes de libros más prestados"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(sql.SELECT_LIBROS_MAS_PRESTADOS)
            reportes = cursor.fetchall()
            conn.close()
            
            # Limpiar solo las filas de datos, preservando las columnas (igual que autores)
            # Primero obtenemos todos los hijos de la tabla
            children = dpg.get_item_children("table_reportes", slot=1)  # slot 1 contiene las filas
            if children:
                for child in children:
                    if dpg.get_item_type(child) == "mvAppItemType::mvTableRow":
                        dpg.delete_item(child)
            
            # Agregar datos (sin encabezados, ya están definidos en las columnas)
            for reporte in reportes:
                with dpg.table_row(parent="table_reportes"):
                    dpg.add_text(reporte[0])
                    dpg.add_text(reporte[1])
                    dpg.add_text(reporte[2])
                    dpg.add_text(str(reporte[3]))
                        
        except Exception as e:
            print(f"Error al cargar reportes: {e}")
    
    def crear_interfaz(self):
        """Crear la interfaz gráfica principal"""
        # Crear el contexto de DearPyGUI
        dpg.create_context()
        
        # Configurar el viewport
        dpg.create_viewport(
            title='Sistema de Gestión de Biblioteca',
            width=1200,
            height=800,
            min_width=800,
            min_height=600,
            x_pos=getPositionX(),
            resizable=True,
            small_icon="logo.png",
            large_icon="logo.png"
        )
        
        # Crear la ventana principal con pestañas
        with dpg.window(
            label="Sistema de Gestión de Biblioteca",
            no_close=True,
            width=dpg.get_viewport_width(),
            height=dpg.get_viewport_height(),
            tag="main_window"
        ):
            with dpg.tab_bar():
                # ===== PESTAÑA DE AUTORES =====
                # Crear interfaz de autores usando el módulo
                tab_autores = dpg.add_tab(label="👨‍💼 Autores")
                self.autores_manager.crear_interfaz_autores(tab_autores)
                
                # Crear interfaz de libros usando el módulo
                tab_libros = dpg.add_tab(label="📚 Libros")
                self.libros_manager.crear_interfaz_libros(tab_libros)
                
                # Crear interfaz de préstamos usando el módulo
                tab_prestamos = dpg.add_tab(label="📋 Préstamos")
                self.prestamos_manager.crear_interfaz_prestamos(tab_prestamos)
                
                # ===== PESTAÑA DE HISTORIAL =====
                with dpg.tab(label="📊 Historial"):
                    dpg.add_text("Historial de Préstamos", color=(0, 255, 0))
                    dpg.add_separator()
                    
                    dpg.add_button(label="Actualizar Historial", callback=self.cargar_historial_prestamos)
                    
                    with dpg.table(tag="table_historial", header_row=True,
                                 borders_innerH=True, borders_outerH=True,
                                 borders_innerV=True, borders_outerV=True,
                                 height=400):
                        dpg.add_table_column(label="ID", width_fixed=True, init_width_or_weight=50)
                        dpg.add_table_column(label="ISBN", width_fixed=True, init_width_or_weight=100)
                        dpg.add_table_column(label="Título", width_fixed=True, init_width_or_weight=150)
                        dpg.add_table_column(label="Usuario", width_fixed=True, init_width_or_weight=120)
                        dpg.add_table_column(label="Fecha Préstamo", width_fixed=True, init_width_or_weight=100)
                        dpg.add_table_column(label="Fecha Devolución", width_fixed=True, init_width_or_weight=100)
                        dpg.add_table_column(label="Estado", width_fixed=True, init_width_or_weight=80)
                
                # ===== PESTAÑA DE REPORTES =====
                with dpg.tab(label="📈 Reportes"):
                    dpg.add_text("Libros Más Prestados", color=(0, 255, 0))
                    dpg.add_separator()
                    
                    dpg.add_button(label="Generar Reporte", callback=self.mostrar_reportes)
                    
                    with dpg.table(tag="table_reportes", header_row=True,
                                 borders_innerH=True, borders_outerH=True,
                                 borders_innerV=True, borders_outerV=True,
                                 height=400):
                        dpg.add_table_column(label="ISBN", width_fixed=True, init_width_or_weight=100)
                        dpg.add_table_column(label="Título", width_fixed=True, init_width_or_weight=200)
                        dpg.add_table_column(label="Autor", width_fixed=True, init_width_or_weight=150)
                        dpg.add_table_column(label="Total Préstamos", width_fixed=True, init_width_or_weight=120)
    
    def ejecutar(self):
        """Ejecutar la aplicación"""
        self.crear_interfaz()
        
        # Configurar DearPyGUI ANTES de cargar datos
        dpg.setup_dearpygui()
        
        # Cargar datos iniciales DESPUÉS de configurar la interfaz usando los módulos
        self.autores_manager.cargar_autores()
        self.autores_manager.actualizar_combo_autores("combo_autor_libro")
        self.libros_manager.cargar_libros()
        self.prestamos_manager.cargar_prestamos()
        
        # Mostrar la aplicación
        dpg.show_viewport()
        dpg.start_dearpygui()
        
        # Limpiar recursos al cerrar
        dpg.destroy_context()

def main():
    app = BibliotecaApp()
    app.ejecutar()

if __name__ == "__main__":
    main()
