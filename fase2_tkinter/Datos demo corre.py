# datos_demo.py
import datetime

# --- FUNCIONES AUXILIARES ---
def formatear_fecha(fecha):
    """
    Recibe un objeto datetime.date (o un string en formato AAAA-MM-DD) 
    y devuelve una cadena en formato dd/mm/aaaa para la interfaz.
    Retorna una cadena vacía si el valor es nulo o inválido.
    """
    if not fecha:
        return ""
    if isinstance(fecha, str):
        try:
            fecha = datetime.datetime.strptime(fecha, "%Y-%m-%d").date()
        except ValueError:
            return fecha  # Si ya viene en otro formato de texto, lo regresa tal cual
    return fecha.strftime("%d/%m/%Y")


# Fechas calculadas dinámicamente basadas en el día de hoy
hoy = datetime.date.today()

# --- USUARIOS DEL SISTEMA ---
# NOTA DE SEGURIDAD: Las contraseñas en texto plano son solo para demostración académica.
USUARIOS = {
    "contacto@elbuensabor.mx": {
        "clave": "claveRestaurante2024",
        "rol": "restaurante",
        "nombre_entidad": "El Buen Sabor",
        "responsable": "Juan Pérez"
    },
    "recepcion@bancoesperanza.org": {
        "clave": "claveFundacion2024",
        "rol": "fundacion",
        "nombre_entidad": "Banco Esperanza",
        "responsable": "María Gómez"
    },
    "admin@foodshare.org": {
        "clave": "rootAdminODS123",
        "rol": "admin",
        "nombre_entidad": "Administración Central",
        "responsable": "Lic. Ana Ruiz"
    }
}

# --- CATÁLOGO DE DONACIONES ---
# Nota: Se estandarizó el campo "restaurante" para que coincida 
# con los nombres de entidad definidos en el diccionario de usuarios.
DONACIONES = [
    {
        "id_donacion": "DON028",
        "descripcion": "Frutas de temporada (manzana, plátano)",
        "peso_kg": 25.0,
        "fecha_vencimiento": hoy + datetime.timedelta(days=3),
        "estado": "Reservada",
        "restaurante": "El Buen Sabor",
        "reservado_por": "Banco Esperanza"
    },
    {
        "id_donacion": "DON027",
        "descripcion": "Guisado de lentejas con verduras",
        "peso_kg": 20.0,
        "fecha_vencimiento": hoy + datetime.timedelta(days=4),
        "estado": "Disponible",
        "restaurante": "El Buen Sabor",
        "reservado_por": None
    },
    {
        "id_donacion": "DON026",
        "descripcion": "Pan integral horneado",
        "peso_kg": 12.0,
        "fecha_vencimiento": hoy + datetime.timedelta(days=2),
        "estado": "Disponible",
        "restaurante": "El Buen Sabor",
        "reservado_por": None
    },
    {
        "id_donacion": "DON025",
        "descripcion": "Arroz con verduras cocido",
        "peso_kg": 15.0,
        "fecha_vencimiento": hoy + datetime.timedelta(days=5),
        "estado": "Disponible",
        "restaurante": "El Buen Sabor",
        "reservado_por": None
    },
    {
        "id_donacion": "DON024",
        "descripcion": "Verduras variadas (calabaza, zanahoria)",
        "peso_kg": 32.0,
        "fecha_vencimiento": hoy + datetime.timedelta(days=1),
        "estado": "Disponible",
        "restaurante": "El Buen Sabor",
        "reservado_por": None
    },
    {
        "id_donacion": "DON023",
        "descripcion": "Arroz cocido al vapor",
        "peso_kg": 18.5,
        "fecha_vencimiento": hoy + datetime.timedelta(days=2),
        "estado": "Reservada",
        "restaurante": "El Buen Sabor",
        "reservado_por": "Banco Esperanza"
    },
    {
        "id_donacion": "DON022",
        "descripcion": "Pan de caja integral",
        "peso_kg": 15.0,
        "fecha_vencimiento": hoy - datetime.timedelta(days=2),
        "estado": "Entregada",
        "restaurante": "El Buen Sabor",
        "reservado_por": "Banco Esperanza"
    },
    {
        "id_donacion": "DON021",
        "descripcion": "Pollo guisado en salsa",
        "peso_kg": 20.0,
        "fecha_vencimiento": hoy - datetime.timedelta(days=5),
        "estado": "Vencida",
        "restaurante": "El Buen Sabor",
        "reservado_por": None
    }
]
