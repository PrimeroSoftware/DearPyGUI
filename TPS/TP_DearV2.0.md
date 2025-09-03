# 🚀 Trabajo Práctico: CRUD de Empleados con DearPyGUI y SQLite

---

## 📝 Consigna

Desarrolla una **aplicación con interfaz gráfica** usando DearPyGUI que permita realizar un CRUD (Crear, Leer, Actualizar y Eliminar) de empleados. Los datos deben almacenarse en una base de datos **SQLite**.

---

## 📋 Requisitos

### 1. **Datos del empleado**

- Cada alumno puede elegir agregar al menos 2 campos que desee para el empleado.
- **Obligatorio:** El número de documento debe estar presente y ser la **clave primaria**.

| Ejemplo de campos          |
| -------------------------- |
| Número de documento (DNI) |
| Tipo de documento          |
| Nombre                     |
| Apellido                   |
| Fecha de nacimiento        |
| Puesto                     |
| Email                      |

### 2. **Interfaz gráfica**

- Utilizar DearPyGUI para crear la interfaz de usuario.
- Debe permitir:
  - ➕ Agregar empleados
  - 📄 Listar empleados
  - ✏️ Modificar empleados
  - 🗑️ Eliminar empleados

### 3. **Base de datos**

- Utilizar SQLite para almacenar los datos.
- El número de documento debe ser la clave primaria de la tabla de empleados.

### 4. **Código**

- El código debe estar **comentado** y **organizado**.
- Se debe entregar el archivo de la base de datos junto con el código fuente.

---

## 📦 Entregables

- Código fuente del proyecto funcionando.
- Archivo de la base de datos SQLite (con los datos de prueba).
- Capturas de pantalla de la aplicación funcionando.
- La entrega se realiza en el repositorio de GitHub de cada alumno.

---

## 🌟 Extra (opcional)

- Validaciones de datos en la interfaz.
- Búsqueda o filtrado de empleados.

---

<div align="center">
   <h2>¡Muchos éxitos y creatividad! 💡</h2>
</div>

---

## 🛠️ Tarea adicional

- Modificar la tabla de personas agregando un campo `tipo_documento_id` que sea una clave foránea relacionada con una nueva tabla `tipos_documento` (por ejemplo: DNI, Pasaporte, etc.).
- Crear la tabla `tipos_documento` con los diferentes tipos posibles.
- En la interfaz gráfica, el tipo de documento debe poder seleccionarse mediante un combo box (lista desplegable) al dar de alta o modificar una persona.
- El campo `tipo_documento_id` debe almacenarse y mostrarse correctamente en las operaciones de alta, modificación y listado.
