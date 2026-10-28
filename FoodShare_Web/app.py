# app.py
"""Aplicación web de FoodShare Network (Flask).

app.py solo se encarga de la parte web: recibe la petición del navegador,
le pide a `sistema` (logica.py) que haga el trabajo y elige qué plantilla
HTML mostrar. Las reglas del negocio viven en logica.py.

Para ejecutar:  python app.py   y abrir http://127.0.0.1:5000
"""

import os
from datetime import timedelta
from functools import wraps

from flask import (Flask, abort, flash, g, redirect, render_template, request,
                   session, url_for)

from logica import Alimento, ErrorFoodShare, Estado, sistema

app = Flask(__name__)
app.secret_key = os.environ.get("FOODSHARE_SECRET", "secreto_foodshare_ods2")
app.permanent_session_lifetime = timedelta(days=7)

# Cuentas que llenan los botones "Cuentas demo" del inicio de sesión.
CUENTAS_DEMO = {
    "restaurante": ("contacto@elbuensabor.mx", "claveRestaurante2024"),
    "fundacion": ("recepcion@bancoesperanza.org", "claveFundacion2024"),
    "admin": ("admin@foodshare.org", "rootAdminODS123"),
}


# ---------------------------------------------------------------------------
# Sesión y permisos
# ---------------------------------------------------------------------------
@app.before_request
def cargar_usuario():
    """Antes de cada petición, recupera el usuario que inició sesión."""
    g.usuario = sistema.obtener_usuario(session.get("usuario_id"))
    sistema.actualizar_vencidas()


@app.context_processor
def variables_globales():
    """Variables disponibles en todas las plantillas."""
    return {"usuario": g.get("usuario"), "Estado": Estado}


def login_requerido(vista):
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if g.usuario is None:
            flash("Inicia sesión para continuar.", "error")
            return redirect(url_for("login"))
        return vista(*args, **kwargs)
    return envoltura


def rol_requerido(rol):
    def decorador(vista):
        @wraps(vista)
        @login_requerido
        def envoltura(*args, **kwargs):
            if g.usuario.rol != rol:
                flash("Esa sección no corresponde a tu tipo de cuenta.", "error")
                return redirect(url_for(g.usuario.pantalla_inicio()))
            return vista(*args, **kwargs)
        return envoltura
    return decorador


def ejecutar(accion, mensaje_exito):
    """Ejecuta una acción del sistema y convierte el resultado en un mensaje."""
    try:
        donacion = accion()
        flash(mensaje_exito.format(id=donacion.id_donacion, desc=donacion.descripcion), "exito")
    except ErrorFoodShare as error:
        flash(str(error), "error")


def filtros_de_busqueda(estado_por_defecto=""):
    """Lee ?q=...&estado=... de la URL."""
    texto = request.args.get("q", "").strip()
    estado = request.args.get("estado", estado_por_defecto)
    if estado not in Estado.TODOS:
        estado = ""
    return texto, estado


