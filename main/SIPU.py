import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import webbrowser # Para simular el envío de correos o links
import smtplib
from email.message import EmailMessage
from backend.app.database.ConexionBD.api_supabase import crear_cliente  # Tu archivo existente

class SistemaSIPU:
    def __init__(self, root):
        self.root = root
        self.supabase = crear_cliente()
        self.root.title("SIPU - Sistema de Inscripción y Postulación")
        self.root.geometry("400x500")
        self.root.configure(bg="#f0f2f5")
        
        # Configuración de correo
        self.EMAIL_EMISOR = "brithany.macias.t@gmail.com"
        self.EMAIL_PASSWORD = "hftdqcpkqmkhnlop" 

        self.mostrar_login()
        
    def enviar_correo(self, destinatario, asunto, mensaje):
        try:
            msg = EmailMessage()
            msg.set_content(mensaje)
            msg['Subject'] = asunto
            msg['From'] = self.EMAIL_EMISOR
            msg['To'] = destinatario

            with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10) as smtp:
                smtp.login(self.EMAIL_EMISOR, self.EMAIL_PASSWORD)
                smtp.send_message(msg)
            return True
        except Exception as e:
            print(f"Detalle del error SMTP: {e}") 
            return False

    # --- VISTAS DE ACCESO ---
    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def mostrar_login(self):
        self.limpiar_pantalla()
        self.root.state('normal')
        self.root.geometry("400x500")
        
        frame = tk.Frame(self.root, bg="white", padx=40, pady=40)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="SIPU", font=("Helvetica", 24, "bold"), bg="white", fg="#2c3e50").pack(pady=10)
        tk.Label(frame, text="Iniciar Sesión", font=("Helvetica", 12), bg="white", fg="gray").pack()

        tk.Label(frame, text="Identificación:", bg="white").pack(anchor="w", pady=(20, 0))
        self.ent_user = ttk.Entry(frame, width=30)
        self.ent_user.pack(pady=5)

        tk.Label(frame, text="Contraseña:", bg="white").pack(anchor="w")
        self.ent_pass = ttk.Entry(frame, width=30, show="*")
        self.ent_pass.pack(pady=5)

        ttk.Button(frame, text="Iniciar Sesión", command=self.proceso_login).pack(pady=20, fill="x")
        
        tk.Button(frame, text="¿Olvidó su contraseña?", fg="#3498db", bg="white", borderwidth=0, 
                  command=self.proceso_recuperar).pack()
        tk.Button(frame, text="Crear una cuenta nueva", fg="#2ecc71", bg="white", borderwidth=0, 
                  command=self.mostrar_registro).pack(pady=10)
        

    def mostrar_registro(self):
        self.limpiar_pantalla()
        frame = tk.Frame(self.root, bg="white", padx=30, pady=30)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        frame.pack(expand=True)

        tk.Label(frame, text="Crear Cuenta", font=("Arial", 16, "bold"), bg="white").pack(pady=10)
        
        campos = ["Cédula/Pasaporte", "Correo", "Contraseña", "Confirmar Contraseña"]
        self.entries_reg = {}
        
        for campo in campos:
            tk.Label(frame, text=campo + ":", bg="white").pack(anchor="w")
            entry = ttk.Entry(frame, width=30, show="*" if "Contraseña" in campo else "")
            entry.pack(pady=5)
            self.entries_reg[campo] = entry

        ttk.Button(frame, text="Registrarse", command=self.proceso_registro).pack(pady=20, fill="x")
        tk.Button(frame, text="Volver", command=self.mostrar_login, borderwidth=0, bg="white").pack()
        
