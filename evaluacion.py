class Evaluacion:
    def __init__(self, id_inscripcion,fecha_inscripcion,periodo,especialidad,modalidad,campo_conocimiento):
        self.id_inscripcion = id_inscripcion
        self.fecha = fecha_inscripcion
        self.periodo = periodo
        self.especialidad = especialidad
        self.modalidad = modalidad
        self.campo_conocimiento = campo_conocimiento
        self.resultado = None
        self.sede = None
    
    def programar(self,nueva_fecha):
        print("Evaluacion programada para {self.fecha_inscripcion}")

    def asignar_sede(self,sede):
        print("Asignando sede...")

    def registrar_resultados(self,resultado):
        print("Registrando resultados...")

    def generar_certificados(self):
        print("Generando certificados de evaluacion....")