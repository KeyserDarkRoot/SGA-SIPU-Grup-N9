class Postulacion:
    def __init__(self, idPostulacion,opcionesCarrera,prioridad,carreraSeleccionada):
        self.idPostulacion = idPostulacion
        self.opcionesCarrera = opcionesCarrera
        self.prioridad = prioridad
        self.carreraSeleccionada = carreraSeleccionada

    def registrarOpciones(self):
        print("ERegistro exitoso")

    def calcularPuntajeFinal(self):
        print("Calculando puntaje.")

    def GenerarCertificadoPostulacion(self):
        print("Generando certificados de evaluacion....")