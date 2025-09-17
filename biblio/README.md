# 📚 Sistema de Gestión de Biblioteca

Sistema completo de gestión bibliotecaria desarrollado con **DearPyGUI** y **SQLite** que permite administrar libros, autores y préstamos de manera integral y eficiente. Este proyecto es una implementación completa de un CRUD (Create, Read, Update, Delete) con interfaz gráfica moderna y arquitectura modular.

## 🎯 Descripción del Proyecto

Este sistema de biblioteca está diseñado para facilitar la gestión completa de una biblioteca, desde el registro de autores y libros hasta el control de préstamos y devoluciones. Utiliza una arquitectura modular que separa las responsabilidades en diferentes managers especializados, garantizando un código mantenible y escalable.

### ✨ Características Principales

- 🏗️ **Arquitectura Modular**: Código organizado en módulos especializados (`AutoresManager`, `LibrosManager`, `PrestamosManager`, `DatabaseManager`)
- 👨‍💼 **Gestión Completa de Autores**: CRUD completo con validación de integridad referencial
- 📚 **Administración de Libros**: Control de inventario con estados y relaciones con autores
- 📋 **Sistema de Préstamos**: Registro de préstamos y devoluciones con control de fechas
- 🔍 **Búsqueda Avanzada**: Filtrado por título y género de libros
- 📊 **Historial Completo**: Registro detallado de todos los préstamos realizados
- 📈 **Reportes Estadísticos**: Análisis de libros más prestados
- 🖥️ **Interfaz Intuitiva**: GUI moderna con pestañas organizadas y controles amigables
- 🗄️ **Base de Datos Robusta**: SQLite con esquema normalizado y relaciones apropiadas
- ⚡ **Tiempo Real**: Actualizaciones automáticas entre módulos mediante callbacks

## 🏗️ Arquitectura del Sistema

### Estructura de Módulos

```
biblio/
├── main.py                 # Aplicación principal y coordinación de módulos
├── modules/                # Módulos especializados
│   ├── database_manager.py    # Gestor base de base de datos
│   ├── autores_manager.py     # Gestión completa de autores
│   ├── libros_manager.py      # Gestión completa de libros
│   ├── prestamos_manager.py   # Gestión completa de préstamos
│   └── sqlstatement.py        # Definición de consultas SQL
├── lib/myfunctions/        # Funciones auxiliares
└── biblioteca.db           # Base de datos SQLite
```

### Componentes Clave

1. **BibliotecaApp**: Clase principal que coordina todos los módulos
2. **DatabaseManager**: Clase base para operaciones de base de datos
3. **AutoresManager**: Manejo especializado de autores
4. **LibrosManager**: Gestión integral de libros
5. **PrestamosManager**: Control completo de préstamos y devoluciones

## 📋 Requisitos del Sistema

- **Python 3.7+**
- **DearPyGUI** (Interfaz gráfica moderna)
- **SQLite3** (incluido en Python)
- **Sistema Operativo**: Windows, Linux, macOS

## 🛠️ Instalación y Configuración

1. **Clonar o descargar el proyecto**
2. **Instalar dependencias:**
   ```bash
   pip install dearpygui
   ```

3. **Ejecutar datos de prueba (opcional):**
   ```bash
   python datos_prueba.py
   ```

4. **Iniciar la aplicación:**
   ```bash
   python main.py
   ```

## 📖 Manual de Usuario Completo

### 👨‍💼 Gestión de Autores

**Funcionalidades disponibles:**
- ➕ **Agregar Autores**: Registro completo con nombre, apellido, nacionalidad y fecha de nacimiento
- 📋 **Listar Autores**: Visualización en tabla con información completa
- 🗑️ **Eliminar Autores**: Con validación de integridad referencial
- 🔄 **Actualización Automática**: Los combos de selección se actualizan en tiempo real

**Proceso para agregar autor:**
1. Navega a la pestaña "👨‍💼 Autores"
2. Completa los campos obligatorios: Nombre y Apellido
3. Opcionalmente: Nacionalidad y Fecha de Nacimiento
4. Haz clic en "Agregar Autor"
5. El sistema validará los datos y actualizará la tabla automáticamente

**Restricciones importantes:**

- Solo se pueden eliminar autores que no tengan libros asociados

### 📚 Gestión de Libros

**Funcionalidades disponibles:**

- ➕ **Agregar Libros**: Registro completo con ISBN, título, autor, año, editorial y género
- 📋 **Listar Libros**: Visualización detallada con información del autor
- 🔍 **Búsqueda Avanzada**: Por título y género simultáneamente
- 🗑️ **Eliminar Libros**: Con validación de estado de préstamo
- 🔄 **Control de Estados**: Automático entre "Disponible" y "Prestado"

**Proceso para agregar libro:**

1. Ve a la pestaña "📚 Libros"
2. Completa los campos obligatorios: ISBN y Título
3. Selecciona un autor del combo desplegable
4. Opcionalmente: Año, Editorial y Género
5. Haz clic en "Agregar Libro"

**Búsqueda de libros:**

1. Ingresa un término en el campo de búsqueda
2. Haz clic en "Buscar Libros" para filtrar por título o género
3. El sistema mostrará resultados coincidentes en tiempo real

**Eliminar libro:**

- Haz clic en "Eliminar" junto al libro deseado
- Solo se pueden eliminar libros que no estén actualmente prestados

### 📋 Gestión de Préstamos

**Funcionalidades disponibles:**

- 📝 **Registrar Préstamos**: Control automático de disponibilidad
- 📋 **Listar Préstamos Activos**: Visualización de préstamos pendientes
- 🔄 **Procesar Devoluciones**: Cambio automático de estados
- 📊 **Control de Fechas**: Registro automático de fechas de préstamo y devolución

