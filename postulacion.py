from abc import ABC, abstractmethod

#Interfaz de certificados
class ICertificado(ABC):
    @abstractmethod
    def generar_certificado_postulacion(self):
        pass

class RegistroUnico:
    def obtener_datos_postulante(self, id_postulacion):
        return {
            "nombre": "Juan Pérez",
            "puntaje": 850,
            "documento": "1728392010"
        }

class Postulacion:
    def __init__(self, idPostulacion,opcionesCarrera,prioridad,carreraSeleccionada,registro):
        
        self.idPostulacion = idPostulacion
        self.opcionesCarrera = opcionesCarrera
        self.prioridad = prioridad
        self.carreraSeleccionada = carreraSeleccionada
        self.registro = registro

    def registrarOpciones(self): 
        print("ERegistro exitoso") 

    def calcularPuntajeFinal(self): 
        print("Calculando puntaje.") 

    def GenerarCertificadoPostulacion(self): 
        print("Generando certificados de evaluacion....")

