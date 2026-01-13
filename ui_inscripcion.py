import tkinter as tk
from tkinter import messagebox, ttk
from inscripcion import Inscripcion # Importamos TU clase lógica

class VentanaFormularioInscripcion:
    def __init__(self, root, datos_rn):
        self.root = root
        self.root.title("Formulario de Inscripción - SIPU")
        self.datos_rn = datos_rn # Aquí vienen nombres, apellidos, estado, etc.

        # Contenedor
        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack()

        # Mostrar Datos del Registro Nacional (Lectura)
        tk.Label(self.frame, text=f"Aspirante: {datos_rn['nombres']} {datos_rn['apellidos']}", font=("Arial", 10, "bold")).pack(pady=5)
        
        # Etiqueta de aviso para CONDICIONADOS
        if datos_rn.get('estadoRegistroNacional') == 'CONDICIONADO':
            lbl_aviso = tk.Label(self.frame, text="ESTADO: CONDICIONADO (Sujeto a revisión)", fg="orange", font=("Arial", 9, "italic"))
            lbl_aviso.pack()

        # --- SELECCIÓN DE CARRERA ---
        tk.Label(self.frame, text="Seleccione Carrera:").pack(pady=(10,0))
        # En un sistema real, esto vendría de la BD (OfertaAcademica)
        self.combo_carrera = ttk.Combobox(self.frame, values=["Ingeniería de Software", "Medicina", "Derecho", "Arquitectura"], state="readonly")
        self.combo_carrera.pack(pady=5)

        # --- SELECCIÓN DE SEDE (NUEVO - REQUERIDO) ---
        tk.Label(self.frame, text="Seleccione Sede:").pack(pady=(10,0))
        self.combo_sede = ttk.Combobox(self.frame, values=["Matriz Manta", "Extensión Chone", "Extensión Bahía"], state="readonly")
        self.combo_sede.pack(pady=5)

        # --- ID INSTITUCIÓN ---
        tk.Label(self.frame, text="ID de la Institución (IES_ID):").pack()
        self.ent_ies = tk.Entry(self.frame)
        self.ent_ies.insert(0, "101") # Valor ejemplo
        self.ent_ies.pack(pady=5)

        # Botón para Guardar usando tu método 'guardar_en_supabase'
        self.btn_inscribir = tk.Button(self.frame, text="Finalizar Inscripción", 
                                       command=self.ejecutar_inscripcion, bg="#2ecc71", fg="white", font=("Arial", 10, "bold"))
        self.btn_inscribir.pack(pady=20)

    def ejecutar_inscripcion(self):
        carrera = self.combo_carrera.get()
        sede = self.combo_sede.get()
        ies = self.ent_ies.get()

        # Validaciones de interfaz
        if not carrera:
            messagebox.showwarning("Error", "Debe seleccionar una carrera")
            return
        if not sede:
            messagebox.showwarning("Error", "Debe seleccionar una sede")
            return

        # --- INSTANCIAMOS TU CLASE LÓGICA ---
        # Usamos los datos que ya validó el Registro Nacional + los de la interfaz
        try:
            nueva_inscripcion = Inscripcion(
                periodo_id=None, # Tu método validar_periodo lo asignará automáticamente buscando en BD
                ies_id=ies,
                tipo_documento=self.datos_rn.get('tipoDocumento', 'cédula'),
                identificacion=self.datos_rn['identificacion'],
                nombres=self.datos_rn['nombres'],
                apellidos=self.datos_rn['apellidos'],
                carrera_seleccionada=carrera,
                nombre_sede=sede # <--- ¡ESTO FALTABA Y ERA OBLIGATORIO!
            )

            # --- LLAMAMOS A TU MÉTODO DE ABSTRACCIÓN ---
            # Este método ya valida el periodo, inserta en Supabase, registra y genera certificado
            nueva_inscripcion.guardar_en_supabase()
            
            messagebox.showinfo("Éxito", f"Inscripción guardada correctamente.\nCertificado generado para {self.datos_rn['nombres']}")
            self.root.destroy() # Cierra la ventana al terminar

        except Exception as e:
            print(f"Error detallado: {e}")
            messagebox.showerror("Error Crítico", f"Fallo al guardar en el sistema: {e}")