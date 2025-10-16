# sqlstatement.py - Sentencias SQL para el Sistema de Gestión de Biblioteca

# ================================
# CREACIÓN DE TABLAS
# ================================

CREATE_TABLE_AUTORES = '''
CREATE TABLE IF NOT EXISTS autores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    nacionalidad TEXT,
    fecha_nacimiento DATE
)
'''

CREATE_TABLE_LIBROS = '''
CREATE TABLE IF NOT EXISTS libros (
    isbn TEXT PRIMARY KEY,
    titulo TEXT NOT NULL,
    autor_id INTEGER,
    año_publicacion INTEGER,
    editorial TEXT,
    genero TEXT,
    estado TEXT DEFAULT 'Disponible',
    FOREIGN KEY (autor_id) REFERENCES autores(id)
)
'''

CREATE_TABLE_PRESTAMOS = '''
CREATE TABLE IF NOT EXISTS prestamos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    isbn TEXT NOT NULL,
    nombre_usuario TEXT NOT NULL,
    fecha_prestamo DATE NOT NULL,
    fecha_devolucion DATE,
    estado TEXT DEFAULT 'Activo',
    FOREIGN KEY (isbn) REFERENCES libros(isbn)
)
'''

# ================================
# OPERACIONES CRUD - AUTORES
# ================================

INSERT_AUTOR = '''
INSERT INTO autores (nombre, apellido, nacionalidad, fecha_nacimiento)
VALUES (?, ?, ?, ?)
'''

# SELECT Específicos
SELECT_ALL_AUTORES = "SELECT * FROM autores ORDER BY apellido, nombre"
SELECT_ALL_LIBROS = "SELECT * FROM libros ORDER BY titulo"
SELECT_ALL_PRESTAMOS = "SELECT * FROM prestamos ORDER BY fecha_prestamo DESC"

# SELECT para combos y relaciones
SELECT_AUTORES_FOR_COMBO = """
SELECT id, 
       (nombre || ' ' || apellido) as nombre_completo
FROM autores 
ORDER BY apellido, nombre
"""

# Verificaciones de integridad
CHECK_AUTOR_HAS_BOOKS = """
SELECT COUNT(*) 
FROM libros 
WHERE autor_id = ?
"""

CHECK_LIBRO_HAS_ACTIVE_LOANS = """
SELECT COUNT(*) 
FROM prestamos 
WHERE isbn = ? AND fecha_devolucion IS NULL
"""

# SELECT con JOINs
SELECT_LIBROS_WITH_AUTHORS = """
SELECT l.isbn, l.titulo, l.autor_id, l.año_publicacion, l.editorial, l.genero, l.estado,
       COALESCE(a.nombre || ' ' || a.apellido, 'Sin autor') as nombre_autor
FROM libros l
LEFT JOIN autores a ON l.autor_id = a.id
ORDER BY l.titulo
"""

SELECT_LIBROS_DISPONIBLES_FOR_COMBO = """
SELECT isbn, titulo
FROM libros 
WHERE estado = 'Disponible'
ORDER BY titulo
"""

# UPDATE específicos
UPDATE_LIBRO_ESTADO = """
UPDATE libros 
SET estado = ?
WHERE isbn = ?
"""

UPDATE_PRESTAMO_DEVOLUCION = """
UPDATE prestamos 
SET fecha_devolucion = ?
WHERE id = ?
"""

# SELECT con JOINs para préstamos
SELECT_PRESTAMOS_WITH_BOOKS = """
SELECT p.id, p.isbn, p.nombre_usuario, p.fecha_prestamo, p.fecha_devolucion, p.estado,
       l.titulo
FROM prestamos p
LEFT JOIN libros l ON p.isbn = l.isbn
WHERE p.fecha_devolucion IS NULL
ORDER BY p.fecha_prestamo DESC
"""

SELECT_HISTORIAL_PRESTAMOS = """
SELECT p.id, p.isbn, p.nombre_usuario, p.fecha_prestamo, p.fecha_devolucion, p.estado,
       l.titulo
FROM prestamos p
LEFT JOIN libros l ON p.isbn = l.isbn
ORDER BY p.fecha_prestamo DESC
"""

