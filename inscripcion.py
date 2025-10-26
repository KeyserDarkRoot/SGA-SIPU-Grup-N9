from datetime import datetime
import uuid

class Inscripcion:
    def __init__(self, periodo_id, ies_id, tipo_documento, documento, nombres, apellidos, carrera_seleccionada, fecha_inscripcion=None, estado="registrado"):
        self.id_inscripcion = str(uuid.uuid4())  # ID único
        self.periodo_id = periodo_id
        self.ies_id = ies_id
        self.tipo_documento = tipo_documento
        self.documento = documento
        self.nombres = nombres
        self.apellidos = apellidos
        self.carrera_seleccionada = carrera_seleccionada
        self.fecha_inscripcion = fecha_inscripcion or datetime.now().isoformat()
        self.estado = estado

    def validar_periodo(self, periodo_objeto):
        return periodo_objeto.estado == "activo" and periodo_objeto.validar_fecha_actual(self.fecha_inscripcion)

    def validar_registro_nacional(self, cliente_supabase):
        try:
            resultado = cliente_supabase.table("registronacional") \
                .select("identificacion") \
                .eq("identificacion", self.documento) \
                .execute()

            if resultado.data:
                return True
            else:
                print("Usted no realizó el registro nacional. Intente inscribirse en el próximo periodo.")
                return False
        except Exception as e:
            print("rror al validar registro nacional:", e)
            return False

    def guardar_en_supabase(self, cliente_supabase):
        datos = {
            "ID_INSCRIPCION": self.id_inscripcion,
            "PERIODO_ID": self.periodo_id,
            "IES_ID": self.ies_id,
            "TIPO_DOCUMENTO": self.tipo_documento,
            "DOCUMENTO": self.documento,
            "NOMBRES": self.nombres,
            "APELLIDOS": self.apellidos,
            "FECHA_INSCRIPCION": self.fecha_inscripcion,
            "CARRERA_SELECCIONADA": self.carrera_seleccionada,
            "ESTADO": self.estado
        }

        try:
            cliente_supabase.table("inscripciones").insert(datos).execute()
            self.registrarInscripcion()
            self.generar_certificado()
        except Exception as e:
            print(f"Error al guardar inscripción: {e}")

    def registrarInscripcion(self):
        print("Registro exitoso.")

    def generar_certificado(self):
        print(f"Certificado generado para {self.nombres} {self.apellidos} - Documento: {self.documento}")

    def consultarHistorial(self):
        print("Consulta de historial exitosa.")

    def consultarInscripcion(self):
        print(f"Inscripción a {self.carrera_seleccionada} en periodo {self.periodo_id}")

    def __str__(self):
        return f"Inscripción {self.id_inscripcion} - {self.carrera_seleccionada} ({self.estado})"