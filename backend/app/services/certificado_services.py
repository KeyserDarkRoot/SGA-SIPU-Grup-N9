from app.services.certificado import CertificadoInscripcion, CertificadoEvaluacion
from abc import ABC, abstractmethod
from fpdf import FPDF

class CertificadoBase(ABC):
    def __init__(self, supabase_client):
        self.supabase = supabase_client
        self.pdf = FPDF()

    @abstractmethod
    def recopilar_datos(self, cedula):
        pass

    @abstractmethod
    def diseñar_pdf(self, datos):
        pass

    def generar(self, cedula):
        datos = self.recopilar_datos(cedula)
        if not datos: 
            return None
        self.diseñar_pdf(datos)
        # Retorna los bytes del PDF
        return self.pdf.output(dest='S').encode('latin-1')

class CertificadoInscripcion(CertificadoBase):
    def recopilar_datos(self, cedula):
        res = self.supabase.table("inscripciones").select("*").eq("identificacion", cedula).execute()
        return res.data

    def diseñar_pdf(self, datos):
        self.pdf.add_page()
        
        # Nombre de la Universidad (Encabezado principal)
        self.pdf.set_font("Arial", 'B', 18)
        self.pdf.cell(200, 10, txt="UNIVERSIDAD LAICA ELOY ALFARO DE MANABÍ", ln=True, align='C')
        
        # Subtítulo del documento
        self.pdf.set_font("Arial", 'B', 14)
        self.pdf.cell(200, 10, txt="COMPROBANTE DE INSCRIPCIÓN - SIPU", ln=True, align='C')
        self.pdf.ln(10)
        
        # Sección: DATOS DEL ASPIRANTE
        self.pdf.set_font("Arial", 'B', 12)
        self.pdf.cell(200, 10, txt="DATOS DEL ASPIRANTE", ln=True)
        
        self.pdf.set_font("Arial", size=11)
        aspirante = datos[0]
        self.pdf.cell(200, 8, txt=f"Nombres: {aspirante['nombres']} {aspirante['apellidos']}", ln=True)
        self.pdf.cell(200, 8, txt=f"Identificación: {aspirante['identificacion']}", ln=True)
        self.pdf.ln(5)
        
        # Sección: DETALLE DE INSCRIPCIÓN
        self.pdf.set_font("Arial", 'B', 12)
        self.pdf.cell(200, 10, txt="DETALLE DE INSCRIPCIÓN", ln=True)
        
        self.pdf.set_font("Arial", size=10)
        for registro in datos:
            # Recuperamos los datos de las columnas de Supabase
            carrera = registro.get('carrera_seleccionada') or "No registrada"
            sede = registro.get('nombre_sede') or "No asignada"
            fecha = registro.get('fecha_inscripcion') or "N/A"
            
            detalle = f"Carrera: {carrera}\nSede: {sede}\nFecha: {fecha}"
            
            self.pdf.multi_cell(0, 8, txt=detalle)
            self.pdf.ln(2)
            self.pdf.cell(0, 0, "", "T") # Línea divisoria
            self.pdf.ln(5)

class CertificadoEvaluacion(CertificadoBase):
    def recopilar_datos(self, cedula):
        # Aquí cambias la tabla a la de tus exámenes
        res = self.supabase.table("evaluaciones").select("*").eq("identificacion", cedula).execute()
        return res.data

    def diseñar_pdf(self, datos):
        self.pdf.add_page()
        self.pdf.set_font("Arial", 'B', 16)
        self.pdf.cell(200, 10, txt="CERTIFICADO DE RESULTADOS", ln=True, align='C')
        # ... lógica de diseño para notas