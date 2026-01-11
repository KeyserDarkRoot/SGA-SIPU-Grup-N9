import tkinter as tk
from tkinter import messagebox, ttk
from serviciosExternos import ServicioRegistroNacional
# Importamos la interfaz que creamos en el otro archivo
from ui_inscripcion import VentanaFormularioInscripcion 

class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("SIPU - Sistema de Admisión 2025")
        self.root.geometry("400x300")
        
        # Instancia del servicio
        self.servicio_rn = ServicioRegistroNacional()

        # Diseño
        self.frame = tk.Frame(self.root, padx=30, pady=30)
        self.frame.pack(expand=True)

        tk.Label(self.frame, text="BIENVENIDO AL SIPU", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(self.frame, text="Ingrese su Identificación:").pack()
        
        self.ent_cedula = tk.Entry(self.frame, font=("Arial", 12), justify='center')
        self.ent_cedula.pack(pady=10)

        self.btn_validar = tk.Button(self.frame, text="Validar Registro", 
                                     command=self.proceso_validacion,
                                     bg="#3498db", fg="white", width=20)
        self.btn_validar.pack(pady=10)

    def proceso_validacion(self):
        cedula = self.ent_cedula.get().strip()
        if not cedula:
            messagebox.showwarning("Atención", "Por favor ingrese una identificación.")
            return

        # Consultamos a Supabase a través del servicio
        aspirante_data = self.servicio_rn.consultar_aspirante(cedula)

        if aspirante_data:
            estado = aspirante_data.get('estadoregistronacional', '').upper()
            
            # Lógica para HABILITADO y CONDICIONADO
            if estado in ['HABILITADO', 'CONDICIONADO']:
                msg = f"Bienvenido {aspirante_data['nombres']}.\nEstado: {estado}"
                messagebox.showinfo("Validación Exitosa", msg)
                
                # Pasamos a la siguiente ventana
                self.abrir_formulario_inscripcion(aspirante_data)
            else:
                messagebox.showerror("No Habilitado", 
                                     f"Lo sentimos, su estado es: {estado}.\nNo puede continuar.")
        else:
            messagebox.showerror("Error", "Cédula no encontrada en el Registro Nacional.")

    def abrir_formulario_inscripcion(self, datos):
        # Ocultamos la ventana principal para que no estorbe
        self.root.withdraw() 
        
        # Creamos una nueva ventana de nivel superior
        nueva_ventana = tk.Toplevel()
        
        # Al cerrar la ventana de inscripción, volvemos a mostrar la principal
        nueva_ventana.protocol("WM_DELETE_WINDOW", lambda: self.on_close_child(nueva_ventana))
        
        # Ejecutamos la interfaz de inscripción que ya tiene tu clase Inscripcion.py por dentro
        VentanaFormularioInscripcion(nueva_ventana, datos)

    def on_close_child(self, child_window):
        child_window.destroy()
        self.root.deiconify() # Muestra la principal otra vez

if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaPrincipal(root)
    root.mainloop()