# 📚 Trabajo Práctico: Sistema de Gestión de Biblioteca con DearPyGUI y SQLite

---

## 📝 Consigna

Desarrolla una **aplicación con interfaz gráfica** usando DearPyGUI que permita gestionar una biblioteca. El sistema debe permitir administrar libros, autores y préstamos. Los datos deben almacenarse en una base de datos **SQLite**.
Usar como base del proyecto, los archivo que estan dentro de la carpeta "biblio"
Cambiar el logo por uno que se relacione con una Biblioteca

---

## 📋 Requisitos

### 1. **Datos de los libros**

- Cada libro debe tener al menos los siguientes campos:
- **Obligatorio:** El ISBN debe estar presente y ser la **clave primaria**.

| Campos del libro             |
| ---------------------------- |
| ISBN (clave primaria)        |
| Título                      |
| Autor                        |
| Año de publicación         |
| Editorial                    |
| Género                      |
| Estado (Disponible/Prestado) |

### 2. **Datos de los autores**

- Cada autor debe tener al menos los siguientes campos:

| Campos del autor    |
| ------------------- |
| ID (clave primaria) |
| Nombre              |
| Apellido            |
| Nacionalidad        |
| Fecha de nacimiento |

### 3. **Datos de los préstamos**

- Cada préstamo debe registrar:

| Campos del préstamo     |
| ------------------------ |
| ID (clave primaria)      |
| ISBN del libro           |
| Nombre del usuario       |
| Fecha de préstamo       |
| Fecha de devolución     |
| Estado (Activo/Devuelto) |

### 4. **Interfaz gráfica**

- Utilizar DearPyGUI para crear la interfaz de usuario.
- Debe permitir:
  - 📖 **Gestión de libros:**
    - ➕ Agregar libros
    - 📄 Listar libros
    - ✏️ Modificar libros
    - 🗑️ Eliminar libros
  - ✍️ **Gestión de autores:**
    - ➕ Agregar autores
    - 📄 Listar autores
    - ✏️ Modificar autores
    - 🗑️ Eliminar autores
  - 📋 **Gestión de préstamos:**
    - ➕ Registrar préstamo
    - 📄 Listar préstamos activos
    - ↩️ Registrar devolución
    - 📊 Ver historial de préstamos

### 5. **Base de datos**

- Utilizar SQLite para almacenar los datos.
- Crear las siguientes tablas:
  - `libros` (con ISBN como clave primaria)
  - `autores` (con ID como clave primaria)
  - `prestamos` (con ID como clave primaria)
- Establecer las relaciones apropiadas entre las tablas.

### 6. **Código**

- El código debe estar **comentado** y **organizado**.
- Implementar funciones separadas para cada operación CRUD.
- Se debe entregar el archivo de la base de datos junto con el código fuente.

---

## 📦 Entregables

- Código fuente del proyecto funcionando.
- Archivo de la base de datos SQLite (con datos de prueba).
- Capturas de pantalla de la aplicación funcionando.
- Documentación breve explicando cómo usar la aplicación.
- La entrega se realiza en el repositorio de GitHub de cada alumno.

---

## 🌟 Extra (opcional)

- Validaciones de datos en la interfaz (ISBN válido, fechas, etc.).
- Búsqueda y filtrado de libros por título, autor o género.
- Reportes de libros más prestados.
- Sistema de multas por devolución tardía.
- Interfaz con pestañas para organizar mejor las funcionalidades.

---

## 🛠️ Tarea adicional

- Implementar relación entre libros y autores usando claves foráneas.
- El autor debe poder seleccionarse mediante un combo box al agregar/modificar libros.
- Mostrar el nombre completo del autor en la lista de libros.
- Validar que no se puedan eliminar autores que tengan libros asociados.

---

<div align="center">
   <h2>¡Muchos éxitos y creatividad! 💡</h2>
</div>
