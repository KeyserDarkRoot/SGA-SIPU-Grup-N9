class Carrera:
    def __init__(self, idCarrera, nombreCarrera, facultad, modalidad, cuposDisponibles):
        self.__idCarrera = idCarrera
        self.nombreCarrera = nombreCarrera
        self.facultad = facultad
        self.modalidad = modalidad
        self.cuposDisponibles = cuposDisponibles

    def asignarCupos(self, numero):
        self.cuposDisponibles += numero
        print(f"Asignado {numero} cupos a {self.nombreCarrera}")

    def obtenerinfo(self):
        return f"{self.nombreCarrera} - {self.facultad} ({self.modalidad})"