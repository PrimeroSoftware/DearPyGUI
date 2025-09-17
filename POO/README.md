# 📚 Programación Orientada a Objetos (POO) en Python

Este directorio contiene material educativo y ejemplos prácticos sobre los conceptos fundamentales de la Programación Orientada a Objetos en Python.

## 📁 Contenido del Directorio

### 📄 Archivos de Código

- **`EjBibiblioPOO.py`** - Ejemplo completo de aplicación de los cuatro pilares de la POO implementado como un sistema de biblioteca

### 📖 Material Teórico (PDFs)

- **`POO en Python - Abstracción.pdf`** - Conceptos y ejemplos del pilar de Abstracción
- **`POO en Python - Encapsulación.pdf`** - Conceptos y ejemplos del pilar de Encapsulación
- **`POO en Python - Herencia.pdf`** - Conceptos y ejemplos del pilar de Herencia
- **`POO en Python - Polimorfismo.pdf`** - Conceptos y ejemplos del pilar de Polimorfismo
- **`POO en Python con ejemplo completo.pdf`** - Guía completa integrando todos los conceptos

## 🎯 Ejemplo Principal: Sistema de Biblioteca

El archivo `EjBibiblioPOO.py` implementa un sistema de gestión de biblioteca que demuestra los **cuatro pilares fundamentales de la POO**:

### 🔐 1. Encapsulación

- **Atributos privados**: Uso de `__` (name mangling) para proteger datos críticos
- **Atributos protegidos**: Uso de `_` para convención de acceso interno
- **Properties**: Control de acceso a través de métodos getter
- **Métodos internos**: Funcionalidad oculta al usuario final

```python
class Libro:
    def __init__(self, titulo, autor, paginas, isbn):
        self._titulo = titulo        # Protegido
        self.__isbn = isbn          # Privado
        self.__disponible = True    # Privado
  
    @property
    def isbn(self):
        return self.__isbn          # Acceso controlado
```

### 🎭 2. Abstracción

- **Interfaz pública**: Métodos simples para el usuario (`prestar()`, `devolver()`)
- **Complejidad oculta**: Implementación interna transparente al usuario
- **Simplicidad**: El usuario no necesita conocer detalles de almacenamiento

```python
def prestar(self):
    if self.__disponible:
        self.__disponible = False
        return f"Préstamo exitoso: {self._titulo}"
    return f"No disponible: {self._titulo}"
```

### 👨‍👩‍👧‍👦 3. Herencia

- **Clase base**: `Libro` como clase padre
- **Clases derivadas**: `LibroDigital` y `LibroAudio` heredan de `Libro`
- **Relación "es-un"**: Un LibroDigital ES UN Libro
- **Reutilización**: Aprovechamiento del código de la clase padre

```python
class LibroDigital(Libro):
    def __init__(self, titulo, autor, paginas, isbn, formato, tamanio_mb):
        super().__init__(titulo, autor, paginas, isbn)  # Herencia
        self.__formato = formato
        self.__tamanio_mb = tamanio_mb
```

### 🎪 4. Polimorfismo

- **Métodos sobrescritos**: Cada tipo de libro implementa `prestar()` de forma diferente
- **Interfaz común**: Todos los libros responden a los mismos métodos
- **Comportamiento dinámico**: El mismo código funciona para diferentes tipos

```python
# Cada tipo responde diferente al mismo método
libro_fisico.prestar()    # → "Préstamo exitoso: ..."
libro_digital.prestar()   # → "Descarga #1 de ..."
libro_audio.prestar()     # → Comportamiento específico para audio
```

## 🏗️ Estructura del Sistema

```
Sistema de Biblioteca
│
├── Libro (Clase Base)
│   ├── Atributos: título, autor, páginas, ISBN, disponibilidad
│   └── Métodos: prestar(), devolver(), propiedades
│
├── LibroDigital (Hereda de Libro)
│   ├── Atributos adicionales: formato, tamaño, descargas
│   └── Métodos específicos: generar_licencia()
│
├── LibroAudio (Hereda de Libro)
│   ├── Atributos adicionales: duración, narrador
│   └── Métodos específicos: reproducir()
│
└── Biblioteca (Composición)
    ├── Catálogo de libros
    └── Operaciones: agregar, buscar, prestar
```

## 🚀 Cómo Ejecutar el Ejemplo

```bash
# Navegar al directorio POO
cd POO

# Ejecutar el ejemplo
python EjBibiblioPOO.py
```

### Salida Esperada:

```
Libro agregado: Cien años de soledad
Libro agregado: Python Crash Course
Libro agregado: El Principito

=== Préstamos ===
Préstamo exitoso: Cien años de soledad
Descarga #1 de Python Crash Course (PDF)
Préstamo exitoso: El Principito

=== Biblioteca Central ===
ID 1: Cien años de soledad (García Márquez) - 432 págs.
ID 2: Python Crash Course (Eric Matthes) - 544 págs. [Digital: PDF, 15.5MB]
ID 3: El Principito (Antoine de Saint-Exupéry) - 96 págs. [Audio: 2.5h - Narrado por Pedro Pascal]

=== Búsqueda ===
ID 1: Cien años de soledad (García Márquez) - 432 págs.
```

## 💡 Conceptos Clave Demostrados

### Beneficios de la POO Aplicados:

1. **Mantenibilidad**: Código organizado en clases lógicas
2. **Reutilización**: Herencia evita duplicación de código
3. **Extensibilidad**: Fácil agregar nuevos tipos de libros
4. **Seguridad**: Encapsulación protege datos críticos
5. **Simplicidad**: Abstracción oculta complejidad interna

### Patrones de Diseño Utilizados:

- **Composición**: La biblioteca contiene libros
- **Herencia**: Especialización de tipos de libros
- **Polimorfismo**: Interfaz uniforme para diferentes tipos
- **Encapsulación**: Protección de datos internos

## 📚 Recursos de Aprendizaje

Los archivos PDF incluidos cubren:

- **Conceptos teóricos** de cada pilar de la POO
- **Ejemplos prácticos** en Python
- **Mejores prácticas** y patrones comunes
- **Ejercicios** para reforzar el aprendizaje

## 🎓 Objetivos de Aprendizaje

Al estudiar este material, podrás:

1. ✅ Entender y aplicar los cuatro pilares de la POO
2. ✅ Diseñar clases con encapsulación apropiada
3. ✅ Implementar herencia y polimorfismo efectivamente
4. ✅ Crear abstracciones útiles y mantenibles
5. ✅ Aplicar conceptos POO en proyectos reales
