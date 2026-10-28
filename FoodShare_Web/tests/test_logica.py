# tests/test_logica.py
"""Pruebas del modelo POO (logica.py). Ejecutar desde FoodShare_Web:

    python -m unittest discover -s tests -v
"""

import os
import sys
import unittest
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logica import (Administrador, Alimento, Donacion, ErrorFoodShare, Estado,  # noqa: E402
                    Fundacion, Restaurante, Sistema, Usuario)

HOY = date(2026, 10, 22)


def nuevo_sistema():
    """Cada prueba usa un sistema nuevo para no afectar a las demás."""
    return Sistema(fecha_actual=HOY)


class PruebasUsuarios(unittest.TestCase):
    def test_usuario_es_abstracto(self):
        with self.assertRaises(TypeError):
            Usuario("U99", "X", "x@x.mx", "123456", "CDMX")

    def test_polimorfismo_de_roles(self):
        s = nuevo_sistema()
        r, f, a = s.obtener_usuario("U01"), s.obtener_usuario("U02"), s.obtener_usuario("U03")
        self.assertIsInstance(r, Restaurante)
        self.assertIsInstance(f, Fundacion)
        self.assertIsInstance(a, Administrador)
        self.assertEqual([u.rol for u in (r, f, a)], ["restaurante", "fundacion", "admin"])
        self.assertEqual(f.pantalla_inicio(), "fundacion_explorar")

    def test_autenticar(self):
        s = nuevo_sistema()
        self.assertIsNotNone(s.autenticar("contacto@elbuensabor.mx", "claveRestaurante2024"))
        self.assertIsNotNone(s.autenticar("  CONTACTO@ElBuenSabor.mx ", "claveRestaurante2024"))
        self.assertIsNone(s.autenticar("contacto@elbuensabor.mx", "incorrecta"))
        self.assertIsNone(s.autenticar("nadie@x.mx", "claveRestaurante2024"))

    def test_registrar_fundacion(self):
        s = nuevo_sistema()
        u = s.registrar_usuario("fundacion", "Comedor Vida", "vida@comedor.org", "secreto1",
                                "secreto1", "Iztapalapa", capacidad_kg="120")
        self.assertIsInstance(u, Fundacion)
        self.assertEqual(u.capacidad_kg, 120.0)
        self.assertIs(s.autenticar("vida@comedor.org", "secreto1"), u)

    def test_registro_valida_datos(self):
        s = nuevo_sistema()
        casos = [
            ("restaurante", "contacto@elbuensabor.mx", "secreto1", "secreto1", "Razón"),  # correo repetido
            ("restaurante", "nuevo@r.mx", "secreto1", "otra-cosa", "Razón"),             # no coinciden
            ("restaurante", "nuevo@r.mx", "123", "123", "Razón"),                        # muy corta
            ("restaurante", "nuevo@r.mx", "secreto1", "secreto1", ""),                   # sin razón social
            ("admin", "nuevo@r.mx", "secreto1", "secreto1", "Razón"),                    # tipo no permitido
        ]
        for tipo, correo, c1, c2, razon in casos:
            with self.subTest(tipo=tipo, correo=correo):
                with self.assertRaises(ErrorFoodShare):
                    s.registrar_usuario(tipo, "Nuevo", correo, c1, c2, "CDMX", razon_social=razon)


class PruebasDonacion(unittest.TestCase):
    def test_alimento_valida_datos(self):
        with self.assertRaises(ErrorFoodShare):
            Alimento("", 5, "25/10/2026")
        with self.assertRaises(ErrorFoodShare):
            Alimento("Pan", 0, "25/10/2026")
        with self.assertRaises(ErrorFoodShare):
            Alimento("Pan", "abc", "25/10/2026")
        with self.assertRaises(ErrorFoodShare):
            Alimento("Pan", 5, "2026-10-25")

    def test_calculos_de_donacion(self):
        s = nuevo_sistema()
        d = Donacion("DON900", [Alimento("Sopa", 12, "26/10/2026"),
                                Alimento("Ensalada", 8.5, "24/10/2026")],
                     s.obtener_usuario("U01"), HOY)
        self.assertEqual(d.peso_total, 20.5)
        self.assertEqual(d.str_vencimiento, "24/10/2026")
        self.assertEqual(d.descripcion, "Sopa y Ensalada")
        self.assertEqual(d.estado, Estado.PENDIENTE)

    def test_transicion_invalida(self):
        s = nuevo_sistema()
        recibida = s.obtener_donacion("DON022")
        with self.assertRaises(ErrorFoodShare):
            recibida.cambiar_estado(Estado.DISPONIBLE)


