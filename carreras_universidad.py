from ofertaAcademica import OfertaAcademica

class Carrera:
    def __init__(self, idCarrera, nombreCarrera, facultad, modalidad, duracion, cuposDisponibles):
        self.__idCarrera = idCarrera
        self.nombreCarrera = nombreCarrera
        self.facultad = facultad
        self.modalidad = modalidad
        self.duracion = duracion
        self.cuposDisponibles = cuposDisponibles

    def asignarCupos(self, numero):
        self.cuposDisponibles += numero
        print(f"{numero} cupos asignados a {self.nombreCarrera}. Total: {self.cuposDisponibles}")

    def obtenerinfo(self):
        print(f"Carrera: {self.nombreCarrera}")
        print(f"Facultad: {self.facultad}")
        print(f"Modalidad: {self.modalidad}")
        print(f"Duración: {self.duracion}")
        print(f"Cupos disponibles: {self.cuposDisponibles}")


class CarreraVirtual(Carrera):
    def __init__(self, idCarrera, nombreCarrera, facultad, modalidad, duracion, cuposDisponibles, plataforma):
        super().__init__(idCarrera, nombreCarrera, facultad, modalidad, duracion, cuposDisponibles)
        self.plataforma = plataforma

    def obtenerinfo(self):
        super().obtenerinfo()
        print(f"Modalidad virtual - Plataforma: {self.plataforma}")




'''class Aspirante(Carrera, OfertaAcademica):
    def __init__(self, idAspirante, nombre, carrera_interes):
        self.idAspirante = idAspirante
        self.nombre = nombre
        self.carrera_interes = carrera_interes

    def mostrarInteres(self):
        print(f"{self.nombre} está interesado en la carrera {self.carrera_interes.nombreCarrera}")


# HERENCIA DE HERENCIA
class AspiranteBecado(Aspirante):   # Hereda de Aspirante (que puede heredar de otras)
    def __init__(self, idAspirante, nombre, carrera_interes, tipoBeca):
        super().__init__(idAspirante, nombre, carrera_interes)
        self.tipoBeca = tipoBeca

    def mostrarInteres(self):
        super().mostrarInteres()
        print(f"Tiene una beca de tipo: {self.tipoBeca}")'''