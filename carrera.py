import OfertaAcademica

class Carrera:
    def __init__(self, idCarrera, nombreCarrera, facultad, modalidad, cuposDisponibles):
        self.__idCarrera = idCarrera
        self.nombreCarrera = nombreCarrera
        self.facultad = facultad
        self.modalidad = modalidad
        self.cuposDisponibles = cuposDisponibles

    def asignarCupos(self, numero):
        print(f"Asignando {numero} cupos a {self.nombreCarrera}")

    def obtenerinfo(self):
        print(f"Carrera: {self.nombreCarrera}, Facultad: {self.facultad}, Modalidad: {self.modalidad}")

#herenci simple
class CarreraVirtual(Carrera):   
    def __init__(self, idCarrera, nombreCarrera, facultad, modalidad, cuposDisponibles, plataforma):
        super().__init__(idCarrera, nombreCarrera, facultad, modalidad, cuposDisponibles)
        self.plataforma = plataforma

    def obtenerinfo(self):
        super().obtenerinfo()
        print(f"Modalidad virtual - Plataforma: {self.plataforma}")



class Aspirante(Carrera, OfertaAcademica):
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
        print(f"Tiene una beca de tipo: {self.tipoBeca}")


c1 = Carrera(1, "Ingeniería en Sistemas", "Facultad de Ingeniería", "Presencial", 50)
c2 = CarreraVirtual(2, "Diseño Web", "Facultad de Artes", "Virtual", 30, "Moodle")

oferta = OfertaAcademica(1, "2025A", "Universidad Central", [c1], "2025-01-10", "Activa")
oferta.agregarCarrera(c2)
oferta.listarCarrera()


asp1 = Aspirante(1, "Mateo", c1)
asp1.mostrarInteres()

asp2 = AspiranteBecado(2, "Ana", c2, "Excelencia Académica")
asp2.mostrarInteres()