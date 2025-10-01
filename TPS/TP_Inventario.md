# 📦 Trabajo Práctico: Sistema de Gestión de Inventario Empresarial

**Entrega Final - Sistema Completado**

---

## 📝 Descripción del Proyecto Realizado

Se ha desarrollado un **sistema completo de gestión de inventario empresarial** utilizando DearPyGUI para la interfaz gráfica y SQLite como base de datos. El sistema permite administrar productos, categorías, proveedores y movimientos de stock con funcionalidades avanzadas de validación, reportes y exportación.

El proyecto se basa en la adaptación de los archivos de la carpeta "biblio", transformándolos para un contexto empresarial de gestión de inventario. Se cambió el logo por uno relacionado con almacén/inventario.

---

## 🏗️ Arquitectura del Sistema

### **Estructura de Módulos (sugerida)**

```
inventario/
├── main.py                 # Archivo principal - punto de entrada
├── inventario.db          # Base de datos SQLite
├── logo.png               # Logo del sistema
├── modules/               # Módulos del sistema
│   ├── __init__.py
│   ├── base_model.py      # Modelo base con soft delete
│   ├── productos_manager.py   # Gestión de productos
│   ├── categorias_manager.py  # Gestión de categorías
│   ├── proveedores_manager.py # Gestión de proveedores
│   ├── movimientos_manager.py # Gestión de movimientos
│   ├── sqlstatements.py       # SQL almacenados para uso en la app
│   └── database_manager.py    # Gestor de base de datos
├── lib/                   # Librerías auxiliares
│   └── myfunctions/
│       ├── __init__.py
│       └── myscreen.py    # Utilidades de pantalla
└──  images/                # Imágenes de productos
```

### **Tecnologías Utilizadas**

- **Lenguaje**: Python 3.13
- **Interfaz Gráfica**: DearPyGUI
- **Base de Datos**: SQLite
- **Generación de PDFs**: ReportLab
- **Manejo de Imágenes**: Pillow (PIL)

---

## �️ Base de Datos - Diseño e Implementación

### **Tablas Implementadas**

#### **1. productos**

```sql
CREATE TABLE productos (
    codigo_barras TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    categoria_id INTEGER,
    proveedor_id INTEGER,
    stock_actual INTEGER DEFAULT 0,
    stock_minimo INTEGER DEFAULT 0,
    precio_compra REAL,
    precio_venta REAL,
    ubicacion TEXT,
    imagen TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id),
    FOREIGN KEY (proveedor_id) REFERENCES proveedores(id)
);
```

#### **2. categorias**

```sql
CREATE TABLE categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT,
    color TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);
```

#### **3. proveedores**

```sql
CREATE TABLE proveedores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    cuit TEXT UNIQUE,
    direccion TEXT,
    telefono TEXT,
    email TEXT,
    contacto TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);
```

#### **4. movimientos_stock**

```sql
CREATE TABLE movimientos_stock (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_codigo TEXT NOT NULL,
    tipo TEXT NOT NULL, -- 'ENTRADA', 'SALIDA', 'AJUSTE'
    cantidad INTEGER NOT NULL,
    precio_unitario REAL,
    descripcion TEXT,
    documento TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,
    FOREIGN KEY (producto_codigo) REFERENCES productos(codigo_barras)
);
```

### **Soft Delete Implementado**

- **Nunca se eliminan registros físicamente**
- Campo `deleted_at` marca registros como eliminados
- Consultas filtran automáticamente registros eliminados
- Métodos `soft_delete()` y `restore()` en BaseModel

### **Índices y Optimización**

```sql
-- Índices para búsquedas frecuentes
CREATE INDEX idx_productos_categoria ON productos(categoria_id);
CREATE INDEX idx_productos_proveedor ON productos(proveedor_id);
CREATE INDEX idx_productos_deleted ON productos(deleted_at);
CREATE INDEX idx_movimientos_producto ON movimientos_stock(producto_codigo);
CREATE INDEX idx_movimientos_fecha ON movimientos_stock(created_at);
```

---

## 🖥️ Interfaz Gráfica Implementada

### **Sistema de Pestañas (Tabs)**

#### **📊 Dashboard**

- **Métricas del sistema**: Total productos, categorías, proveedores
- **Productos con stock bajo**: Tabla con alertas visuales
- **Últimos movimientos**: Historial reciente
- **Botón actualizar**: Refresca todas las métricas

#### **📦 Productos**

- **Tabla principal**: Lista todos los productos con paginación
- **Botones CRUD**: Agregar, editar, eliminar (soft delete)
- **Filtros**: Por nombre, categoría, stock bajo
- **Modal de formulario**: Campos validados para agregar/editar
- **Imágenes**: Carga y visualización de fotos de productos

#### **🏷️ Categorías**

- **Gestión completa**: CRUD con validaciones
- **Selector de color**: Para identificación visual
- **Validación de unicidad**: Nombres únicos
- **Soft delete**: Solo si no hay productos activos

#### **🏢 Proveedores**

- **Registro completo**: Datos de contacto y fiscales
- **Validación CUIT**: Formato básico implementado
- **Búsqueda y filtros**: Por nombre, CUIT
- **Soft delete**: Con validaciones de dependencias

#### **📈 Movimientos**