**Proceso para registrar préstamo:**

1. Ve a la pestaña "📋 Préstamos"
2. Completa el ISBN del libro (debe estar disponible)
3. Ingresa el nombre del usuario
4. Haz clic en "Registrar Préstamo"
5. El sistema cambia automáticamente el estado del libro a "Prestado"

**Procesar devolución:**

- En la lista de préstamos activos, haz clic en "Devolver"
- El sistema registra la fecha de devolución y cambia el estado a "Disponible"

### 📊 Consultar Historial

**Ver historial completo:**

1. Ve a la pestaña "📊 Historial"
2. Haz clic en "Actualizar Historial"
3. Se mostrará el registro completo de todos los préstamos (activos y devueltos)

### 📈 Reportes y Estadísticas

**Generar reportes:**

1. Ve a la pestaña "📈 Reportes"
2. Haz clic en "Generar Reporte"
3. Se mostrarán los libros más prestados ordenados por cantidad

## 🗄️ Estructura Técnica de la Base de Datos

### Esquema Normalizado

**Tabla `autores`**

- `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- `nombre` (TEXT, NOT NULL)
- `apellido` (TEXT, NOT NULL)
- `nacionalidad` (TEXT)
- `fecha_nacimiento` (DATE)

**Tabla `libros`**

- `isbn` (TEXT, PRIMARY KEY)
- `titulo` (TEXT, NOT NULL)
- `autor_id` (INTEGER, FOREIGN KEY → autores.id)
- `año` (INTEGER)
- `editorial` (TEXT)
- `genero` (TEXT)
- `estado` (TEXT, DEFAULT 'Disponible')

**Tabla `prestamos`**

- `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- `isbn` (TEXT, FOREIGN KEY → libros.isbn)
- `nombre_usuario` (TEXT, NOT NULL)
- `fecha_prestamo` (DATE, NOT NULL)
- `fecha_devolucion` (DATE)
- `estado` (TEXT, DEFAULT 'Activo')

### Relaciones y Integridad Referencial

- Un **autor** puede tener múltiples **libros** (relación 1:N)
- Un **libro** puede tener múltiples **préstamos** (relación 1:N)
- Los **préstamos** mantienen referencia al **libro** prestado
- Integridad referencial: No se pueden eliminar autores con libros asociados

## ⚙️ Funcionalidades Técnicas Avanzadas

### 🔄 Sistema de Callbacks y Actualizaciones Automáticas

El sistema implementa un patrón de callbacks que permite actualizaciones en tiempo real entre módulos:

```python
# Configuración de callbacks entre módulos
self.autores_manager.set_callbacks(
    on_autor_added=self.actualizar_combo_autores,
    on_autor_deleted=self.actualizar_combo_autores
)
```

### 🏗️ Arquitectura Modular

- **Separación de Responsabilidades**: Cada módulo maneja una entidad específica
- **Herencia de DatabaseManager**: Todas las clases heredan funcionalidades base
- **Delegación de Funciones**: La clase principal delega operaciones a módulos especializados
- **Reutilización de Código**: Métodos comunes centralizados en la clase base

### 🔍 Consultas SQL Optimizadas

```sql
-- Ejemplo: Consulta de libros con información de autores
SELECT l.isbn, l.titulo, 
       CASE 
           WHEN a.nombre IS NOT NULL THEN a.nombre || ' ' || a.apellido 
           ELSE 'Sin autor' 
       END as autor,
       l.año, l.editorial, l.genero, l.estado
FROM libros l
LEFT JOIN autores a ON l.autor_id = a.id
```

## 🔧 Solución de Problemas Comunes

### Error al crear la base de datos

- Verifica que tengas permisos de escritura en el directorio
- Asegúrate de que no haya otro proceso usando la base de datos

### Interfaz no se muestra correctamente

- Verifica que DearPyGUI esté instalado: `pip install dearpygui`
- Comprueba la resolución de pantalla mínima requerida

### Base de datos vacía al iniciar

- Ejecuta `datos_prueba.py` para cargar datos de ejemplo
- Verifica que el archivo `biblioteca.db` se haya creado correctamente

## 📁 Archivos del Proyecto

### Archivos Principales

- `main.py`: Contiene la clase principal `BibliotecaApp` con toda la lógica
- `modules/database_manager.py`: Clase base para operaciones de base de datos
- `modules/autores_manager.py`: Gestión completa de autores
- `modules/libros_manager.py`: Gestión completa de libros
- `modules/prestamos_manager.py`: Gestión completa de préstamos
- `modules/sqlstatement.py`: Definición centralizada de consultas SQL
- `datos_prueba.py`: Script para generar datos de prueba
- `biblioteca.db`: Base de datos SQLite generada automáticamente

### Archivos de Soporte

- `lib/myfunctions/myscreen.py`: Funciones auxiliares para la interfaz
- `logo.png`: Icono de la aplicación

## 🚀 Posibles Extensiones Futuras

- **Sistema de Multas**: Control de fechas de devolución y penalizaciones
- **Reservas de Libros**: Permitir reservar libros prestados
- **Categorización Avanzada**: Gestión de categorías y subcategorías
- **Reportes PDF**: Generación de reportes en formato PDF
- **Base de Datos Remota**: Soporte para PostgreSQL o MySQL
- **Autenticación de Usuarios**: Sistema de login para bibliotecarios
- **API REST**: Exposición de funcionalidades via API

## 📜 Licencia

Este proyecto se distribuye bajo los términos especificados en el archivo `LICENSE`.

---

### 💻 Desarrollado con Python y DearPyGUI

Este sistema representa una implementación completa y profesional de gestión bibliotecaria, demostrando buenas prácticas de programación y diseño de interfaces de usuario.


