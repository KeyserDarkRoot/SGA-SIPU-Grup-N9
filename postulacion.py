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

    def registrar_opciones(self):
        print(f"Registro exitoso: {self.opciones_carrera}")

    def calcular_puntaje_final(self):
        puntaje_base = 600
        puntaje_prioridad = self.prioridad * 50
        puntaje_total = puntaje_base + puntaje_prioridad
        print(f"Puntaje final: {puntaje_total}")
        return puntaje_total

    def generar_certificado_postulacion(self):
        print(f"Generando certificado para la carrera {self.carrera_seleccionada}")
        if self.registro:
            datos = self.registro.obtener_datos_postulante(self.id_postulacion)
            print(f"Datos del postulante: {datos}")
        else:
            print("Registro único no disponible.")