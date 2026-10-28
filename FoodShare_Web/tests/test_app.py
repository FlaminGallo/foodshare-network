# tests/test_app.py
"""Pruebas de las pantallas y rutas de Flask (app.py). Ejecutar desde FoodShare_Web:

    python -m unittest discover -s tests -v
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as aplicacion  # noqa: E402
import logica  # noqa: E402
from datos_demo import FECHA_DEMO  # noqa: E402


class PruebasWeb(unittest.TestCase):
    def setUp(self):
        # Sistema limpio en cada prueba, para que una no afecte a otra.
        aplicacion.sistema = logica.Sistema(fecha_actual=FECHA_DEMO)
        aplicacion.app.config["TESTING"] = True
        self.cliente = aplicacion.app.test_client()

    def entrar(self, rol):
        correo, clave = aplicacion.CUENTAS_DEMO[rol]
        return self.cliente.post("/login", data={"email": correo, "password": clave})

    def texto(self, url):
        return self.cliente.get(url).get_data(as_text=True)

    # --- Acceso ---------------------------------------------------------
    def test_login_redirige_segun_rol(self):
        destinos = {"restaurante": "/restaurante/panel", "fundacion": "/fundacion/explorar",
                    "admin": "/admin/panel"}
        for rol, destino in destinos.items():
            with self.subTest(rol=rol):
                respuesta = self.entrar(rol)
                self.assertEqual(respuesta.status_code, 302)
                self.assertTrue(respuesta.headers["Location"].endswith(destino))
                self.cliente.get("/logout")

    def test_login_incorrecto(self):
        respuesta = self.cliente.post("/login", data={"email": "admin@foodshare.org", "password": "x"})
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("Correo o contraseña incorrectos", respuesta.get_data(as_text=True))

    def test_pantallas_protegidas(self):
        respuesta = self.cliente.get("/admin/panel")
        self.assertTrue(respuesta.headers["Location"].endswith("/login"))
        self.entrar("fundacion")
        respuesta = self.cliente.get("/admin/validar")
        self.assertTrue(respuesta.headers["Location"].endswith("/fundacion/explorar"))

    def test_crear_cuenta(self):
        datos = {"account_type": "restaurante", "org_name": "Tacos Don Luis", "business_name": "Tacos SA",
                 "location": "CDMX", "email": "tacos@donluis.mx", "password": "secreto1",
                 "password_confirm": "secreto1"}
        respuesta = self.cliente.post("/crear-cuenta", data=datos)
        self.assertTrue(respuesta.headers["Location"].endswith("/login"))
        respuesta = self.cliente.post("/login", data={"email": "tacos@donluis.mx", "password": "secreto1"})
        self.assertTrue(respuesta.headers["Location"].endswith("/restaurante/panel"))

    # --- Flujo completo por la interfaz ---------------------------------
    def test_flujo_completo(self):
        self.entrar("restaurante")
        self.cliente.post("/restaurante/publicar", data={
            "accion": "agregar", "food_name": "Sopa de verduras", "food_weight": "12",
            "food_expiry": "26/10/2026", "food_nutrients": "Fibra"})
        self.cliente.post("/restaurante/publicar", data={
            "accion": "agregar", "food_name": "Ensalada de frutas", "food_weight": "8.5",
            "food_expiry": "24/10/2026"})
        self.assertIn("Total: 20.5 kg", self.texto("/restaurante/publicar"))
        self.cliente.post("/restaurante/publicar", data={"accion": "publicar", "declaracion": "1"})
        self.assertIn("DON029", self.texto("/restaurante/mis-donaciones"))
        self.cliente.get("/logout")

        self.entrar("admin")
        self.assertIn("DON029", self.texto("/admin/validar"))
        self.cliente.post("/admin/aprobar/DON029")
        self.cliente.get("/logout")

        self.entrar("fundacion")
        self.assertIn("DON029", self.texto("/fundacion/explorar"))
        self.cliente.post("/fundacion/reservar/DON029")
        self.cliente.post("/fundacion/recibir/DON029")
        self.assertEqual(aplicacion.sistema.obtener_donacion("DON029").estado, logica.Estado.RECIBIDA)

    def test_publicar_exige_declaracion(self):
        self.entrar("restaurante")
        self.cliente.post("/restaurante/publicar", data={
            "accion": "agregar", "food_name": "Pan", "food_weight": "3", "food_expiry": "30/10/2026"})
        self.cliente.post("/restaurante/publicar", data={"accion": "publicar"})
        self.assertIsNone(aplicacion.sistema.obtener_donacion("DON029"))

    def test_quitar_alimento_del_borrador(self):
        self.entrar("restaurante")
        self.cliente.post("/restaurante/publicar", data={
            "accion": "agregar", "food_name": "Pan", "food_weight": "3", "food_expiry": "30/10/2026"})
        self.cliente.post("/restaurante/publicar", data={"accion": "quitar-0"})
        self.assertIn("Total alimentos: 0", self.texto("/restaurante/publicar"))

    def test_filtros_por_url(self):
        self.entrar("admin")
        html = self.texto("/admin/todas?estado=Vencida")
        self.assertIn("DON021", html)
        self.assertNotIn("DON027", html)
        html = self.texto("/admin/todas?q=lentejas")
        self.assertIn("DON027", html)
        self.assertNotIn("DON021", html)


if __name__ == "__main__":
    unittest.main()
