# FoodShare Network — versión web 2.0

Plataforma que conecta restaurantes con fundaciones para aprovechar excedentes de comida
(ODS 2 · Hambre Cero). Versión web hecha con **Python + Flask**, con la interfaz diseñada
en Google Stitch. Los datos viven en memoria; la versión 3.0 los guardará en SQLite.

## Cómo ejecutarla (Windows)

```
cd FoodShare_Web
python -m pip install -r requirements.txt
python app.py
```

Abre **http://127.0.0.1:5000** en el navegador. Se necesita internet, porque los estilos
(Tailwind) y los íconos se cargan desde la red.

### Cuentas de demostración

También se llenan solas con los botones «Cuentas demo» del inicio de sesión.

| Rol | Correo | Contraseña |
|---|---|---|
| Restaurante | contacto@elbuensabor.mx | claveRestaurante2024 |
| Fundación | recepcion@bancoesperanza.org | claveFundacion2024 |
| Administradora | admin@foodshare.org | rootAdminODS123 |

Para la demo, el sistema toma como «hoy» el **22/10/2026** (`FECHA_DEMO` en `datos_demo.py`).
Así los datos de ejemplo siempre se ven igual. Con `FECHA_DEMO = None` usa la fecha real.

## Flujo de una donación

```
Restaurante publica ──► Pendiente de validación
                           │
          Administradora aprueba ──► Disponible ──► Fundación reserva ──► Reservada ──► Fundación marca ──► Recibida
          Administradora rechaza ──► Rechazada
          Caduca sin reservarse   ──► Vencida (automático)
```

## Cómo está organizado

| Archivo | Qué hace |
|---|---|
| `logica.py` | **Modelo POO y reglas del negocio.** No sabe nada de páginas web. |
| `app.py` | **Parte web (Flask).** Recibe cada petición, llama a `sistema` y elige la plantilla. |
| `datos_demo.py` | Usuarios y donaciones de ejemplo (diccionarios). |
| `templates/` | Pantallas HTML (Jinja2 + Tailwind) basadas en los diseños de Stitch. |
| `tests/` | Pruebas automáticas del modelo y de las rutas. |

### Conceptos de POO en `logica.py`

- **Abstracción:** `Usuario` es una clase abstracta (`ABC`); no se puede crear un «usuario genérico».
- **Herencia:** `Restaurante`, `Fundacion` y `Administrador` heredan de `Usuario`.
- **Polimorfismo:** cada subclase implementa a su manera `rol`, `etiqueta_rol` y `pantalla_inicio()`.
  Por eso `app.py` manda a cada quien a su pantalla con `usuario.pantalla_inicio()`, sin `if` por rol.
- **Encapsulamiento:** la contraseña se guarda en `_contrasena` y solo se compara con `verificar_contrasena()`.
- **Composición:** una `Donacion` está formada por varios `Alimento`; su peso total y su fecha
  de vencimiento se calculan a partir de ellos (`@property`).
- **Máquina de estados:** `Estado.TRANSICIONES` define a qué estado se puede pasar desde cada uno;
  `Donacion.cambiar_estado()` impide saltos inválidos (por ejemplo, de Recibida a Disponible).
- **Excepciones propias:** las reglas lanzan `ErrorFoodShare`; `app.py` la atrapa y muestra el mensaje.

### Reglas que aplica el sistema

- Solo un restaurante publica, solo la administradora valida y solo una fundación reserva.
- No se puede publicar comida ya caducada ni una donación sin alimentos.
- Una fundación no puede reservar más kilos de su capacidad de recepción.
- Solo la fundación que reservó puede marcar la donación como recibida.
- Lo que caduca estando Pendiente o Disponible pasa solo a Vencida.

### Rutas principales

| Rol | Pantallas |
|---|---|
| Todos | `/login`, `/crear-cuenta`, `/donacion/<id>` (detalle) |
| Restaurante | `/restaurante/panel`, `/restaurante/publicar`, `/restaurante/mis-donaciones` |
| Fundación | `/fundacion/explorar`, `/fundacion/mis-reservas` |
| Administradora | `/admin/panel`, `/admin/validar`, `/admin/todas` |

Las búsquedas usan la URL (`?q=pan&estado=Disponible`), así que un filtro se puede compartir o recargar.

## Pruebas

```
cd FoodShare_Web
python -m unittest discover -s tests -v
```

Son 26 pruebas: roles, registro, validaciones, permisos, capacidad, vencimiento y el flujo
completo publicar → validar → reservar → recibir, por código y por la interfaz.

## Pendiente para la versión 3.0

- Guardar usuarios y donaciones en **SQLite** (`sqlite3`) en lugar de memoria. Al reiniciar
  `app.py` hoy se pierden las donaciones nuevas.
- Guardar contraseñas con hash (`werkzeug.security`).
- Pantalla de Alertas (hoy muestra «en construcción»).
