# 📦 Trabajo Práctico: Sistema de Gestión de Inventario Empresarial con DearPyGUI y SQLite

---

## 📝 Consigna

Desarrolla una **aplicación empresarial con interfaz gráfica**  usando DearPyGUI que permita gestionar un inventario completo. El sistema debe permitir administrar productos, categorías, proveedores y movimientos de stock con funcionalidades avanzadas como alertas automáticas, códigos de barras y análisis visual de tendencias. Los datos deben almacenarse en una base de datos **SQLite** con validaciones robustas.

Usar como base del proyecto los archivos que están dentro de la carpeta "biblio", adaptándolos para el contexto empresarial.
Cambiar el logo por uno que se relacione con gestión de inventario/almacén.

---

## 📋 Requisitos

### 1. **Datos de los productos**

- Cada producto debe tener al menos los siguientes campos:
- **Obligatorio:** El código de barras debe estar presente y ser la **clave primaria**.

| Campos del producto                        |
| ------------------------------------------ |
| Código de barras (clave primaria)         |
| Nombre del producto                        |
| Descripción                               |
| Categoría (ID foránea)                   |
| Proveedor (ID foránea)                    |
| Stock actual                               |
| Stock mínimo (para alertas)               |
| Precio de compra                           |
| Precio de venta                            |
| Fecha de ingreso                           |
| Imagen del producto (ruta archivo)         |
| **created_at** (timestamp)           |
| **updated_at** (timestamp)           |
| **deleted_at** (timestamp, nullable) |

### 2. **Datos de las categorías**

- Cada categoría debe tener al menos los siguientes campos:

| Campos de la categoría                    |
| ------------------------------------------ |
| ID (clave primaria)                        |
| Nombre                                     |
| Descripción                               |
| Color identificador                        |
| **created_at** (timestamp)           |
| **updated_at** (timestamp)           |
| **deleted_at** (timestamp, nullable) |

### 3. **Datos de los proveedores**

- Cada proveedor debe registrar:

| Campos del proveedor                       |
| ------------------------------------------ |
| ID (clave primaria)                        |
| Nombre/Razón social                       |
| CUIT/RUT                                   |
| Dirección                                 |
| Teléfono                                  |
| Email                                      |
| Contacto responsable                       |
| **created_at** (timestamp)           |
| **updated_at** (timestamp)           |
| **deleted_at** (timestamp, nullable) |

### 4. **Datos de movimientos de stock**

- Cada movimiento debe registrar:

| Campos del movimiento                      |
| ------------------------------------------ |
| ID (clave primaria)                        |
| Código de barras producto                 |
| Tipo (Entrada/Salida/Ajuste)               |
| Cantidad                                   |
| Precio unitario                            |
| Motivo/Descripción                        |
| Usuario responsable                        |
| Número de documento/factura               |
| **created_at** (timestamp)           |
| **updated_at** (timestamp)           |
| **deleted_at** (timestamp, nullable) |

---

## 🖥️ Interfaz Gráfica Avanzada

### **Uso obligatorio de Tabs (pestañas) para organizar secciones:**

#### **📦 Tab 1: Gestión de Productos**

- ➕ Agregar productos con validación de código de barras
- 📄 Listar productos con filtros avanzados
- ✏️ Modificar productos
- 🗑️ **Soft Delete** productos (marcar como eliminados sin borrar físicamente)
- 🔍 Búsqueda por código de barras, nombre o categoría
- 📸 Carga y visualización de imágenes de productos
- ⚠️ **Alertas visuales** para productos con stock bajo

#### **🏷️ Tab 2: Gestión de Categorías**

- ➕ Agregar categorías con selector de color
- 📄 Listar categorías
- ✏️ Modificar categorías
- 🗑️ **Soft Delete** categorías (validar que no tengan productos activos)

#### **🏭 Tab 3: Gestión de Proveedores**

- ➕ Agregar proveedores con validación de CUIT/RUT
- 📄 Listar proveedores
- ✏️ Modificar proveedores
- 🗑️ **Soft Delete** proveedores (validar que no tengan productos activos)

#### **📊 Tab 4: Control de Stock**

- ➕ Registrar entrada de mercadería
- ➖ Registrar salida de productos
- 🔄 Ajustes de inventario
- 📋 Historial completo de movimientos
- 🔍 Filtros por fecha, tipo de movimiento, producto

#### **📈 Tab 5: Dashboard y Reportes**

- **📊 Gráficos obligatorios usando plots:**
  - Tendencias de stock por producto
  - Movimientos mensuales
  - Productos más vendidos
  - Alertas de stock crítico
- 📋 Reportes de productos con stock bajo
- 💰 Cálculo automático de valor total del inventario
- 📤 **Exportación obligatoria** a PDF

---

