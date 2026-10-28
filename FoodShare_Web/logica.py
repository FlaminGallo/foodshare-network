# logica.py
"""Modelo de FoodShare Network (Programación Orientada a Objetos).

Este archivo no sabe nada de páginas web: solo contiene las clases y
las reglas del negocio. app.py (Flask) las usa para mostrar pantallas.

Conceptos de POO que se aplican aquí:
- Abstracción: Usuario es una clase abstracta (no se puede instanciar).
- Herencia: Restaurante, Fundacion y Administrador heredan de Usuario.
- Polimorfismo: cada subclase responde distinto a `rol`, `etiqueta_rol`
  y `pantalla_inicio`.
- Encapsulamiento: la contraseña se guarda en un atributo "privado"
  (_contrasena) y solo se compara con verificar_contrasena().
- Composición: una Donacion está formada por varios objetos Alimento.
"""

from abc import ABC, abstractmethod
from datetime import date, datetime

from datos_demo import DONACIONES_DEMO, FECHA_DEMO, USUARIOS_DEMO

FORMATO_FECHA = "%d/%m/%Y"


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------
class ErrorFoodShare(Exception):
    """Error de una regla del negocio. Su mensaje se le muestra al usuario."""


def convertir_fecha(valor):
    """Convierte 'dd/mm/aaaa' (o un objeto date) a datetime.date."""
    if isinstance(valor, date):
        return valor
    try:
        return datetime.strptime(str(valor).strip(), FORMATO_FECHA).date()
    except ValueError:
        raise ErrorFoodShare("La fecha debe tener el formato dd/mm/aaaa.")


def formatear_fecha(fecha):
    """Convierte un datetime.date a texto 'dd/mm/aaaa'."""
    return fecha.strftime(FORMATO_FECHA) if fecha else ""


class Estado:
    """Nombres de los estados posibles de una donación."""

    PENDIENTE = "Pendiente de validación"
    DISPONIBLE = "Disponible"
    RESERVADA = "Reservada"
    RECIBIDA = "Recibida"
    VENCIDA = "Vencida"
    RECHAZADA = "Rechazada"

    TODOS = [PENDIENTE, DISPONIBLE, RESERVADA, RECIBIDA, VENCIDA, RECHAZADA]

    # Desde qué estado se puede pasar a cuál (máquina de estados).
    TRANSICIONES = {
        PENDIENTE: [DISPONIBLE, RECHAZADA, VENCIDA],
        DISPONIBLE: [RESERVADA, VENCIDA],
        RESERVADA: [RECIBIDA],
        RECIBIDA: [],
        VENCIDA: [],
        RECHAZADA: [],
    }


# ---------------------------------------------------------------------------
# Usuarios (herencia + clase abstracta)
# ---------------------------------------------------------------------------
class Usuario(ABC):
    """Clase base abstracta para todos los usuarios del sistema."""

    def __init__(self, id_usuario, nombre, correo, contrasena, ubicacion):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.correo = correo.strip().lower()
        self._contrasena = contrasena
        self.ubicacion = ubicacion

    def verificar_contrasena(self, contrasena):
        return self._contrasena == contrasena

    @property
    @abstractmethod
    def rol(self):
        """Identificador interno del rol: 'restaurante', 'fundacion' o 'admin'."""

    @property
    @abstractmethod
    def etiqueta_rol(self):
        """Texto que se muestra en la interfaz junto al nombre."""

    @abstractmethod
    def pantalla_inicio(self):
        """Nombre de la ruta de Flask a la que entra después de iniciar sesión."""

    def __repr__(self):
        return "{}({}, {})".format(type(self).__name__, self.id_usuario, self.nombre)


class Restaurante(Usuario):
    """Donante: publica excedentes de comida."""

    def __init__(self, id_usuario, nombre, correo, contrasena, ubicacion, razon_social):
        super().__init__(id_usuario, nombre, correo, contrasena, ubicacion)
        self.razon_social = razon_social

    @property
    def rol(self):
        return "restaurante"

    @property
    def etiqueta_rol(self):
        return "Restaurante"

    def pantalla_inicio(self):
        return "restaurante_panel"


