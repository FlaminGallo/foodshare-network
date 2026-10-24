# logica.py
from datetime import datetime
from abc import ABC
from datos_demo import USUARIOS_DEMO, DONACIONES_DEMO

# --- MODELO POO ---
class Usuario(ABC):
    def __init__(self, id_usuario, nombre, correo, contrasena, ubicacion):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.correo = correo
        self.contrasena = contrasena
        self.ubicacion = ubicacion

class Restaurante(Usuario):
    def __init__(self, id_usuario, nombre, correo, contrasena, ubicacion, razon_social):
        super().__init__(id_usuario, nombre, correo, contrasena, ubicacion)
        self.razon_social = razon_social
        self.rol = "restaurante"

class Fundacion(Usuario):
    def __init__(self, id_usuario, nombre, correo, contrasena, ubicacion, capacidad_kg):
        super().__init__(id_usuario, nombre, correo, contrasena, ubicacion)
        self.capacidad_kg = capacidad_kg
        self.rol = "fundacion"

class Administrador(Usuario):
    def __init__(self, id_usuario, nombre, correo, contrasena, ubicacion):
        super().__init__(id_usuario, nombre, correo, contrasena, ubicacion)
        self.rol = "admin"

class Alimento:
    def __init__(self, nombre, peso_kg, fecha_vencimiento):
        self.nombre = nombre
        self.peso_kg = float(peso_kg)
        self.fecha_vencimiento = datetime.strptime(fecha_vencimiento, "%d/%m/%Y").date()

class Donacion:
    def __init__(self, id_donacion, descripcion, fecha_creacion, estado, alimentos, donante, reservado_por=None):
        self.id_donacion = id_donacion
        self.descripcion = descripcion
        self.fecha_creacion = datetime.strptime(fecha_creacion, "%d/%m/%Y").date()
        self.estado = estado
        self.alimentos = alimentos
        self.donante = donante
        self.reservado_por = reservado_por

    @property
    def peso_total(self):
        return sum(a.peso_kg for a in self.alimentos)

    @property
    def vencimiento_proximo(self):
        if not self.alimentos:
            return None
        return min(a.fecha_vencimiento for a in self.alimentos)
    
    @property
    def str_vencimiento(self):
        v = self.vencimiento_proximo
        return v.strftime("%d/%m/%Y") if v else ""

# --- CONTROLADOR / SISTEMA EN MEMORIA ---
class Sistema:
    def __init__(self):
        self.usuarios = []
        self.donaciones = []
        self._cargar_datos()

    def _cargar_datos(self):
        # Cargar usuarios
        for u in USUARIOS_DEMO:
            if u["rol"] == "restaurante":
                obj = Restaurante(u["id_usuario"], u["nombre"], u["correo"], u["contrasena"], u["ubicacion"], u["razon_social"])
            elif u["rol"] == "fundacion":
                obj = Fundacion(u["id_usuario"], u["nombre"], u["correo"], u["contrasena"], u["ubicacion"], u["capacidad_kg"])
            else:
                obj = Administrador(u["id_usuario"], u["nombre"], u["correo"], u["contrasena"], u["ubicacion"])
            self.usuarios.append(obj)

        # Cargar donaciones
        for d in DONACIONES_DEMO:
            alimentos = [Alimento(a["nombre"], a["peso_kg"], a["fecha_vencimiento"]) for a in d["alimentos"]]
            donante = self.obtener_usuario(d["donante_id"])
            reservado_por = self.obtener_usuario(d["reservado_por_id"])
            donacion = Donacion(d["id_donacion"], d["descripcion"], d["fecha_creacion"], d["estado"], alimentos, donante, reservado_por)
            self.donaciones.append(donacion)

    def obtener_usuario(self, id_usuario):
        for u in self.usuarios:
            if u.id_usuario == id_usuario:
                return u
        return None

    def autenticar(self, correo, contrasena):
        for u in self.usuarios:
            if u.correo == correo and u.contrasena == contrasena:
                return u
        return None

    def obtener_donaciones_por_estado(self, estados_permitidos):
        return [d for d in self.donaciones if d.estado in estados_permitidos]

    def obtener_donaciones_de_restaurante(self, id_restaurante):
        return [d for d in self.donaciones if isinstance(d.donante, Usuario) and d.donante.id_usuario == id_restaurante]

    def obtener_reservas_de_fundacion(self, id_fundacion):
        return [d for d in self.donaciones if d.reservado_por and d.reservado_por.id_usuario == id_fundacion]

sistema = Sistema()