## 🔧 Características Técnicas Avanzadas

### **Códigos de Barras (simulados)**

- Generación automática de códigos de barras válidos
- Validación de formato de código de barras
- Búsqueda rápida por código de barras

### **Cálculos Automáticos**

- Valor total del inventario en tiempo real
- Ganancia potencial por producto
- Rotación de stock
- Punto de reorden automático

### **Validaciones Numéricas Robustas**

- Precios no negativos
- Stock mínimo menor que máximo
- Cantidades enteras para productos no fraccionables
- CUIT/RUT con algoritmo de validación

### **Manejo de Imágenes**

- Carga de imágenes de productos
- Redimensionamiento automático
- Formatos soportados: JPG, PNG, BMP
- Imagen por defecto si no se carga ninguna

### **Exportación de Datos**

- Exportar reportes a PDF con formato
- Exportar movimientos por rango de fechas

---

## 🗄️ Base de Datos

- Utilizar SQLite para almacenar los datos.
- Crear las siguientes tablas con sus relaciones:
  - `productos` (código de barras como PK)
  - `categorias` (ID como PK)
  - `proveedores` (ID como PK)
  - `movimientos_stock` (ID como PK, FK a productos)

### **🗑️ Implementación de Soft Delete**

- **NUNCA** eliminar registros físicamente de la base de datos
- Usar **`deleted_at`** para marcar registros como eliminados
- **Filtrar automáticamente** registros eliminados en consultas SELECT
- **Permitir recuperación** de registros eliminados accidentalmente
- **Auditoría completa** con `created_at` y `updated_at` en todas las tablas

### **🔧 Configuración de Base de Datos**

- **Índices** para optimizar búsquedas frecuentes y filtros por `deleted_at`
- **Triggers** para:
  - Actualizar `updated_at` automáticamente en cada modificación
  - Actualizar stock automáticamente en movimientos
  - Validar que no se eliminen registros con dependencias activas
- **Constraints** para validar integridad referencial
- **Views** para simplificar consultas sin registros eliminados

---

## 💻 Código y Arquitectura

- Código **completamente comentado** y **organizado en módulos**
- **Clases separadas** para cada entidad (Producto, Proveedor, etc.)
- **Validadores** independientes para cada tipo de dato
- **Manejo robusto de errores** con try-catch
- **Logging** de operaciones críticas
- **Configuración** mediante archivos externos

### **🔄 Implementación de Soft Delete en Código**

- **BaseModel** con métodos comunes para todas las entidades:
  - `create()` - Establece `created_at` automáticamente
  - `update()` - Actualiza `updated_at` automáticamente
  - `soft_delete()` - Marca `deleted_at` sin eliminar físicamente
  - `restore()` - Restaura registros eliminados (deleted_at = NULL)
  - `get_active()` - Filtra automáticamente registros no eliminados
  - `get_deleted()` - Obtiene solo registros eliminados
  - `get_all_including_deleted()` - Obtiene todos los registros
- **Validaciones** antes de soft delete (ej: productos con stock > 0)
- **Cascada inteligente** para relaciones (marcar dependencias como inactivas)

---

## 📦 Entregables

- ✅ Código fuente completo y funcional
- ✅ Base de datos SQLite con **datos de prueba realistas** (mínimo 50 productos, 10 categorías, 5 proveedores)
- ✅ Carpeta con **imágenes de productos de ejemplo**
- ✅ Capturas de pantalla de cada tab funcionando
- ✅ Documentación técnica con diagramas de base de datos
- ✅ Archivos pdf de  de ejemplo exportados
- ✅ **README.md** con instrucciones de instalación y uso
- ✅ Entrega en repositorio GitHub con commits descriptivos

## 🛠️ Desafíos Técnicos Obligatorios

### **Validación Avanzada**

- ✅ Implementar validador de códigos de barras EAN-13
- ✅ Validación de CUIT/RUT con dígito verificador
- ✅ Control de tipos de datos numéricos con decimales
- ✅ Validación de emails con regex

### **Performance y Escalabilidad**

- ✅ Paginación en listas con más de 100 elementos
- ✅ Índices de base de datos para búsquedas rápida.

---

## ⏰ Cronograma Sugerido

- **Semana 1-2:** Diseño de base de datos y arquitectura básica
- **Semana 3-4:** Implementación de CRUD básico y interfaz con tabs
- **Semana 5-6:** Funcionalidades avanzadas (plots, validaciones, imágenes)
- **Semana 7-8:** Exportación, alertas y refinamiento de UX
- **Semana 9:** Testing, documentación y video demo

---

<div align="center">
   <h2>🚀 ¡A construir una aplicación de nivel empresarial! 💼</h2>
   <p><em>Este proyecto te preparará para desarrollos profesionales reales</em></p>
</div>