class Fundacion(Usuario):
    """Receptor: reserva donaciones disponibles y confirma que las recibió."""

    def __init__(self, id_usuario, nombre, correo, contrasena, ubicacion, capacidad_kg):
        super().__init__(id_usuario, nombre, correo, contrasena, ubicacion)
        self.capacidad_kg = float(capacidad_kg)

    @property
    def rol(self):
        return "fundacion"

    @property
    def etiqueta_rol(self):
        return "Fundación"

    def pantalla_inicio(self):
        return "fundacion_explorar"


class Administrador(Usuario):
    """Valida (aprueba o rechaza) las donaciones antes de publicarlas."""

    @property
    def rol(self):
        return "admin"

    @property
    def etiqueta_rol(self):
        return "Administradora"

    def pantalla_inicio(self):
        return "admin_panel"


# ---------------------------------------------------------------------------
# Alimentos y donaciones (composición)
# ---------------------------------------------------------------------------
class Alimento:
    """Un alimento dentro de una donación."""

    def __init__(self, nombre, peso_kg, fecha_vencimiento, nutrientes=""):
        nombre = (nombre or "").strip()
        if not nombre:
            raise ErrorFoodShare("El nombre del alimento es obligatorio.")
        try:
            peso_kg = float(peso_kg)
        except (TypeError, ValueError):
            raise ErrorFoodShare("La cantidad debe ser un número.")
        if peso_kg <= 0:
            raise ErrorFoodShare("La cantidad debe ser mayor que 0 kg.")

        self.nombre = nombre
        self.peso_kg = round(peso_kg, 2)
        self.fecha_vencimiento = convertir_fecha(fecha_vencimiento)
        self.nutrientes = (nutrientes or "").strip()

    @property
    def str_vencimiento(self):
        return formatear_fecha(self.fecha_vencimiento)


class Donacion:
    """Conjunto de alimentos que un restaurante ofrece a las fundaciones."""

    def __init__(self, id_donacion, alimentos, donante, fecha_creacion,
                 estado=Estado.PENDIENTE, reservado_por=None, descripcion=None):
        if not alimentos:
            raise ErrorFoodShare("Una donación debe tener al menos un alimento.")
        if estado not in Estado.TODOS:
            raise ErrorFoodShare("Estado desconocido: {}".format(estado))
        self.id_donacion = id_donacion
        self.alimentos = list(alimentos)
        self.donante = donante
        self.fecha_creacion = convertir_fecha(fecha_creacion)
        self.estado = estado
        self.reservado_por = reservado_por
        self.fecha_recepcion = None
        self._descripcion = descripcion

    # --- Datos calculados -------------------------------------------------
    @property
    def descripcion(self):
        """Usa la descripción dada o, si no hay, los nombres de los alimentos."""
        if self._descripcion:
            return self._descripcion
        nombres = [a.nombre for a in self.alimentos]
        if len(nombres) <= 2:
            return " y ".join(nombres)
        return "{} y {} más".format(", ".join(nombres[:2]), len(nombres) - 2)

    @property
    def peso_total(self):
        return round(sum(a.peso_kg for a in self.alimentos), 2)

    @property
    def vencimiento_proximo(self):
        return min(a.fecha_vencimiento for a in self.alimentos)

    @property
    def str_vencimiento(self):
        return formatear_fecha(self.vencimiento_proximo)

    # --- Comportamiento ---------------------------------------------------
    def puede_cambiar_a(self, nuevo_estado):
        return nuevo_estado in Estado.TRANSICIONES[self.estado]

    def cambiar_estado(self, nuevo_estado):
        if not self.puede_cambiar_a(nuevo_estado):
            raise ErrorFoodShare(
                "La donación {} está {} y no puede pasar a {}.".format(
                    self.id_donacion, self.estado.lower(), nuevo_estado.lower()))
        self.estado = nuevo_estado

    def esta_vencida(self, hoy):
        return self.vencimiento_proximo < hoy

    def coincide_con(self, texto):
        """True si el texto aparece en el ID, la descripción, el donante o un alimento."""
        texto = (texto or "").strip().lower()
        if not texto:
            return True
        partes = [self.id_donacion, self.descripcion, self.donante.nombre]
        partes += [a.nombre for a in self.alimentos]
        return any(texto in parte.lower() for parte in partes)