- **Registro de movimientos**: Entrada, salida, ajustes
- **Actualización automática de stock**: Triggers en BD
- **Historial completo**: Con filtros por fecha y tipo
- **Documentos**: Referencias a facturas/comprobantes

---

## 🔧 Funcionalidades Técnicas Implementadas

### **Validaciones Implementadas**

- **Campos obligatorios**: Nombre, código de barras, etc.
- **Formatos numéricos**: Precios, stocks como números
- **Unicidad**: Códigos de barras, nombres de categorías
- **Relaciones**: Validación de claves foráneas
- **Soft delete**: Validaciones antes de eliminar

### **Gestión de Imágenes**

- **Carga de archivos**: JPG, PNG soportados
- **Almacenamiento**: En carpeta `images/`
- **Visualización**: En modales y tablas
- **Imagen por defecto**: Si no se carga ninguna

### **Reportes y Exportación**

- **PDFs generados**: Reportes de productos, categorías, proveedores, stock bajo
- **Excel exportable**: Inventario completo
- **Formatos profesionales**: Con logos y encabezados

### **Sistema de Temas**

- **Temas personalizados**: Verde (aceptar), rojo (cancelar), azul (exportar), etc.
- **UI Manager centralizado**: Aplicación consistente de estilos
- **Tab bar gris oscuro**: Para navegación

---

## 💻 Código - Arquitectura y Patrones

### **BaseModel - Clase Base**

```python
class BaseModel:
    def __init__(self, table_name):
        self.table_name = table_name
        self.db_manager = DatabaseManager()

    def create(self, data):
        # Implementa inserción con timestamps

    def update(self, id_value, data):
        # Actualiza con updated_at automático

    def soft_delete(self, id_value):
        # Marca como eliminado sin borrar

    def get_active(self):
        # Filtra deleted_at IS NULL

    def restore(self, id_value):
        # Restaura registro eliminado
```

### **Managers Especializados**

Cada módulo tiene su manager con métodos específicos:

- `ProductosManager`: CRUD productos + validaciones stock
- `CategoriasManager`: Gestión categorías + colores
- `ProveedoresManager`: Gestión proveedores + validaciones CUIT
- `MovimientosManager`: Registro movimientos + actualización stock

### **UIManager - Interfaz Centralizada**

- **Configuración de temas globales**
- **Creación de interfaz completa**
- **Aplicación automática de estilos**
- **Gestión de layouts y pestañas**

### **DatabaseManager - Abstracción de BD**

- **Conexiones seguras**
- **Métodos genéricos**: select, insert, update, delete
- **Manejo de transacciones**
- **Logging de consultas**

---

## 📊 Datos de Prueba Incluidos

### **Categorías de Ejemplo**

- Electrónicos
- Ropa y Accesorios
- Alimentos
- Limpieza
- Oficina

### **Proveedores Registrados**

- TechSolutions S.A.
- Distribuidora General
- Almacén Central
- Proveedores Unidos

### **Productos de Muestra**

- Más de 50 productos con códigos de barras únicos
- Imágenes representativas
- Stocks variados (algunos bajos para testing)
- Precios realistas

### **Movimientos Históricos**

- Entradas iniciales
- Salidas de ventas
- Ajustes de inventario

---

## 🚀**Carga de Datos Iniciales**

```bash
# Ejecutar script de datos de prueba
python datos_prueba.py
```

### **Uso del Sistema**

1. **Dashboard**: Vista general y métricas
2. **Productos**: Gestión del catálogo
3. **Categorías**: Administración de clasificaciones
4. **Proveedores**: Gestión de suministradores
5. **Movimientos**: Control de stock

---

## 📈 Características Avanzadas Implementadas

### **Validaciones**

- ✅ Campos obligatorios
- ✅ Tipos de datos correctos
- ✅ Unicidad de claves
- ✅ Relaciones referenciales
- ✅ No validaciones avanzadas (como solicitado)

### **Interfaz de Usuario**

- ✅ Pestañas organizadas
- ✅ Temas personalizados
- ✅ Diálogos modales
- ✅ Tablas con filtros
- ✅ UI adjunta en imágenes

### **Base de Datos**

- ✅ SQLite con relaciones
- ✅ Soft delete implementado
- ✅ Índices de optimización
- ✅ Triggers automáticos

### **Funcionalidades**

- ✅ CRUD completo
- ✅ Reportes PDF
- ✅ Gestión de imágenes
- ✅ Control de stock

---

## ⏰ Información del Proyecto

- **Tiempo de entrega**: 2 semanas
- **Validaciones**: Solo estándar (no avanzadas)
- **Interfaz**: Adjunta en imágenes
- **Datos iniciales**: Set de datos incluido para carga inicial

---

## 📋 Entregables Completados

- ✅ Código fuente completo y funcional
- ✅ Base de datos SQLite con datos de prueba
- ✅ Carpeta con imágenes de productos
- ✅ Sistema de temas y UI profesional
- ✅ Reportes PDF generados
- ✅ README.md con documentación
- ✅ Arquitectura modular y comentada
- ✅ Soft delete implementado
- ✅ Validaciones estándar
- ✅ Exportación de datos

---

<div align="center">
   <h2>🚀 ¡A construir una aplicación de nivel empresarial! 💼</h2>
   <p><em>Este proyecto te preparará para desarrollos profesionales reales</em></p>
</div>