# --- LÓGICA CON SUPABASE ---
    def proceso_login(self):
        cedula = self.ent_user.get()
        contra = self.ent_pass.get()

        res = self.supabase.table("usuarios").select("*").eq("cedula", cedula).execute()
        
        if res.data and res.data[0]['contrasena'] == contra:
            self.usuario_actual = res.data[0]
            self.abrir_dashboard()
        else:
            messagebox.showerror("Error", "Cédula/pasaporte o contraseña incorrectos")

    def proceso_registro(self):
        cedula_input = self.entries_reg["Cédula/Pasaporte"].get().strip()
        correo_input = self.entries_reg["Correo"].get().strip()
        contra_input = self.entries_reg["Contraseña"].get().strip()
        confir_input = self.entries_reg["Confirmar Contraseña"].get().strip()

        # Validaciones básicas
        if not cedula_input or not correo_input or not contra_input:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if contra_input != confir_input:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return

        try:
            # 1. BUSCAR EN REGISTRO NACIONAL
            # Consultamos nombres y apellidos usando la cédula ingresada
            res_rn = self.supabase.table("registronacional").select("nombres, apellidos").eq("identificacion", cedula_input).execute()
            
            if not res_rn.data:
                messagebox.showerror("No Habilitado", "La cédula/pasaporte no consta en el Registro Nacional. No puede crear una cuenta.")
                return

            # Extraemos los datos de la tabla oficial
            datos_oficiales = res_rn.data[0]
            nombres_reales = datos_oficiales['nombres']
            apellidos_reales = datos_oficiales['apellidos']

            # 2. INSERTAR EN LA TABLA USUARIOS
            # Aquí asignamos el rol 'Aspirante' por defecto y los datos extraídos
            self.supabase.table("usuarios").insert({
                "cedula": cedula_input,
                "rol": "Aspirante",           # Rol automático
                "nombres": nombres_reales,    # De Registro Nacional
                "apellidos": apellidos_reales, # De Registro Nacional
                "correo": correo_input,
                "contrasena": contra_input
                # fecha_creacion se pone sola en Supabase si es 'now()'
            }).execute()

            # 3. NOTIFICACIÓN AL CORREO
            asunto = "Bienvenido al SIPU - Registro Exitoso"
            cuerpo = f"Hola {nombres_reales},\n\nTu cuenta ha sido creada exitosamente.\nUsuario: {cedula_input}\nRol: Aspirante"
            self.enviar_correo(correo_input, asunto, cuerpo)

            messagebox.showinfo("Éxito", f"¡Cuenta creada para {nombres_reales} {apellidos_reales}!")
            self.mostrar_login()

        except Exception as e:
            print(f"Error Registro: {e}")
            messagebox.showerror("Error", f"No se pudo completar el registro: {e}")
            
    # --- VISTA DE RECUPERACIÓN ESTILIZADA ---
    def proceso_recuperar(self):
        """Muestra el formulario de recuperación con el mismo estilo que el login"""
        self.limpiar_pantalla()
        self.root.state('normal')
        self.root.geometry("400x500")
        
        frame = tk.Frame(self.root, bg="white", padx=40, pady=40)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="SIPU", font=("Helvetica", 24, "bold"), bg="white", fg="#2c3e50").pack(pady=10)
        tk.Label(frame, text="Recuperar Contraseña", font=("Helvetica", 12), bg="white", fg="gray").pack()

        tk.Label(frame, text="Ingrese su Cédula/Pasaporte:", bg="white").pack(anchor="w", pady=(30, 0))
        self.ent_cedula_rec = ttk.Entry(frame, width=30)
        self.ent_cedula_rec.pack(pady=5)
        self.ent_cedula_rec.focus_set() # Pone el cursor automáticamente aquí

        # Botón para ejecutar la lógica
        ttk.Button(frame, text="Enviar Contraseña", command=self.ejecutar_recuperacion).pack(pady=20, fill="x")
        
        # Botón para volver
        tk.Button(frame, text="Volver al inicio de sesión", fg="#3498db", bg="white", borderwidth=0, 
                  command=self.mostrar_login).pack()

    def ejecutar_recuperacion(self):
        """Lógica que consulta Supabase y envía el correo"""
        cedula = self.ent_cedula_rec.get().strip()
        
        if not cedula:
            messagebox.showwarning("Atención", "Por favor, ingrese su identificación.")
            return

        try:
            # Consultamos los datos
            res = self.supabase.table("usuarios").select("correo", "contrasena", "nombres", "apellidos").eq("cedula", cedula).execute()
            
            if res.data:
                u = res.data[0]
                asunto = "Recuperación de Acceso SIPU"
                mensaje = f"Hola {u['nombres']} {u['apellidos']},\n\nTu contraseña registrada en SIPU es: {u['contrasena']}"
                
                # Intentar enviar
                if self.enviar_correo(u['correo'], asunto, mensaje):
                    messagebox.showinfo("Éxito", f"La contraseña ha sido enviada al correo:\n{u['correo']}")
                    self.mostrar_login() # Regresamos al login tras el éxito
                else:
                    messagebox.showerror("Error", "No se pudo conectar con el servidor de correos.\nVerifique su conexión o clave de aplicación.")
            else:
                messagebox.showerror("No Encontrado", "La identificación ingresada no existe en nuestro sistema.")
                
        except Exception as e:
            print(f"Error en BD: {e}")
            messagebox.showerror("Error", "Error al conectar con la base de datos.")
            


    # --- DASHBOARD PRINCIPAL (Pantalla Completa) ---
    def abrir_dashboard(self):
        self.limpiar_pantalla()
        self.root.state('zoomed') # Pantalla completa
        
        # Colores
        color_sidebar = "#2c3e50"
        color_main = "#f4f7f6"
        color_accent = "#3498db"

        # --- SIDEBAR (Panel Izquierdo) ---
        sidebar = tk.Frame(self.root, bg=color_sidebar, width=280)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="SIPU", font=("Helvetica", 32, "bold"), bg=color_sidebar, fg="white", pady=30).pack()
        tk.Frame(sidebar, bg="#34495e", height=2, width=220).pack(pady=10)
        
        # Info Usuario
        tk.Label(sidebar, text=f"C.I: {self.usuario_actual['cedula']}", bg=color_sidebar, fg="#bdc3c7").pack(pady=5)
        tk.Label(sidebar, text=self.usuario_actual['correo'], bg=color_sidebar, fg="#bdc3c7", font=("Arial", 9)).pack()

        # Botón Cerrar Sesión al fondo
        btn_logout = tk.Button(sidebar, text="Cerrar Sesión", bg="#e74c3c", fg="white", 
                               relief="flat", command=self.mostrar_login)
        btn_logout.pack(side="bottom", fill="x", padx=20, pady=20)

        # --- ÁREA PRINCIPAL (Derecha) ---
        self.main_area = tk.Frame(self.root, bg=color_main)
        self.main_area.pack(side="right", expand=True, fill="both")

        # Cabecera
        header = tk.Frame(self.main_area, bg="white", height=120)
        header.pack(fill="x", padx=30, pady=30)
        
        tk.Label(header, text="Sistema de Inscripción y Postulación a las Universidades", 
                 font=("Helvetica", 18, "bold"), bg="white").pack(pady=(10, 0))
        nombre_completo = f"{self.usuario_actual['nombres']} {self.usuario_actual['apellidos']}"
        tk.Label(header, text=f"Bienvenido(a), {nombre_completo}", 
                 font=("Helvetica", 14), bg="white", fg="#7f8c8d").pack(pady=10)

        # --- CONSULTA DE ESTADO EN SUPABASE ---
        estado_rn = "NO REGISTRADO"
        color_estado = "gray"
        icono = "❓"

        try:
            res_estado = self.supabase.table("registronacional").select("estadoregistronacional").eq("identificacion", self.usuario_actual['cedula']).execute()
            if res_estado.data:
                val = res_estado.data[0]['estadoregistronacional'].upper()
                estado_rn = val
                if val == "HABILITADO":
                    color_estado = "#2ecc71" # Verde
                    icono = "✅"
                elif val == "CONDICIONADO":
                    color_estado = "#f1c40f" # Amarillo
                    icono = "⚠️"
                else:
                    color_estado = "#e74c3c" # Rojo
                    icono = "❌"
        except:
            estado_rn = "ERROR DE CONEXIÓN"

        # --- SECCIONES (Fases) ---
        self.crear_acordion_pro(self.main_area, "FASE 1: REGISTRO NACIONAL", 
                               f"Su estado actual es: {estado_rn} {icono}", color_estado)
        
        self.crear_acordion_pro(self.main_area, "FASE 2: INSCRIPCIÓN Y EVALUACIÓN", 
                               "Complete su inscripción para la sede de examen.", "#3498db", botones=True)

    def crear_acordion_pro(self, parent, titulo, contenido, color_status, botones=False):
        # Contenedor principal de la tarjeta
        card = tk.Frame(parent, bg="white", bd=0, highlightthickness=1, highlightbackground="#dcdde1")
        card.pack(fill="x", padx=60, pady=10)
        
        # Encabezado de la fase
        head = tk.Frame(card, bg="#f8f9fa", height=40)
        head.pack(fill="x")
        tk.Label(head, text=titulo, font=("Arial", 10, "bold"), bg="#f8f9fa", fg="#34495e", padx=15).pack(side="left")

        # Cuerpo
        body = tk.Frame(card, bg="white", pady=20)
        body.pack(fill="x", padx=20)

        if not botones:
            lbl_status = tk.Label(body, text=contenido, font=("Arial", 12, "bold"), fg=color_status, bg="white")
            lbl_status.pack(anchor="w")
        else:
            tk.Label(body, text=contenido, bg="white", font=("Arial", 11)).pack(anchor="w", pady=(0, 15))
            btn_frame = tk.Frame(body, bg="white")
            btn_frame.pack(anchor="w")
            
            # Botones con estilo ttk
            style = ttk.Style()
            style.configure("Accent.TButton", font=("Arial", 10, "bold"))
            
            btn_reg = ttk.Button(btn_frame, text="Realizar Inscripción", width=25, 
                command=self.mostrar_formulario_inscripcion)
            btn_reg.pack(side="left", padx=(0, 10))

            btn_cert = ttk.Button(btn_frame, text="Descargar Certificado", width=25)
            btn_cert.pack(side="left")
            
    def mostrar_formulario_inscripcion(self):
        from ui.ui_inscripcion import VistaInscripcion
        # Limpiamos el contenido del área principal (conservando el sidebar)
        for widget in self.main_area.winfo_children():
            widget.destroy()
        
        # Cargamos la nueva vista de pasos
        self.vista_form = VistaInscripcion(self.main_area, self)
        self.vista_form.pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaSIPU(root)
    root.mainloop()