# Búsquedas específicas
SEARCH_PRESTAMOS_BY_USER = """
SELECT p.id, p.isbn, p.nombre_usuario, p.fecha_prestamo, p.fecha_devolucion, p.estado,
       l.titulo
FROM prestamos p
LEFT JOIN libros l ON p.isbn = l.isbn
WHERE p.nombre_usuario LIKE ?
ORDER BY p.fecha_prestamo DESC
"""

SEARCH_PRESTAMOS_BY_TITLE = """
SELECT p.id, p.isbn, p.nombre_usuario, p.fecha_prestamo, p.fecha_devolucion, p.estado,
       l.titulo
FROM prestamos p
LEFT JOIN libros l ON p.isbn = l.isbn
WHERE l.titulo LIKE ?
ORDER BY p.fecha_prestamo DESC
"""

# Verificaciones para préstamos
CHECK_LIBRO_DISPONIBLE = """
SELECT isbn, titulo, estado
FROM libros 
WHERE isbn = ? AND estado = 'Disponible'
"""

SELECT_AUTOR_BY_ID = '''
SELECT id, nombre, apellido, nacionalidad, fecha_nacimiento
FROM autores
WHERE id = ?
'''

UPDATE_AUTOR = '''
UPDATE autores
SET nombre = ?, apellido = ?, nacionalidad = ?, fecha_nacimiento = ?
WHERE id = ?
'''

DELETE_AUTOR = '''
DELETE FROM autores
WHERE id = ?
'''

# Verificar si un autor tiene libros asociados
CHECK_AUTOR_HAS_BOOKS = '''
SELECT COUNT(*) FROM libros WHERE autor_id = ?
'''

# ================================
# OPERACIONES CRUD - LIBROS
# ================================

INSERT_LIBRO = '''
INSERT INTO libros (isbn, titulo, autor_id, año_publicacion, editorial, genero, estado)
VALUES (?, ?, ?, ?, ?, ?, ?)
'''

SELECT_ALL_LIBROS = '''
SELECT l.isbn, l.titulo, 
       COALESCE(a.nombre || ' ' || a.apellido, 'Sin autor') as autor,
       l.año_publicacion, l.editorial, l.genero, l.estado
FROM libros l
LEFT JOIN autores a ON l.autor_id = a.id
ORDER BY l.titulo
'''

SELECT_LIBRO_BY_ISBN = '''
SELECT l.isbn, l.titulo, l.autor_id,
       COALESCE(a.nombre || ' ' || a.apellido, 'Sin autor') as autor,
       l.año_publicacion, l.editorial, l.genero, l.estado
FROM libros l
LEFT JOIN autores a ON l.autor_id = a.id
WHERE l.isbn = ?
'''

UPDATE_LIBRO = '''
UPDATE libros
SET titulo = ?, autor_id = ?, año_publicacion = ?, editorial = ?, genero = ?, estado = ?
WHERE isbn = ?
'''

UPDATE_LIBRO_INFO = '''
UPDATE libros
SET titulo = ?, autor_id = ?, año_publicacion = ?, editorial = ?, genero = ?
WHERE isbn = ?
'''

DELETE_LIBRO = '''
DELETE FROM libros
WHERE isbn = ?
'''

# Búsqueda de libros
SEARCH_LIBROS_BY_TITLE = '''
SELECT l.isbn, l.titulo, 
       COALESCE(a.nombre || ' ' || a.apellido, 'Sin autor') as autor,
       l.año_publicacion, l.editorial, l.genero, l.estado
FROM libros l
LEFT JOIN autores a ON l.autor_id = a.id
WHERE l.titulo LIKE ?
ORDER BY l.titulo
'''

SEARCH_LIBROS_BY_GENRE = '''
SELECT l.isbn, l.titulo, 
       COALESCE(a.nombre || ' ' || a.apellido, 'Sin autor') as autor,
       l.año_publicacion, l.editorial, l.genero, l.estado
FROM libros l
LEFT JOIN autores a ON l.autor_id = a.id
WHERE l.genero LIKE ?
ORDER BY l.titulo
'''

