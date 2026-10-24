# datos_demo.py
USUARIOS_DEMO = [
    {
        "id_usuario": "U01", "rol": "restaurante", "nombre": "El Buen Sabor",
        "correo": "contacto@elbuensabor.mx", "contrasena": "claveRestaurante2024",
        "ubicacion": "Centro, CDMX", "razon_social": "Gastronómica El Buen Sabor S.A."
    },
    {
        "id_usuario": "U02", "rol": "fundacion", "nombre": "Banco Esperanza",
        "correo": "recepcion@bancoesperanza.org", "contrasena": "claveFundacion2024",
        "ubicacion": "Sur, CDMX", "capacidad_kg": 500.0
    },
    {
        "id_usuario": "U03", "rol": "admin", "nombre": "Lic. Ana Ruiz",
        "correo": "admin@foodshare.org", "contrasena": "rootAdminODS123",
        "ubicacion": "Sede Central"
    },
    {
        "id_usuario": "U04", "rol": "restaurante", "nombre": "Frutería Central",
        "correo": "contacto@fruteriacentral.mx", "contrasena": "clave2024",
        "ubicacion": "Norte, CDMX", "razon_social": "Frutas del Norte S.A."
    },
    {
        "id_usuario": "U05", "rol": "restaurante", "nombre": "Comedor La Esquina",
        "correo": "contacto@comedorlaesquina.mx", "contrasena": "clave2024",
        "ubicacion": "Oriente, CDMX", "razon_social": "Comedor Popular La Esquina"
    },
    {
        "id_usuario": "U06", "rol": "restaurante", "nombre": "Panadería San José",
        "correo": "contacto@panaderiasanjose.mx", "contrasena": "clave2024",
        "ubicacion": "Poniente, CDMX", "razon_social": "Panificadora San José S.A."
    }
]

DONACIONES_DEMO = [
    {
        "id_donacion": "DON028", "descripcion": "Frutas de temporada", "fecha_creacion": "22/10/2026",
        "estado": "Reservada", "donante_id": "U04", "reservado_por_id": "U02",
        "alimentos": [{"nombre": "Caja de frutas mixtas", "peso_kg": 25.0, "fecha_vencimiento": "25/10/2026"}]
    },
    {
        "id_donacion": "DON027", "descripcion": "Guisado de lentejas con verduras", "fecha_creacion": "22/10/2026",
        "estado": "Disponible", "donante_id": "U05", "reservado_por_id": None,
        "alimentos": [{"nombre": "Lentejas preparadas", "peso_kg": 20.0, "fecha_vencimiento": "26/10/2026"}]
    },
    {
        "id_donacion": "DON026", "descripcion": "Pan integral horneado", "fecha_creacion": "22/10/2026",
        "estado": "Disponible", "donante_id": "U06", "reservado_por_id": None,
        "alimentos": [{"nombre": "Pan integral", "peso_kg": 12.0, "fecha_vencimiento": "24/10/2026"}]
    },
    {
        "id_donacion": "DON025", "descripcion": "Arroz con verduras cocido", "fecha_creacion": "22/10/2026",
        "estado": "Pendiente de validación", "donante_id": "U01", "reservado_por_id": None,
        "alimentos": [{"nombre": "Arroz preparado", "peso_kg": 15.0, "fecha_vencimiento": "27/10/2026"}]
    },
    {
        "id_donacion": "DON024", "descripcion": "Verduras variadas", "fecha_creacion": "22/10/2026",
        "estado": "Disponible", "donante_id": "U01", "reservado_por_id": None,
        "alimentos": [{"nombre": "Caja de verduras", "peso_kg": 32.0, "fecha_vencimiento": "23/10/2026"}]
    },
    {
        "id_donacion": "DON023", "descripcion": "Arroz cocido al vapor", "fecha_creacion": "22/10/2026",
        "estado": "Reservada", "donante_id": "U01", "reservado_por_id": "U02",
        "alimentos": [{"nombre": "Arroz al vapor", "peso_kg": 18.5, "fecha_vencimiento": "25/10/2026"}]
    },
    {
        "id_donacion": "DON022", "descripcion": "Pan de caja integral", "fecha_creacion": "22/10/2026",
        "estado": "Recibida", "donante_id": "U01", "reservado_por_id": "U02",
        "alimentos": [{"nombre": "Pan de caja", "peso_kg": 15.0, "fecha_vencimiento": "20/10/2026"}]
    },
    {
        "id_donacion": "DON021", "descripcion": "Pollo guisado en salsa", "fecha_creacion": "22/10/2026",
        "estado": "Vencida", "donante_id": "U01", "reservado_por_id": None,
        "alimentos": [{"nombre": "Pollo guisado", "peso_kg": 20.0, "fecha_vencimiento": "17/10/2026"}]
    }
]