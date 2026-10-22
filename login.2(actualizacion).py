# vistas/login.py
import tkinter as tk
import tkinter.ttk as ttk
import estilos
import datos_demo


class Login(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, style="Panel.TFrame")
        self.app = app

        self.rol_seleccionado = tk.StringVar(value="restaurante")
        self.mostrar_pwd = False

        self._construir_interfaz()

    def _construir_interfaz(self):
        # Contenedor central para simular el cuadro de login
        marco_central = ttk.Frame(
            self,
            style="Panel.TFrame",
            padding=30
        )
        marco_central.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # Título
        ttk.Label(
            marco_central,
            text="Control de Acceso",
            style="Titulo.TLabel"
        ).pack(anchor="w", pady=(0, 2))

        ttk.Label(
            marco_central,
            text="Plataforma de redistribución | ODS 2 Hambre Cero",
            style="TLabel"
        ).pack(anchor="w", pady=(0, 20))

        # Pestañas de rol
        marco_tabs = tk.Frame(
            marco_central,
            bg=estilos.BG_PANEL
        )
        marco_tabs.pack(fill="x", pady=(0, 15))

        self.btn_restaurante = tk.Button(
            marco_tabs,
            text="Restaurante",
            font=estilos.FUENTE_BASE,
            relief="flat",
            command=lambda: self.seleccionar_rol("restaurante")
        )
        self.btn_restaurante.pack(
            side="left",
            expand=True,
            fill="x",
            padx=2
        )

        self.btn_fundacion = tk.Button(
            marco_tabs,
            text="Fundación",
            font=estilos.FUENTE_BASE,
            relief="flat",
            command=lambda: self.seleccionar_rol("fundacion")
        )
        self.btn_fundacion.pack(
            side="left",
            expand=True,
            fill="x",
            padx=2
        )

        self.btn_admin = tk.Button(
            marco_tabs,
            text="Administrador",
            font=estilos.FUENTE_BASE,
            relief="flat",
            command=lambda: self.seleccionar_rol("admin")
        )
        self.btn_admin.pack(
            side="left",
            expand=True,
            fill="x",
            padx=2
        )

        # Formulario
        ttk.Label(
            marco_central,
            text="Correo electrónico institucional:",
            style="Subtitulo.TLabel"
        ).pack(anchor="w")

        self.var_email = tk.StringVar()

        self.entry_email = ttk.Entry(
            marco_central,
            textvariable=self.var_email,
            font=estilos.FUENTE_BASE,
            width=40
        )
        self.entry_email.pack(
            fill="x",
            pady=(2, 10)
        )

        ttk.Label(
            marco_central,
            text="Contraseña de acceso:",
            style="Subtitulo.TLabel"
        ).pack(anchor="w")

        marco_pwd = ttk.Frame(
            marco_central,
            style="Panel.TFrame"
        )
        marco_pwd.pack(
            fill="x",
            pady=(2, 10)
        )

        self.var_pwd = tk.StringVar()

        self.entry_pwd = ttk.Entry(
            marco_pwd,
            textvariable=self.var_pwd,
            font=estilos.FUENTE_BASE,
            show="*"
        )
        self.entry_pwd.pack(
            side="left",
            expand=True,
            fill="x"
        )

        self.btn_ver = ttk.Button(
            marco_pwd,
            text="👁",
            width=3,
            command=self.alternar_pwd
        )
        self.btn_ver.pack(
            side="right",
            padx=(5, 0)
        )

        # Checkbox recordar sesión
        self.var_recordar = tk.BooleanVar(value=True)

        ttk.Checkbutton(
            marco_central,
            text="Recordar sesión en este equipo",
            variable=self.var_recordar
        ).pack(
            anchor="w",
            pady=(0, 15)
        )

        # Etiqueta de error
        self.lbl_error = tk.Label(
            marco_central,
            text="",
            fg=estilos.ESTADO_VENCIDA,
            bg=estilos.BG_PANEL,
            font=estilos.FUENTE_BASE
        )
        self.lbl_error.pack(
            fill="x",
            pady=(0, 5)
        )

        # Botón ingresar
        btn_ingresar = ttk.Button(
            marco_central,
            text="INGRESAR AL SISTEMA",
            style="Primario.TButton",
            command=self.validar_login
        )
        btn_ingresar.pack(
            fill="x",
            pady=(0, 20)
        )

        # Botones de cuentas demo
        # Las credenciales se consultan desde datos_demo.py
        marco_demo = ttk.Frame(
            marco_central,
            style="Sidebar.TFrame",
            padding=10
        )
        marco_demo.pack(fill="x")

        ttk.Label(
            marco_demo,
            text="Cuentas demo:",
            font=estilos.FUENTE_SUBTITULO,
            background=estilos.BG_SIDEBAR
        ).pack(side="left")

        ttk.Button(
            marco_demo,
            text="Restaurante",
            style="Secundario.TButton",
            command=lambda: self.cargar_demo_por_rol("restaurante")
        ).pack(side="left", padx=5)

        ttk.Button(
            marco_demo,
            text="Fundación",
            style="Secundario.TButton",
            command=lambda: self.cargar_demo_por_rol("fundacion")
        ).pack(side="left", padx=5)

        ttk.Button(
            marco_demo,
            text="Admin",
            style="Secundario.TButton",
            command=lambda: self.cargar_demo_por_rol("admin")
        ).pack(side="left", padx=5)

        # Inicializar interfaz
        self.seleccionar_rol("restaurante")

    def seleccionar_rol(self, rol):
        self.rol_seleccionado.set(rol)

        # Actualizar colores de las pestañas
        botones = [
            (self.btn_restaurante, "restaurante"),
            (self.btn_fundacion, "fundacion"),
            (self.btn_admin, "admin")
        ]

        for btn, nombre_rol in botones:
            if rol == nombre_rol:
                btn.config(
                    bg=estilos.PRIMARIO,
                    fg="white"
                )
            else:
                btn.config(
                    bg=estilos.BORDE,
                    fg=estilos.TEXTO_PRINCIPAL
                )

    def alternar_pwd(self):
        self.mostrar_pwd = not self.mostrar_pwd
        self.entry_pwd.config(
            show="" if self.mostrar_pwd else "*"
        )

    def cargar_demo(self, rol, email, pwd):
        self.seleccionar_rol(rol)
        self.var_email.set(email)
        self.var_pwd.set(pwd)
        self.lbl_error.config(text="")

    def cargar_demo_por_rol(self, rol):
        # Buscar una cuenta demo en la fuente central
        for email, usuario in datos_demo.USUARIOS.items():
            if usuario.get("rol") == rol:
                self.cargar_demo(
                    rol,
                    email,
                    usuario["clave"]
                )
                return

        self.lbl_error.config(
            text="No hay una cuenta demo para este rol."
        )

    def validar_login(self):
        email = self.var_email.get().strip()
        pwd = self.var_pwd.get()
        rol = self.rol_seleccionado.get()

        usuario = datos_demo.USUARIOS.get(email)

        # Validar existencia, contraseña y rol
        if (
            usuario
            and usuario.get("clave") == pwd
            and usuario.get("rol") == rol
        ):
            self.lbl_error.config(text="")
            self.var_pwd.set("")
            self.app.iniciar_sesion(email)
        else:
            self.lbl_error.config(
                text="⚠️ Credenciales incorrectas o rol no coincidente."
            )

    def actualizar(self):
        # Limpiar formulario al regresar a esta pantalla
        self.var_email.set("")
        self.var_pwd.set("")
        self.lbl_error.config(text="")
        self.seleccionar_rol("restaurante")
