class Usuario:
    """Clase base (molde) para todos los usuarios."""
    def __init__(self, id_usuario: str, nombre: str, correo: str, contrasena: str, ubicacion: str):
        # Use un solo guion bajo (_) para indicar que son datos protegidos
        # Guarda el identificador único del usuario (Ej: "USR-01", "R-100")
        self.id_usuario = id_usuario
        # Guarda el nombre de la persona o contacto principal (Ej: "Carlos Pérez")
        self.nombre = nombre
        # Guarda el correo electrónico para el inicio de sesión (Ej: "contacto@mail.com")
        self.correo = correo
        # Guarda la contraseña en texto plano para validar acceso (Ej: "pass123")
        self.contrasena = contrasena
        # Guarda la dirección o zona geográfica para el algoritmo de cercanía (Ej: "Zona Centro")
        self.ubicacion = ubicacion

    def autenticar(self, correo: str, contrasena: str) -> bool:
        """Compara si el correo y contraseña ingresados son correctos."""
        return self.correo == correo and self.contrasena == contrasena



class Restaurante(Usuario):
    """Hijo 1: Donante de comida."""
    def __init__(self, id_usuario: str, nombre: str, correo: str, contrasena: str, ubicacion: str, razon_social: str):
        # super().__init__() es una instrucción que sirve para llamar al constructor de la clase padre (la superclase) desde una clase hija.
        # super().__init__ copia automáticamente los datos del padre
        super().__init__(id_usuario, nombre, correo, contrasena, ubicacion)
        # Guarda el nombre legal o comercial del negocio (Ej: "Pizzería Don S.A.")
        self.razon_social: str = razon_social
        # Lista vacía para guardar sus donaciones
        # US-04: Lista que guardará los objetos completos de tipo 'Donacion' que este restaurante publique
        self.donaciones_realizadas: list = [] 

    def rol(self) -> str:
        return "Restaurante"


class Fundacion(Usuario):
    """Hijo 2: Receptor de comida."""
    def __init__(self, id_usuario: str, nombre: str, correo: str, contrasena: str, ubicacion: str, capacidad_kg: float):
        # super().__init__() es una instrucción que sirve para llamar al constructor de la clase padre (la superclase) desde una clase hija.
        super().__init__(id_usuario, nombre, correo, contrasena, ubicacion)
        # Guarda el límite máximo de peso en kg que la fundación puede recibir o almacenar (Ej: 500.0)
        self.capacidad_kg: float = capacidad_kg
        # Lista vacía para guardar sus apartados
        # US-05: Lista que guardará los objetos completos de tipo 'Donacion' que la fundación decida reservar
        self.reservas: list = []

    def rol(self) -> str:
        return "Fundación"


class Administrador(Usuario):
    """Hijo 3: Supervisor del sistema."""
    # Como no tiene atributos nuevos, no necesita un __init__ propio.
    # Python hereda automáticamente todo el del padre.

    def rol(self) -> str:
        return "Administrador"
