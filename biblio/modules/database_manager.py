# database_manager.py - Clase base para el manejo de la base de datos

import sqlite3
from . import sqlstatement as sql

class DatabaseManager:
    """Clase base para manejar operaciones comunes de base de datos"""
    
    def __init__(self, db_name="biblioteca.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Inicializar la base de datos y crear las tablas"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Crear tablas
            cursor.execute(sql.CREATE_TABLE_AUTORES)
            cursor.execute(sql.CREATE_TABLE_LIBROS)
            cursor.execute(sql.CREATE_TABLE_PRESTAMOS)
            
            conn.commit()
            conn.close()
            print("✅ Base de datos inicializada correctamente")
        except Exception as e:
            print(f"❌ Error al inicializar la base de datos: {e}")
    
    def get_connection(self):
        """Obtener una conexión a la base de datos"""
        return sqlite3.connect(self.db_name)
    
    def execute_query(self, query, params=None):
        """Ejecutar una consulta SELECT y retornar resultados"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            results = cursor.fetchall()
            conn.close()
            return results
        except Exception as e:
            print(f"❌ Error ejecutando consulta: {e}")
            return []
    
    def execute_command(self, command, params=None):
        """Ejecutar un comando INSERT, UPDATE o DELETE"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if params:
                cursor.execute(command, params)
            else:
                cursor.execute(command)
            
            conn.commit()
            rows_affected = cursor.rowcount
            conn.close()
            return rows_affected
        except Exception as e:
            print(f"❌ Error ejecutando comando: {e}")
            return 0
    
    def verificar_datos(self):
        """Verificar que hay datos en la base de datos"""
        try:
            count_autores = self.execute_query("SELECT COUNT(*) FROM autores")[0][0]
            count_libros = self.execute_query("SELECT COUNT(*) FROM libros")[0][0]
            count_prestamos = self.execute_query("SELECT COUNT(*) FROM prestamos")[0][0]
            
            info = {
                'autores': count_autores,
                'libros': count_libros,
                'prestamos': count_prestamos
            }
            
            print(f"📊 BD: {count_autores} autores, {count_libros} libros, {count_prestamos} préstamos")
            return info
            
        except Exception as e:
            print(f"❌ Error verificando datos: {e}")
            return {'autores': 0, 'libros': 0, 'prestamos': 0}