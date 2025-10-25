class Inscripcion:
    def __init__(self, id_inscripcion,fecha_inscripcion,periodo,carrera_seleccionada,estado):
        self.id_inscripcion = id_inscripcion
        self.fecha = fecha_inscripcion
        self.periodo = periodo
        self.carrera_seleccionada = carrera_seleccionada
        self.estado = estado

    def registrarInscripcion(self):
        print("Registro exitoso.")

    def validarPeriodo(self,):
        print("validacion de periodo")

    def consultarHistorial(self,):
        print("Consulta exitosa.")

    def generarCertificados(self):
        print("Generando certificados de inscripcion....")

    def consultarInscripcion(self):
        print(f"Inscripción a {self.carrera_seleccionada} en periodo {self.periodo}")

    def __str__(self):
        return f"Inscripción {self.id_inscripcion} - {self.carrera_seleccionada} ({self.estado})"