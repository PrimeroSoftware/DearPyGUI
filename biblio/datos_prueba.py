# datos_prueba.py - Script para poblar la base de datos con datos de prueba

import sqlite3
from datetime import datetime, date
import modules.sqlstatement as sql

def crear_datos_prueba():
    """Crear datos de prueba para el sistema de biblioteca"""
    
    try:
        conn = sqlite3.connect("biblioteca.db")
        cursor = conn.cursor()
        
        # Crear tablas si no existen
        cursor.execute(sql.CREATE_TABLE_AUTORES)
        cursor.execute(sql.CREATE_TABLE_LIBROS)
        cursor.execute(sql.CREATE_TABLE_PRESTAMOS)
        
        # Datos de autores de prueba
        autores_prueba = [
            ("Gabriel", "García Márquez", "Colombiano", "1927-03-06"),
            ("Isabel", "Allende", "Chilena", "1942-08-02"),
            ("Mario", "Vargas Llosa", "Peruano", "1936-03-28"),
            ("Jorge Luis", "Borges", "Argentino", "1899-08-24"),
            ("Octavio", "Paz", "Mexicano", "1914-03-31"),
            ("Pablo", "Neruda", "Chileno", "1904-07-12"),
            ("Julio", "Cortázar", "Argentino", "1914-08-26"),
            ("Carlos", "Fuentes", "Mexicano", "1928-11-11"),
            ("Miguel", "de Cervantes", "Español", "1547-09-29"),
            ("Federico", "García Lorca", "Español", "1898-06-05")
        ]
        
        # Insertar autores
        for autor in autores_prueba:
            try:
                cursor.execute(sql.INSERT_AUTOR, autor)
            except sqlite3.IntegrityError:
                pass  # El autor ya existe
        
        # Datos de libros de prueba
        libros_prueba = [
            ("978-84-376-0494-7", "Cien años de soledad", 1, 1967, "Sudamericana", "Realismo mágico", "Disponible"),
            ("978-84-204-8228-5", "La casa de los espíritus", 2, 1982, "Plaza & Janés", "Realismo mágico", "Disponible"),
            ("978-84-204-2962-1", "La ciudad y los perros", 3, 1963, "Seix Barral", "Novela", "Disponible"),
            ("978-84-376-0495-4", "El amor en los tiempos del cólera", 1, 1985, "Oveja Negra", "Romance", "Disponible"),
            ("978-84-204-8229-2", "De amor y de sombra", 2, 1984, "Plaza & Janés", "Novela", "Disponible"),
            ("978-84-204-2963-8", "Conversación en La Catedral", 3, 1969, "Seix Barral", "Novela", "Disponible"),
            ("978-84-376-0496-1", "Ficciones", 4, 1944, "Sur", "Cuentos", "Disponible"),
            ("978-84-376-0497-8", "El laberinto de la soledad", 5, 1950, "Cuadernos Americanos", "Ensayo", "Disponible"),
            ("978-84-376-0498-5", "Veinte poemas de amor y una canción desesperada", 6, 1924, "Nascimento", "Poesía", "Disponible"),
            ("978-84-376-0499-2", "Rayuela", 7, 1963, "Sudamericana", "Novela experimental", "Disponible"),
            ("978-84-376-0500-5", "La muerte de Artemio Cruz", 8, 1962, "Fondo de Cultura Económica", "Novela", "Disponible"),
            ("978-84-376-0501-2", "Don Quijote de La Mancha", 9, 1605, "Juan de la Cuesta", "Novela clásica", "Disponible"),
            ("978-84-376-0502-9", "Bodas de sangre", 10, 1933, "Cruz y Raya", "Teatro", "Disponible"),
            ("978-84-204-8230-8", "Paula", 2, 1994, "Plaza & Janés", "Autobiografía", "Disponible"),
            ("978-84-204-2964-5", "La tía Julia y el escribidor", 3, 1977, "Seix Barral", "Novela", "Disponible")
        ]
        
        # Insertar libros
        for libro in libros_prueba:
            try:
                cursor.execute(sql.INSERT_LIBRO, libro)
            except sqlite3.IntegrityError:
                pass  # El libro ya existe
        
        # Datos de préstamos de prueba (algunos activos, algunos devueltos)
        prestamos_prueba = [
            ("978-84-376-0494-7", "Juan Pérez", "2024-08-15", "2024-08-30", "Devuelto"),
            ("978-84-204-8228-5", "María García", "2024-09-01", None, "Activo"),
            ("978-84-204-2962-1", "Carlos López", "2024-09-05", None, "Activo"),
            ("978-84-376-0495-4", "Ana Martínez", "2024-08-20", "2024-09-03", "Devuelto"),
            ("978-84-204-8229-2", "Luis Rodríguez", "2024-09-08", None, "Activo")
        ]
        
        # Insertar préstamos
        for prestamo in prestamos_prueba:
            try:
                if prestamo[3]:  # Si tiene fecha de devolución
                    cursor.execute("""
                        INSERT INTO prestamos (isbn, nombre_usuario, fecha_prestamo, fecha_devolucion, estado)
                        VALUES (?, ?, ?, ?, ?)
                    """, prestamo)
                else:  # Préstamo activo
                    cursor.execute(sql.INSERT_PRESTAMO, (prestamo[0], prestamo[1], prestamo[2]))
                    # Actualizar estado del libro a prestado
                    cursor.execute(sql.UPDATE_LIBRO_PRESTADO, (prestamo[0],))
            except sqlite3.IntegrityError:
                pass  # El préstamo ya existe
        
        conn.commit()
        conn.close()
        print("✅ Datos de prueba creados exitosamente")
        print("📚 Se agregaron:")
        print(f"   - {len(autores_prueba)} autores")
        print(f"   - {len(libros_prueba)} libros")
        print(f"   - {len(prestamos_prueba)} préstamos")
        
    except Exception as e:
        print(f"❌ Error al crear datos de prueba: {e}")

if __name__ == "__main__":
    crear_datos_prueba()
