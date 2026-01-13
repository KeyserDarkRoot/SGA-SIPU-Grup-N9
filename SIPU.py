import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import webbrowser # Para simular el envío de correos o links
import smtplib
from email.message import EmailMessage
from ConexionBD.api_supabase import crear_cliente  # Tu archivo existente

class SistemaSIPU:
    def __init__(self, root):
        self.root = root
        self.supabase = crear_cliente()
        self.root.title("SIPU - Sistema de Inscripción y Postulación")
        self.root.geometry("400x500")
        self.root.configure(bg="#f0f2f5")
        
        # Configuración de correo (REEMPLAZA ESTO)
        self.EMAIL_EMISOR = "tu_correo@gmail.com"
        self.EMAIL_PASSWORD = "tu_clave_de_16_letras" 

        self.mostrar_login()
        
    def enviar_correo(self, destinatario, asunto, mensaje):
        try:
            msg = EmailMessage()
            msg.set_content(mensaje)
            msg['Subject'] = asunto
            msg['From'] = self.EMAIL_EMISOR
            msg['To'] = destinatario

            # Servidor SMTP de Gmail
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(self.EMAIL_EMISOR, self.EMAIL_PASSWORD)
                smtp.send_message(msg)
            return True
        except Exception as e:
            print(f"Error SMTP: {e}")
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
            
    def proceso_recuperar(self):
        self.root.geometry("400x500")
        
        frame = tk.Frame(self.root, bg="white", padx=40, pady=40)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        cedula = simpledialog.askstring("Recuperar contraseña", "Ingrese su cédula/pasaporte:")
        if not cedula: return

        try:
            # Buscamos usando el nombre de columna correcto
            res = self.supabase.table("usuarios").select("correo", "contrasena", "nombre_completo").eq("cedula", cedula).execute()
            
            if res.data:
                u = res.data[0]
                asunto = "Recuperación de Acceso SIPU"
                mensaje = f"Hola {u['nombre_completo']},\n\nTu contraseña es: {u['contrasena']}"
                
                if self.enviar_correo(u['correo'], asunto, mensaje):
                    messagebox.showinfo("Éxito", f"Clave enviada a: {u['correo']}")
                else:
                    messagebox.showerror("Error", "Servidor de correo no disponible.")
            else:
                messagebox.showerror("Error", "Cédula/pasaporte no registrado.")
        except Exception as e:
            print(f"Error Recuperar: {e}")
            


    # --- DASHBOARD PRINCIPAL (Pantalla Completa) ---
    def abrir_dashboard(self):
        self.limpiar_pantalla()
        self.root.state('zoomed') # Pantalla completa
        
        # Colores
        color_sidebar = "#2c3e50"
        color_main = "#ecf0f1"

        # --- SIDEBAR (Panel Izquierdo) ---
        sidebar = tk.Frame(self.root, bg=color_sidebar, width=250)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="SIPU", font=("Helvetica", 30, "bold"), bg=color_sidebar, fg="white", pady=20).pack()
        tk.Frame(sidebar, bg="white", height=1, width=200).pack(pady=10)
        
        # Info Usuario
        tk.Label(sidebar, text=f"C.I: {self.usuario_actual['cedula']}", bg=color_sidebar, fg="#bdc3c7").pack(pady=5)
        tk.Label(sidebar, text=self.usuario_actual['correo'], bg=color_sidebar, fg="#bdc3c7", font=("Arial", 9)).pack()

        # Botón Cerrar Sesión al fondo
        btn_logout = tk.Button(sidebar, text="Cerrar Sesión", bg="#e74c3c", fg="white", 
                               relief="flat", command=self.mostrar_login)
        btn_logout.pack(side="bottom", fill="x", padx=20, pady=20)

        # --- ÁREA PRINCIPAL (Derecha) ---
        main_area = tk.Frame(self.root, bg=color_main)
        main_area.pack(side="right", expand=True, fill="both")

        # Cabecera
        header = tk.Frame(main_area, bg="white", height=100)
        header.pack(fill="x", padx=20, pady=20)
        
        tk.Label(header, text="Sistema de Inscripción y Postulación a las Universidades", 
                 font=("Helvetica", 18, "bold"), bg="white").pack(pady=(10, 0))
        tk.Label(header, text=f"Bienvenido(a), {self.usuario_actual['nombres']}", 
                 font=("Helvetica", 14), bg="white", fg="#7f8c8d").pack(pady=10)

        # --- SECCIONES DESPLEGABLES (Fases) ---
        self.crear_acordion(main_area, "FASE 1: REGISTRO NACIONAL", "Estado: REALIZADO ✅")
        self.crear_acordion(main_area, "FASE 2: INSCRIPCIÓN", "Seleccione una opción:", botones=True)

    def crear_acordion(self, parent, titulo, contenido, botones=False):
        f = tk.Frame(parent, bg="white", bd=1, relief="groove")
        f.pack(fill="x", padx=40, pady=10)
        
        lbl_titulo = tk.Label(f, text=titulo, font=("Arial", 11, "bold"), bg="#f8f9fa", anchor="w", padx=10)
        lbl_titulo.pack(fill="x")

        detalles = tk.Frame(f, bg="white", pady=15)
        
        if not botones:
            tk.Label(detalles, text=contenido, bg="white", font=("Arial", 10)).pack(padx=20)
        else:
            tk.Label(detalles, text=contenido, bg="white").pack(pady=5)
            btn_frame = tk.Frame(detalles, bg="white")
            btn_frame.pack()
            ttk.Button(btn_frame, text="Registrarse").pack(side="left", padx=5)
            ttk.Button(btn_frame, text="Certificado").pack(side="left", padx=5)

        # Lógica de despliegue
        detalles.pack(fill="x") # Por defecto abierto, se puede añadir lógica para ocultar

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaSIPU(root)
    root.mainloop()