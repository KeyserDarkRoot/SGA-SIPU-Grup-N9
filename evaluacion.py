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
    
    def programar(self, nueva_fecha):
        self.fecha = nueva_fecha
        print(f"Evaluación programada para {self.fecha}")

    def asignar_sede(self, sede):
        self.sede = sede
        print(f"Sede asignada: {self.sede.nombre_sede}")

    def registrar_resultados(self, resultado):
        self.resultado = resultado
        print(f"Resultado registrado: {self.resultado}")

    def generar_certificados(self):
        print("Generando certificados de evaluacion....")