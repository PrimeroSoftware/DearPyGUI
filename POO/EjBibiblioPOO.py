# #############################
# ## REGLAS DE ORO APLICADAS ##
# #############################

# 1. ENCAPSULACIÓN:
#   - Atributos privados (__) y protegidos (_)
#   - Uso de properties para acceso controlado
#   - Métodos internos ocultos

# 2. ABSTRACCIÓN:
#   - El usuario solo interactúa con métodos públicos
#   - No necesita saber cómo se almacenan los libros

# 3. HERENCIA:
#   - LibroDigital y LibroAudio heredan de Libro
#   - Relación clara "es-un"

# 4. POLIMORFISMO:
#   - Todos responden a prestar() y __str__()
#   - La biblioteca trata todos los libros igual

class Libro:
    # Atributo de clase (privado con name mangling)
    __contador_libros = 0
    
    def __init__(self, titulo, autor, paginas, isbn):
        # Atributos protegidos (convención _)
        self._titulo = titulo
        self._autor = autor
        self._paginas = paginas
        
        # Atributo privado (name mangling)
        self.__isbn = isbn  
        self.__disponible = True
        
        # Control interno con encapsulación
        Libro.__contador_libros += 1
        self.__id = Libro.__contador_libros
    
    # === Métodos públicos (interfaz abstracta) ===
    def prestar(self):
        if self.__disponible:
            self.__disponible = False
            return f"Préstamo exitoso: {self._titulo}"
        return f"No disponible: {self._titulo}"
    
    def devolver(self):
        self.__disponible = True
        return f"Devolución registrada: {self._titulo}"
    
    # === Métodos especiales para polimorfismo ===
    def __str__(self):
        return f"ID {self.__id}: {self._titulo} ({self._autor}) - {self._paginas} págs."
    
    # === Propiedades para acceso controlado ===
    @property
    def isbn(self):
        return self.__isbn
    
    @property
    def disponible(self):
        return self.__disponible
    
    @property
    def id(self):
        return self.__id

    # === Método estático (no depende de instancia) ===
    @staticmethod
    def validar_isbn(isbn):
        return len(isbn) in (10, 13)


class LibroDigital(Libro):
    def __init__(self, titulo, autor, paginas, isbn, formato, tamanio_mb):
        # Herencia del constructor padre
        super().__init__(titulo, autor, paginas, isbn)
        
        # Nuevos atributos privados
        self.__formato = formato
        self.__tamanio_mb = tamanio_mb
        self.__descargas = 0
    
    # === Polimorfismo: Sobrescritura de métodos ===
    def prestar(self):
        self.__descargas += 1
        return f"Descarga #{self.__descargas} de {self._titulo} ({self.__formato})"
    
    def __str__(self):
        # Reutilización del método padre + extensión
        return f"{super().__str__()} [Digital: {self.__formato}, {self.__tamanio_mb}MB]"
    
    # === Nuevos métodos específicos ===
    def generar_licencia(self, dias):
        return f"Licencia de {dias} días para {self._titulo}"


class LibroAudio(Libro):
    def __init__(self, titulo, autor, paginas, isbn, duracion_horas, narrador):
        super().__init__(titulo, autor, paginas, isbn)
        self.__duracion = duracion_horas
        self.__narrador = narrador
    
    # Polimorfismo
    def __str__(self):
        return f"{super().__str__()} [Audio: {self.__duracion}h - Narrado por {self.__narrador}]"
    
    def reproducir(self):
        return f"Reproduciendo {self._titulo}..."


class Biblioteca:
    def __init__(self, nombre):
        self.__nombre = nombre
        self.__catalogo = []  # Lista privada de libros
    
    # === Interfaz pública (abstracción) ===
    def agregar_libro(self, libro):
        if isinstance(libro, Libro) and Libro.validar_isbn(libro.isbn):
            self.__catalogo.append(libro)
            return f"Libro agregado: {libro._titulo}"
        return "Error: Libro no válido"
    
    def buscar_por_titulo(self, texto):
        return [libro for libro in self.__catalogo if texto.lower() in libro._titulo.lower()]
    
    def prestar_libro(self, id_libro):
        for libro in self.__catalogo:
            if libro.id == id_libro:
                return libro.prestar()  # Polimorfismo en acción
        return "Libro no encontrado"
    
    # === Método especial ===
    def __str__(self):
        return f"\n=== {self.__nombre} ===\n" + \
               "\n".join(str(libro) for libro in self.__catalogo)


# ==============
# == EJEMPLO ==
# ==============
if __name__ == "__main__":
    # Crear biblioteca
    biblio = Biblioteca("Biblioteca Central")
    
    # Crear libros (polimorfismo)
    libros = [
        Libro("Cien años de soledad", "García Márquez", 432, "9780307474728"),
        LibroDigital("Python Crash Course", "Eric Matthes", 544, "9781593279288", "PDF", 15.5),
        LibroAudio("El Principito", "Antoine de Saint-Exupéry", 96, "9780156013925", 2.5, "Pedro Pascal")
    ]
    
    # Agregar libros
    for libro in libros:
        print(biblio.agregar_libro(libro))
    
    # Procesar préstamos (polimorfismo)
    print("\n=== Préstamos ===")
    for libro in libros:
        print(libro.prestar())  # Cada tipo responde diferente
    
    # Mostrar catálogo
    print(biblio)
    
    # Buscar libros
    print("\n=== Búsqueda ===")
    resultados = biblio.buscar_por_titulo("cien")
    for libro in resultados:
        print(libro)