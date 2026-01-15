import tkinter as tk
from tkinter import ttk, messagebox
from backend.app.core.inscripcion import Inscripcion
from backend.app.core.periodo import Periodo

class VistaInscripcion(tk.Frame):
    def __init__(self, parent, sipu_app):
        super().__init__(parent, bg="white")
        self.sipu = sipu_app  # Referencia a la app principal
        self.usuario = sipu_app.usuario_actual
        self.supabase = sipu_app.supabase
        
        # Almacén de datos temporal
        self.seleccion = {"ies_id": None, "carrera": None, "bloque": None}
        
        self.setup_ui()

    def setup_ui(self):
        # 1. BARRA DE PASOS (Encabezado)
        self.header_steps = tk.Frame(self, bg="#f8f9fa", height=60)
        self.header_steps.pack(fill="x")
        
        self.pasos_labels = {}
        for i, texto in enumerate(["1. DATOS PERSONALES", "2. UNIVERSIDAD Y BLOQUE", "3. POSTULACIÓN"]):
            lbl = tk.Label(self.header_steps, text=texto, font=("Helvetica", 9, "bold"), 
                           bg="#f8f9fa", fg="#bdc3c7", padx=20)
            lbl.pack(side="left", expand=True)
            self.pasos_labels[i+1] = lbl

        # 2. CONTENEDOR DINÁMICO
        self.contenedor_pasos = tk.Frame(self, bg="white", padx=40, pady=20)
        self.contenedor_pasos.pack(fill="both", expand=True)

        self.ir_paso_1()

    def limpiar_paso(self, num_paso):
        for w in self.contenedor_pasos.winfo_children(): w.destroy()
        for k, v in self.pasos_labels.items():
            v.config(fg="#bdc3c7", bg="#f8f9fa")
        self.pasos_labels[num_paso].config(fg="#3498db", bg="white")

    # --- PASO 1: DATOS PERSONALES ---
    def ir_paso_1(self):
        self.limpiar_paso(1)
        tk.Label(self.contenedor_pasos, text="Datos del Registro Nacional", font=("Arial", 14, "bold"), bg="white").pack(anchor="w", pady=10)
        
        # Consultar datos de registronacional
        res = self.supabase.table("registronacional").select("*").eq("identificacion", self.usuario['cedula']).execute()
        datos_rn = res.data[0] if res.data else {}

        # Rejilla de datos (Solo lectura)
        grid = tk.Frame(self.contenedor_pasos, bg="white")
        grid.pack(fill="x", pady=20)

        campos = [
            ("Identificación", "identificacion"), ("Nombres", "nombres"),
            ("Apellidos", "apellidos"), ("Nacionalidad", "nacionalidad"),
            ("Fecha Nacimiento", "fechanacimiento"), ("Sexo", "sexo"),
            ("Género", "genero"), ("Autoidentificación", "autoidentificacion")
        ]

        for i, (label, key) in enumerate(campos):
            r, c = divmod(i, 2)
            tk.Label(grid, text=f"{label}:", bg="white", fg="gray").grid(row=r, column=c*2, sticky="w", pady=5)
            val = tk.Label(grid, text=datos_rn.get(key, "N/A"), bg="white", font=("Arial", 10, "bold"))
            val.grid(row=r, column=c*2+1, sticky="w", padx=(10, 40))

        ttk.Button(self.contenedor_pasos, text="Siguiente", command=self.ir_paso_2).pack(anchor="e")

    # --- PASO 2: BLOQUE DE CONOCIMIENTO ---
    def ir_paso_2(self):
        self.limpiar_paso(2)
        tk.Label(self.contenedor_pasos, text="Selección de Universidad y Carrera", font=("Arial", 14, "bold"), bg="white").pack(anchor="w")

        # Universidad
        tk.Label(self.contenedor_pasos, text="Elija la Universidad:", bg="white").pack(anchor="w", pady=(20,5))
        self.cb_uni = ttk.Combobox(self.contenedor_pasos, width=50, state="readonly")
        self.cb_uni.pack(anchor="w")
        
        res_uni = self.supabase.table("universidad").select("ies_id, nombre").execute()
        unis = {u['nombre']: u['ies_id'] for u in res_uni.data}
        self.cb_uni['values'] = list(unis.keys())

        # Tabla de Carreras (Simulando Bloques de Conocimiento)
        tk.Label(self.contenedor_pasos, text="Oferta Académica:", bg="white").pack(anchor="w", pady=(20,5))
        self.tree = ttk.Treeview(self.contenedor_pasos, columns=("Bloque", "Carrera", "Cupos"), show="headings", height=8)
        self.tree.heading("Bloque", text="Bloque de Conocimiento")
        self.tree.heading("Carrera", text="Carrera")
        self.tree.heading("Cupos", text="Cupos")
        self.tree.pack(fill="x")

        # Cargar datos de oferta_academica
        res_oferta = self.supabase.table("oferta_academica").select("*").execute()
        for o in res_oferta.data:
            self.tree.insert("", "end", values=(o['BloqueConocimiento'], o['nombre_carrera'], o['cupos_disponibles']))

        def guardar_seleccion():
            sel = self.tree.selection()
            if not sel or not self.cb_uni.get():
                messagebox.showwarning("Atención", "Seleccione universidad y carrera")
                return
            item = self.tree.item(sel[0])['values']
            self.seleccion = {"ies_id": unis[self.cb_uni.get()], "carrera": item[1], "bloque": item[0]}
            self.ir_paso_3()

        btn_f = tk.Frame(self.contenedor_pasos, bg="white")
        btn_f.pack(fill="x", pady=20)
        ttk.Button(btn_f, text="Atrás", command=self.ir_paso_1).pack(side="left")
        ttk.Button(btn_f, text="Siguiente", command=guardar_seleccion).pack(side="right")

    # --- PASO 3: POSTULACIÓN ---
    def ir_paso_3(self):
        self.limpiar_paso(3)
        tk.Label(self.contenedor_pasos, text="Confirmación de Postulación", font=("Arial", 14, "bold"), bg="white").pack(anchor="w")
        
        resumen = f"Carrera: {self.seleccion['carrera']}\nBloque: {self.seleccion['bloque']}\nIES ID: {self.seleccion['ies_id']}"
        tk.Label(self.contenedor_pasos, text=resumen, bg="#f1f2f6", justify="left", padx=20, pady=20, font=("Courier", 11)).pack(fill="x", pady=20)

        def finalizar():
            try:
                # INSTANCIA DE TU CLASE INSCRIPCION.PY
                nueva = Inscripcion(
                    periodo_id=None, # Se valida en guardar_en_supabase
                    ies_id=self.seleccion['ies_id'],
                    tipo_documento="Cédula",
                    identificacion=self.usuario['cedula'],
                    nombres=self.usuario['nombres'],
                    apellidos=self.usuario['apellidos'],
                    carrera_seleccionada=self.seleccion['carrera']
                )
                nueva.guardar_en_supabase() # Tu método ya hace todo el trabajo
                messagebox.showinfo("Éxito", "Inscripción registrada correctamente.")
                self.sipu.abrir_dashboard() # Volver al inicio
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar: {e}")

        ttk.Button(self.contenedor_pasos, text="FINALIZAR REGISTRO", command=finalizar).pack()