class PruebasFlujoCompleto(unittest.TestCase):
    def setUp(self):
        self.s = nuevo_sistema()
        self.restaurante = self.s.obtener_usuario("U01")
        self.fundacion = self.s.obtener_usuario("U02")
        self.admin = self.s.obtener_usuario("U03")

    def test_datos_demo(self):
        r = self.s.resumen_general()
        self.assertEqual((r["pendientes"], r["disponibles"], r["reservadas"], r["recibidas"]), (1, 3, 2, 1))
        self.assertEqual(r["kg_disponibles"], 64.0)
        self.assertEqual(self.s.resumen_fundacion(self.fundacion), {"activas": 2, "kg_por_recibir": 43.5})

    def test_publicar_validar_reservar_recibir(self):
        d = self.s.publicar_donacion(self.restaurante, [Alimento("Ensalada de frutas", 8.5, "24/10/2026"),
                                                         Alimento("Sopa de verduras", 12, "26/10/2026")])
        self.assertEqual(d.id_donacion, "DON029")
        self.assertEqual(d.estado, Estado.PENDIENTE)

        self.s.aprobar_donacion(self.admin, "DON029")
        self.assertEqual(d.estado, Estado.DISPONIBLE)

        self.s.reservar_donacion(self.fundacion, "DON029")
        self.assertEqual(d.estado, Estado.RESERVADA)
        self.assertIs(d.reservado_por, self.fundacion)

        self.s.marcar_recibida(self.fundacion, "DON029")
        self.assertEqual(d.estado, Estado.RECIBIDA)
        self.assertEqual(d.fecha_recepcion, HOY)
        self.assertEqual(self.s.siguiente_id(), "DON030")

    def test_rechazar(self):
        self.s.rechazar_donacion(self.admin, "DON025")
        self.assertEqual(self.s.obtener_donacion("DON025").estado, Estado.RECHAZADA)
        with self.assertRaises(ErrorFoodShare):
            self.s.aprobar_donacion(self.admin, "DON025")

    def test_permisos_por_rol(self):
        with self.assertRaises(ErrorFoodShare):
            self.s.aprobar_donacion(self.restaurante, "DON025")
        with self.assertRaises(ErrorFoodShare):
            self.s.reservar_donacion(self.admin, "DON027")
        with self.assertRaises(ErrorFoodShare):
            self.s.publicar_donacion(self.fundacion, [Alimento("Pan", 1, "30/10/2026")])

    def test_no_se_reserva_lo_no_disponible(self):
        for id_donacion in ("DON025", "DON028", "DON022", "DON021"):
            with self.subTest(id_donacion=id_donacion):
                with self.assertRaises(ErrorFoodShare):
                    self.s.reservar_donacion(self.fundacion, id_donacion)

    def test_solo_quien_reservo_marca_recibida(self):
        otra = self.s.registrar_usuario("fundacion", "Otra", "otra@f.org", "secreto1", "secreto1",
                                        "CDMX", capacidad_kg=100)
        with self.assertRaises(ErrorFoodShare):
            self.s.marcar_recibida(otra, "DON028")

    def test_capacidad_de_la_fundacion(self):
        chica = self.s.registrar_usuario("fundacion", "Chica", "chica@f.org", "secreto1", "secreto1",
                                         "CDMX", capacidad_kg=25)
        self.s.reservar_donacion(chica, "DON027")          # 20 kg: cabe
        with self.assertRaises(ErrorFoodShare):
            self.s.reservar_donacion(chica, "DON026")      # 20 + 12 > 25

    def test_no_se_publica_comida_caducada(self):
        with self.assertRaises(ErrorFoodShare):
            self.s.publicar_donacion(self.restaurante, [Alimento("Pan", 2, "21/10/2026")])
        with self.assertRaises(ErrorFoodShare):
            self.s.publicar_donacion(self.restaurante, [])

    def test_vencimiento_automatico(self):
        s = Sistema(fecha_actual=date(2026, 10, 25))
        # DON024 (vence 23/10) y DON026 (24/10) estaban disponibles; DON025 vence 27/10.
        self.assertEqual(s.obtener_donacion("DON024").estado, Estado.VENCIDA)
        self.assertEqual(s.obtener_donacion("DON026").estado, Estado.VENCIDA)
        self.assertEqual(s.obtener_donacion("DON025").estado, Estado.PENDIENTE)
        # Lo reservado no vence automáticamente: ya tiene quién lo recoja.
        self.assertEqual(s.obtener_donacion("DON028").estado, Estado.RESERVADA)

    def test_filtrar(self):
        todas = self.s.todas_las_donaciones()
        self.assertEqual([d.id_donacion for d in self.s.filtrar(todas, "pan")], ["DON026", "DON022"])
        self.assertEqual(len(self.s.filtrar(todas, "", Estado.DISPONIBLE)), 3)
        self.assertEqual(len(self.s.filtrar(todas, "buen sabor", Estado.RESERVADA)), 1)


if __name__ == "__main__":
    unittest.main()
