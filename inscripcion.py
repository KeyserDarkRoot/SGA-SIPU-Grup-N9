class Inscripcion:
    def __init__(self, id_inscripcion, periodo_id, ies_id, tipo_documento, documento, nombres, apellidos, fecha_inscripcion,carrera_seleccionada, estado="registrado"):
        self.id_inscripcion = id_inscripcion
        self.periodo_id = periodo_id
        self.ies_id = ies_id
        self.tipo_documento = tipo_documento
        self.documento = documento
        self.nombres = nombres
        self.apellidos = apellidos
        self.fecha_inscripcion = fecha_inscripcion
        self.carrera_seleccionada = carrera_seleccionada
        self.estado = estado

    def generar_certificado(self):
        print(f"Certificado generado para {self.nombres} {self.apellidos} - {self.documento}")

    def registrarInscripcion(self):
        print("Registro exitoso.")

    def validar_periodo(self, periodo_objeto):
        return periodo_objeto.validar_fecha_actual(self.fecha_inscripcion)

    def consultarHistorial(self,):
        print("Consulta exitosa.")

    def consultarInscripcion(self):
        print(f"Inscripción a {self.carrera_seleccionada} en periodo {self.periodo}")

    def __str__(self):
        return f"Inscripción {self.id_inscripcion} - {self.carrera_seleccionada} ({self.estado})"