# ================================
# OPERACIONES CRUD - PRÉSTAMOS
# ================================

INSERT_PRESTAMO = '''
INSERT INTO prestamos (isbn, nombre_usuario, fecha_prestamo, estado)
VALUES (?, ?, ?, 'Activo')
'''

SELECT_ALL_PRESTAMOS = '''
SELECT p.id, p.isbn, l.titulo, p.nombre_usuario, 
       p.fecha_prestamo, p.fecha_devolucion, p.estado
FROM prestamos p
JOIN libros l ON p.isbn = l.isbn
ORDER BY p.fecha_prestamo DESC
'''

SELECT_PRESTAMOS_ACTIVOS = '''
SELECT p.id, p.isbn, l.titulo, p.nombre_usuario, 
       p.fecha_prestamo, p.estado
FROM prestamos p
JOIN libros l ON p.isbn = l.isbn
WHERE p.estado = 'Activo'
ORDER BY p.fecha_prestamo DESC
'''

SELECT_PRESTAMO_BY_ID = '''
SELECT p.id, p.isbn, l.titulo, p.nombre_usuario, 
       p.fecha_prestamo, p.fecha_devolucion, p.estado
FROM prestamos p
JOIN libros l ON p.isbn = l.isbn
WHERE p.id = ?
'''

UPDATE_PRESTAMO_DEVUELTO = '''
UPDATE prestamos
SET fecha_devolucion = ?, estado = 'Devuelto'
WHERE id = ?
'''

# Verificar si un libro está disponible para préstamo
CHECK_LIBRO_DISPONIBLE = '''
SELECT COUNT(*) FROM prestamos 
WHERE isbn = ? AND estado = 'Activo'
'''

# Actualizar estado del libro a prestado
UPDATE_LIBRO_PRESTADO = '''
UPDATE libros
SET estado = 'Prestado'
WHERE isbn = ?
'''

# Actualizar estado del libro a disponible
UPDATE_LIBRO_DISPONIBLE = '''
UPDATE libros
SET estado = 'Disponible'
WHERE isbn = ?
'''

# ================================
# CONSULTAS ESPECIALES
# ================================

# Combo box para seleccionar autores
SELECT_AUTORES_FOR_COMBO = '''
SELECT id, nombre || ' ' || apellido as nombre_completo
FROM autores
ORDER BY apellido, nombre
'''

# Libros más prestados (para reportes)
SELECT_LIBROS_MAS_PRESTADOS = '''
SELECT l.isbn, l.titulo, 
       COALESCE(a.nombre || ' ' || a.apellido, 'Sin autor') as autor,
       COUNT(p.id) as total_prestamos
FROM libros l
LEFT JOIN autores a ON l.autor_id = a.id
LEFT JOIN prestamos p ON l.isbn = p.isbn
GROUP BY l.isbn, l.titulo, autor
HAVING COUNT(p.id) > 0
ORDER BY total_prestamos DESC, l.titulo
LIMIT 10
'''

# Historial de préstamos de un usuario
SELECT_HISTORIAL_USUARIO = '''
SELECT p.id, p.isbn, l.titulo, p.fecha_prestamo, p.fecha_devolucion, p.estado
FROM prestamos p
JOIN libros l ON p.isbn = l.isbn
WHERE p.nombre_usuario = ?
ORDER BY p.fecha_prestamo DESC
'''

# Préstamos con retraso (opcional para sistema de multas)
SELECT_PRESTAMOS_VENCIDOS = '''
SELECT p.id, p.isbn, l.titulo, p.nombre_usuario, 
       p.fecha_prestamo,
       julianday('now') - julianday(p.fecha_prestamo) as dias_transcurridos
FROM prestamos p
JOIN libros l ON p.isbn = l.isbn
WHERE p.estado = 'Activo' 
  AND julianday('now') - julianday(p.fecha_prestamo) > 15
ORDER BY dias_transcurridos DESC
'''