# ---------------------------------------------------------------------------
# Acceso
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    return redirect(url_for("inicio_por_rol" if g.usuario else "login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if g.usuario:
        return redirect(url_for("inicio_por_rol"))

    correo = ""
    error = None
    if request.method == "POST":
        correo = request.form.get("email", "").strip()
        usuario = sistema.autenticar(correo, request.form.get("password", ""))
        if usuario:
            session.clear()
            session["usuario_id"] = usuario.id_usuario
            session.permanent = bool(request.form.get("remember"))
            return redirect(url_for(usuario.pantalla_inicio()))
        error = "Correo o contraseña incorrectos."

    return render_template("login.html", correo=correo, error=error,
                           resumen=sistema.resumen_general(), cuentas_demo=CUENTAS_DEMO)


@app.route("/crear-cuenta", methods=["GET", "POST"])
def crear_cuenta():
    if g.usuario:
        return redirect(url_for("inicio_por_rol"))

    datos = request.form if request.method == "POST" else {}
    error = None
    if request.method == "POST":
        try:
            sistema.registrar_usuario(
                tipo=datos.get("account_type"),
                nombre=datos.get("org_name"),
                correo=datos.get("email"),
                contrasena=datos.get("password", ""),
                confirmacion=datos.get("password_confirm", ""),
                ubicacion=datos.get("location"),
                razon_social=datos.get("business_name"),
                capacidad_kg=datos.get("capacity_kg"),
            )
            flash("Cuenta creada. Ya puedes iniciar sesión.", "exito")
            return redirect(url_for("login"))
        except ErrorFoodShare as e:
            error = str(e)

    return render_template("crear_cuenta.html", datos=datos, error=error,
                           tipo=datos.get("account_type", "restaurante"),
                           resumen=sistema.resumen_general())


@app.route("/recuperar")
def recuperar_contrasena():
    flash("La recuperación de contraseña estará disponible en una próxima versión. "
          "Por ahora, contacta a la administración.", "info")
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada.", "info")
    return redirect(url_for("login"))


@app.route("/inicio")
@login_requerido
def inicio_por_rol():
    return redirect(url_for(g.usuario.pantalla_inicio()))


# ---------------------------------------------------------------------------
# Restaurante
# ---------------------------------------------------------------------------
@app.route("/restaurante/panel")
@rol_requerido("restaurante")
def restaurante_panel():
    propias = sistema.donaciones_de_restaurante(g.usuario)
    return render_template("restaurante_panel.html",
                           resumen=sistema.resumen_restaurante(g.usuario),
                           donaciones=propias[:8])


@app.route("/restaurante/publicar", methods=["GET", "POST"])
@rol_requerido("restaurante")
def restaurante_publicar():
    # La lista de alimentos que se va armando vive en la sesión del navegador
    # hasta que se pulsa "Publicar donación".
    borrador = session.get("borrador", [])
    campos = {}

    if request.method == "POST":
        accion = request.form.get("accion", "")

        if accion == "agregar":
            campos = request.form
            try:
                alimento = Alimento(campos.get("food_name"), campos.get("food_weight"),
                                    campos.get("food_expiry"), campos.get("food_nutrients"))
                if alimento.fecha_vencimiento < sistema.hoy:
                    raise ErrorFoodShare("La fecha de caducidad no puede ser anterior a hoy.")
                borrador.append({"nombre": alimento.nombre, "peso": alimento.peso_kg,
                                 "caducidad": alimento.str_vencimiento,
                                 "nutrientes": alimento.nutrientes})
                session["borrador"] = borrador
                campos = {}
            except ErrorFoodShare as e:
                flash(str(e), "error")

        elif accion.startswith("quitar-"):
            indice = accion.split("-", 1)[1]
            if indice.isdigit() and int(indice) < len(borrador):
                borrador.pop(int(indice))
                session["borrador"] = borrador

        elif accion == "cancelar":
            session.pop("borrador", None)
            return redirect(url_for("restaurante_panel"))

        elif accion == "publicar":
            if not request.form.get("declaracion"):
                flash("Debes aceptar la declaración de higiene y temperatura adecuada.", "error")
            else:
                try:
                    alimentos = [Alimento(a["nombre"], a["peso"], a["caducidad"], a["nutrientes"])
                                 for a in borrador]
                    donacion = sistema.publicar_donacion(g.usuario, alimentos)
                    session.pop("borrador", None)
                    flash("Donación {} enviada. Queda pendiente de validación.".format(
                        donacion.id_donacion), "exito")
                    return redirect(url_for("restaurante_mis_donaciones"))
                except ErrorFoodShare as e:
                    flash(str(e), "error")

        if accion != "agregar" or not campos:
            return redirect(url_for("restaurante_publicar"))

    total_kg = round(sum(a["peso"] for a in borrador), 2)
    return render_template("restaurante_publicar.html", borrador=borrador, total_kg=total_kg,
                           siguiente_id=sistema.siguiente_id(), campos=campos)


@app.route("/restaurante/mis-donaciones")
@rol_requerido("restaurante")
def restaurante_mis_donaciones():
    texto, estado = filtros_de_busqueda()
    propias = sistema.donaciones_de_restaurante(g.usuario)
    return render_template("restaurante_mis_donaciones.html",
                           donaciones=sistema.filtrar(propias, texto, estado),
                           resumen=sistema.resumen_restaurante(g.usuario),
                           texto=texto, estado=estado)


# ---------------------------------------------------------------------------
# Fundación
# ---------------------------------------------------------------------------
@app.route("/fundacion/explorar")
@rol_requerido("fundacion")
def fundacion_explorar():
    texto, estado = filtros_de_busqueda(Estado.DISPONIBLE)
    visibles = sistema.donaciones_por_estado(Estado.DISPONIBLE, Estado.RESERVADA,
                                             Estado.RECIBIDA, Estado.VENCIDA)
    return render_template("fundacion_explorar.html",
                           donaciones=sistema.filtrar(visibles, texto, estado),
                           resumen=sistema.resumen_general(), texto=texto, estado=estado)


@app.route("/fundacion/reservar/<id_donacion>", methods=["POST"])
@rol_requerido("fundacion")
def fundacion_reservar(id_donacion):
    ejecutar(lambda: sistema.reservar_donacion(g.usuario, id_donacion),
             "Reservaste «{desc}» ({id}). La verás en Mis reservas.")
    return redirect(request.referrer or url_for("fundacion_explorar"))


@app.route("/fundacion/mis-reservas")
@rol_requerido("fundacion")
def fundacion_mis_reservas():
    texto, estado = filtros_de_busqueda()
    if estado not in ("", Estado.RESERVADA, Estado.RECIBIDA):
        estado = ""
    reservas = sistema.reservas_de_fundacion(g.usuario)
    return render_template("fundacion_mis_reservas.html",
                           donaciones=sistema.filtrar(reservas, texto, estado),
                           total=len(reservas),
                           resumen=sistema.resumen_fundacion(g.usuario),
                           texto=texto, estado=estado)


@app.route("/fundacion/recibir/<id_donacion>", methods=["POST"])
@rol_requerido("fundacion")
def fundacion_recibir(id_donacion):
    ejecutar(lambda: sistema.marcar_recibida(g.usuario, id_donacion),
             "Registraste la recepción de «{desc}» ({id}).")
    return redirect(request.referrer or url_for("fundacion_mis_reservas"))


# ---------------------------------------------------------------------------
# Administrador
# ---------------------------------------------------------------------------
@app.route("/admin/panel")
@rol_requerido("admin")
def admin_panel():
    return render_template("admin_panel.html", resumen=sistema.resumen_general())


@app.route("/admin/validar")
@rol_requerido("admin")
def admin_validar():
    return render_template("admin_validar.html",
                           donaciones=sistema.donaciones_por_estado(Estado.PENDIENTE))


@app.route("/admin/aprobar/<id_donacion>", methods=["POST"])
@rol_requerido("admin")
def admin_aprobar(id_donacion):
    ejecutar(lambda: sistema.aprobar_donacion(g.usuario, id_donacion),
             "Aprobaste {id}. Ya está disponible para las fundaciones.")
    return redirect(url_for("admin_validar"))


@app.route("/admin/rechazar/<id_donacion>", methods=["POST"])
@rol_requerido("admin")
def admin_rechazar(id_donacion):
    ejecutar(lambda: sistema.rechazar_donacion(g.usuario, id_donacion),
             "Rechazaste {id}.")
    return redirect(url_for("admin_validar"))


@app.route("/admin/todas")
@rol_requerido("admin")
def admin_todas():
    texto, estado = filtros_de_busqueda()
    return render_template("admin_todas.html",
                           donaciones=sistema.filtrar(sistema.todas_las_donaciones(), texto, estado),
                           total=len(sistema.donaciones), texto=texto, estado=estado)


# ---------------------------------------------------------------------------
# Compartidas
# ---------------------------------------------------------------------------
@app.route("/donacion/<id_donacion>")
@login_requerido
def donacion_detalle(id_donacion):
    donacion = sistema.obtener_donacion(id_donacion)
    if donacion is None:
        abort(404)
    u = g.usuario
    puede_ver = (u.rol == "admin"
                 or donacion.donante is u
                 or (u.rol == "fundacion" and (donacion.reservado_por is u
                                                or donacion.estado == Estado.DISPONIBLE)))
    if not puede_ver:
        flash("No tienes acceso a esa donación.", "error")
        return redirect(url_for(u.pantalla_inicio()))
    return render_template("donacion_detalle.html", d=donacion)


@app.route("/en-construccion")
@login_requerido
def en_construccion():
    return render_template("en_construccion.html")


@app.errorhandler(404)
def no_encontrado(_error):
    return render_template("en_construccion.html", titulo="Página no encontrada",
                           mensaje="La dirección que abriste no existe."), 404


if __name__ == "__main__":
    app.run(debug=True)
