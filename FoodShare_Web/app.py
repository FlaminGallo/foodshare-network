# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from logica import sistema
from functools import wraps

app = Flask(__name__)
app.secret_key = 'secreto_foodshare_ods2'

# --- DECORADORES ---
def login_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorador

def rol_requerido(rol):
    def decorador(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if session.get('rol') != rol:
                return redirect(url_for('inicio_por_rol'))
            return f(*args, **kwargs)
        return wrapper
    return decorador

# --- RUTAS DE SESIÓN ---
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'usuario_id' in session:
        return redirect(url_for('inicio_por_rol'))
    
    if request.method == 'POST':
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')
        rol_esperado = request.form.get('rol')

        usuario = sistema.autenticar(correo, contrasena)
        
        if usuario and usuario.rol == rol_esperado:
            session['usuario_id'] = usuario.id_usuario
            session['rol'] = usuario.rol
            session['nombre'] = usuario.nombre
            return redirect(url_for('inicio_por_rol'))
        else:
            flash('Credenciales incorrectas o rol no coincidente.', 'error')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/inicio')
@login_requerido
def inicio_por_rol():
    rutas = {
        'restaurante': 'restaurante_panel',
        'fundacion': 'fundacion_explorar',
        'admin': 'admin_panel'
    }
    return redirect(url_for(rutas.get(session['rol'], 'login')))

# --- RUTAS RESTAURANTE ---
@app.route('/restaurante/panel')
@login_requerido
@rol_requerido('restaurante')
def restaurante_panel():
    return render_template('restaurante_panel.html')

@app.route('/restaurante/publicar')
@login_requerido
@rol_requerido('restaurante')
def restaurante_publicar():
    return render_template('restaurante_publicar.html')

@app.route('/restaurante/mis-donaciones')
@login_requerido
@rol_requerido('restaurante')
def restaurante_mis_donaciones():
    donaciones = sistema.obtener_donaciones_de_restaurante(session['usuario_id'])
    estado_filtro = request.args.get('estado', '')
    if estado_filtro:
        donaciones = [d for d in donaciones if d.estado.lower() == estado_filtro.lower()]
    return render_template('restaurante_mis_donaciones.html', donaciones=donaciones)

# --- RUTAS FUNDACIÓN ---
@app.route('/fundacion/explorar')
@login_requerido
@rol_requerido('fundacion')
def fundacion_explorar():
    donaciones = sistema.obtener_donaciones_por_estado(["Disponible", "Reservada", "Recibida", "Vencida"])
    estado_filtro = request.args.get('estado', '')
    if estado_filtro:
        donaciones = [d for d in donaciones if d.estado.lower() == estado_filtro.lower()]
    return render_template('fundacion_explorar.html', donaciones=donaciones)

@app.route('/fundacion/mis-reservas')
@login_requerido
@rol_requerido('fundacion')
def fundacion_mis_reservas():
    donaciones = sistema.obtener_reservas_de_fundacion(session['usuario_id'])
    
    # Cálculos globales de reservas (solo estado "Reservada")
    reservadas = [d for d in donaciones if d.estado.lower() == 'reservada']
    total_reservas = len(reservadas)
    peso_total = sum(d.peso_total for d in reservadas)

    # Parámetros de búsqueda y filtrado
    q = request.args.get('q', '').lower()
    estado_filtro = request.args.get('estado', 'Todas')

    if q:
        donaciones = [d for d in donaciones if q in d.descripcion.lower() or (hasattr(d.donante, 'nombre') and q in d.donante.nombre.lower())]
    if estado_filtro and estado_filtro != 'Todas':
        donaciones = [d for d in donaciones if d.estado.lower() == estado_filtro.lower()]

    return render_template('fundacion_mis_reservas.html', 
                           donaciones=donaciones, 
                           total_reservas=total_reservas, 
                           peso_total=peso_total)

# --- RUTAS ADMIN ---
@app.route('/admin/panel')
@login_requerido
@rol_requerido('admin')
def admin_panel():
    return render_template('admin_panel.html')

@app.route('/admin/validar')
@login_requerido
@rol_requerido('admin')
def admin_validar():
    donaciones = sistema.obtener_donaciones_por_estado(["Pendiente de validación"])
    return render_template('admin_validar.html', donaciones=donaciones)

@app.route('/admin/todas')
@login_requerido
@rol_requerido('admin')
def admin_todas():
    donaciones = sistema.donaciones
    estado_filtro = request.args.get('estado', '')
    if estado_filtro:
        donaciones = [d for d in donaciones if d.estado.lower() == estado_filtro.lower()]
    return render_template('admin_todas.html', donaciones=donaciones)

@app.route('/en-construccion')
@login_requerido
def en_construccion():
    return render_template('en_construccion.html')

if __name__ == '__main__':
    app.run(debug=True)