# ---------------------------------------------------------------------------
# Sistema: guarda todo en memoria y aplica las reglas
# ---------------------------------------------------------------------------
class Sistema:
    """Controlador de la aplicación (versión 2.0, datos en memoria)."""

    def __init__(self, fecha_actual=None, cargar_demo=True):
        self._fecha_fija = fecha_actual
        self.usuarios = []
        self.donaciones = []
        if cargar_demo:
            self._cargar_datos()
        self.actualizar_vencidas()

    @property
    def hoy(self):
        return self._fecha_fija or date.today()

    # --- Carga inicial ----------------------------------------------------
    def _cargar_datos(self):
        for u in USUARIOS_DEMO:
            self.usuarios.append(self._crear_usuario_desde_dict(u))

        for d in DONACIONES_DEMO:
            alimentos = [Alimento(a["nombre"], a["peso_kg"], a["fecha_vencimiento"],
                                  a.get("nutrientes", "")) for a in d["alimentos"]]
            donacion = Donacion(
                d["id_donacion"], alimentos,
                donante=self.obtener_usuario(d["donante_id"]),
                fecha_creacion=d["fecha_creacion"],
                estado=d["estado"],
                reservado_por=self.obtener_usuario(d["reservado_por_id"]),
                descripcion=d.get("descripcion"),
            )
            self.donaciones.append(donacion)

    @staticmethod
    def _crear_usuario_desde_dict(u):
        if u["rol"] == "restaurante":
            return Restaurante(u["id_usuario"], u["nombre"], u["correo"], u["contrasena"],
                               u["ubicacion"], u["razon_social"])
        if u["rol"] == "fundacion":
            return Fundacion(u["id_usuario"], u["nombre"], u["correo"], u["contrasena"],
                             u["ubicacion"], u["capacidad_kg"])
        return Administrador(u["id_usuario"], u["nombre"], u["correo"], u["contrasena"],
                             u["ubicacion"])

    # --- Usuarios ---------------------------------------------------------
    def obtener_usuario(self, id_usuario):
        for u in self.usuarios:
            if u.id_usuario == id_usuario:
                return u
        return None

    def buscar_por_correo(self, correo):
        correo = (correo or "").strip().lower()
        for u in self.usuarios:
            if u.correo == correo:
                return u
        return None

    def autenticar(self, correo, contrasena):
        usuario = self.buscar_por_correo(correo)
        if usuario and usuario.verificar_contrasena(contrasena):
            return usuario
        return None

    def registrar_usuario(self, tipo, nombre, correo, contrasena, confirmacion,
                          ubicacion, razon_social="", capacidad_kg=""):
        """Crea una cuenta de Restaurante o Fundación (nunca de Administrador)."""
        nombre = (nombre or "").strip()
        correo = (correo or "").strip().lower()
        ubicacion = (ubicacion or "").strip()
        razon_social = (razon_social or "").strip()

        if tipo not in ("restaurante", "fundacion"):
            raise ErrorFoodShare("Elige un tipo de cuenta válido.")
        if not nombre or not correo or not ubicacion or not contrasena:
            raise ErrorFoodShare("Completa todos los campos obligatorios.")
        if "@" not in correo or "." not in correo.split("@")[-1]:
            raise ErrorFoodShare("Escribe un correo electrónico válido.")
        if self.buscar_por_correo(correo):
            raise ErrorFoodShare("Ya existe una cuenta con ese correo.")
        if len(contrasena) < 6:
            raise ErrorFoodShare("La contraseña debe tener al menos 6 caracteres.")
        if contrasena != confirmacion:
            raise ErrorFoodShare("Las contraseñas no coinciden.")

        nuevo_id = "U{:02d}".format(len(self.usuarios) + 1)
        if tipo == "restaurante":
            if not razon_social:
                raise ErrorFoodShare("La razón social es obligatoria para restaurantes.")
            usuario = Restaurante(nuevo_id, nombre, correo, contrasena, ubicacion, razon_social)
        else:
            try:
                capacidad = float(capacidad_kg)
            except (TypeError, ValueError):
                raise ErrorFoodShare("Escribe la capacidad de recepción en kg.")
            if capacidad <= 0:
                raise ErrorFoodShare("La capacidad de recepción debe ser mayor que 0 kg.")
            usuario = Fundacion(nuevo_id, nombre, correo, contrasena, ubicacion, capacidad)

        self.usuarios.append(usuario)
        return usuario

    def restaurantes(self):
        return [u for u in self.usuarios if isinstance(u, Restaurante)]

    # --- Consultas de donaciones -----------------------------------------
    def obtener_donacion(self, id_donacion):
        for d in self.donaciones:
            if d.id_donacion == id_donacion:
                return d
        return None

    def _exigir_donacion(self, id_donacion):
        donacion = self.obtener_donacion(id_donacion)
        if donacion is None:
            raise ErrorFoodShare("No existe la donación {}.".format(id_donacion))
        return donacion

    def todas_las_donaciones(self):
        """Más recientes primero (por ID)."""
        return sorted(self.donaciones, key=lambda d: d.id_donacion, reverse=True)

    def donaciones_por_estado(self, *estados):
        return [d for d in self.todas_las_donaciones() if d.estado in estados]

    def donaciones_de_restaurante(self, restaurante):
        return [d for d in self.todas_las_donaciones() if d.donante is restaurante]

    def reservas_de_fundacion(self, fundacion):
        return [d for d in self.todas_las_donaciones() if d.reservado_por is fundacion]

    @staticmethod
    def filtrar(donaciones, texto="", estado=""):
        """Filtra una lista por texto de búsqueda y por estado ('' = todos)."""
        resultado = [d for d in donaciones if d.coincide_con(texto)]
        if estado:
            resultado = [d for d in resultado if d.estado == estado]
        return resultado

    @staticmethod
    def peso_de(donaciones):
        return round(sum(d.peso_total for d in donaciones), 2)

    def siguiente_id(self):
        numeros = [int(d.id_donacion[3:]) for d in self.donaciones
                   if d.id_donacion[3:].isdigit()]
        return "DON{:03d}".format(max(numeros, default=0) + 1)

    def actualizar_vencidas(self):
        """Marca como Vencida lo que caducó antes de ser reservado."""
        cambiadas = []
        for d in self.donaciones:
            if d.estado in (Estado.PENDIENTE, Estado.DISPONIBLE) and d.esta_vencida(self.hoy):
                d.cambiar_estado(Estado.VENCIDA)
                cambiadas.append(d)
        return cambiadas

    # --- Acciones (cada una valida quién la hace) -------------------------
    def publicar_donacion(self, restaurante, alimentos):
        if not isinstance(restaurante, Restaurante):
            raise ErrorFoodShare("Solo un restaurante puede publicar donaciones.")
        if not alimentos:
            raise ErrorFoodShare("Agrega al menos un alimento a la donación.")
        for a in alimentos:
            if a.fecha_vencimiento < self.hoy:
                raise ErrorFoodShare("«{}» ya está caducado ({}).".format(a.nombre, a.str_vencimiento))
        donacion = Donacion(self.siguiente_id(), alimentos, restaurante, self.hoy)
        self.donaciones.append(donacion)
        return donacion

    def aprobar_donacion(self, administrador, id_donacion):
        self._exigir_admin(administrador)
        donacion = self._exigir_donacion(id_donacion)
        if donacion.estado == Estado.PENDIENTE and donacion.esta_vencida(self.hoy):
            donacion.cambiar_estado(Estado.VENCIDA)
            raise ErrorFoodShare("La donación {} ya caducó; se marcó como vencida.".format(id_donacion))
        donacion.cambiar_estado(Estado.DISPONIBLE)
        return donacion

    def rechazar_donacion(self, administrador, id_donacion):
        self._exigir_admin(administrador)
        donacion = self._exigir_donacion(id_donacion)
        donacion.cambiar_estado(Estado.RECHAZADA)
        return donacion

    def reservar_donacion(self, fundacion, id_donacion):
        if not isinstance(fundacion, Fundacion):
            raise ErrorFoodShare("Solo una fundación puede reservar donaciones.")
        donacion = self._exigir_donacion(id_donacion)
        if donacion.estado == Estado.DISPONIBLE and donacion.esta_vencida(self.hoy):
            donacion.cambiar_estado(Estado.VENCIDA)
            raise ErrorFoodShare("La donación {} ya caducó y no se puede reservar.".format(id_donacion))

        por_recibir = self.peso_de([d for d in self.reservas_de_fundacion(fundacion)
                                    if d.estado == Estado.RESERVADA])
        if por_recibir + donacion.peso_total > fundacion.capacidad_kg:
            raise ErrorFoodShare(
                "Supera tu capacidad de recepción ({:.1f} kg). Tienes {:.1f} kg por recibir.".format(
                    fundacion.capacidad_kg, por_recibir))

        donacion.cambiar_estado(Estado.RESERVADA)
        donacion.reservado_por = fundacion
        return donacion

    def marcar_recibida(self, fundacion, id_donacion):
        donacion = self._exigir_donacion(id_donacion)
        if donacion.reservado_por is not fundacion:
            raise ErrorFoodShare("Solo la fundación que reservó la donación puede marcarla como recibida.")
        donacion.cambiar_estado(Estado.RECIBIDA)
        donacion.fecha_recepcion = self.hoy
        return donacion

    @staticmethod
    def _exigir_admin(usuario):
        if not isinstance(usuario, Administrador):
            raise ErrorFoodShare("Solo un administrador puede validar donaciones.")

    # --- Resúmenes para los paneles ---------------------------------------
    def resumen_general(self):
        disponibles = self.donaciones_por_estado(Estado.DISPONIBLE)
        return {
            "pendientes": len(self.donaciones_por_estado(Estado.PENDIENTE)),
            "disponibles": len(disponibles),
            "kg_disponibles": self.peso_de(disponibles),
            "reservadas": len(self.donaciones_por_estado(Estado.RESERVADA)),
            "recibidas": len(self.donaciones_por_estado(Estado.RECIBIDA)),
            "restaurantes": len(self.restaurantes()),
            "total": len(self.donaciones),
        }

    def resumen_restaurante(self, restaurante):
        propias = self.donaciones_de_restaurante(restaurante)
        disponibles = [d for d in propias if d.estado == Estado.DISPONIBLE]
        reservadas = [d for d in propias if d.estado == Estado.RESERVADA]
        return {
            "publicadas": len(propias),
            "pendientes": len([d for d in propias if d.estado == Estado.PENDIENTE]),
            "disponibles": len(disponibles),
            "kg_disponibles": self.peso_de(disponibles),
            "reservadas": len(reservadas),
            "kg_reservadas": self.peso_de(reservadas),
        }

    def resumen_fundacion(self, fundacion):
        activas = [d for d in self.reservas_de_fundacion(fundacion) if d.estado == Estado.RESERVADA]
        return {"activas": len(activas), "kg_por_recibir": self.peso_de(activas)}


# Instancia única que usa la aplicación web.
sistema = Sistema(fecha_actual=FECHA_DEMO)
