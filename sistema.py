class RegistroNacional:
    pass


class Universidad:
    def __init__(self, idUniversidad, nombre, direccion, sedes):
        self.__idUniversidad = idUniversidad
        self.nombre = nombre
        self.direccion = direccion
        self.sedes = sedes

    def cargarOferta():
        print("Cargando oferta académica...")

    def asignarSede():
        print("Asigando sedes...")

    def notificarAspirantes():
        print("Enviando notificaciones a los aspirantes...")

class Carrera:
    def __init__(self, idCarrera, nombreCarrera, facultad, modalidad, cuposDisponibles):
        self.__idCarrera = idCarrera
        self.nombreCarrera = nombreCarrera
        self.facultad = facultad
        self.modalidad = modalidad
        self.cuposDisponibles = cuposDisponibles

    def asignarCupos(self, numero):
        print(f"Asiganado {numero} cupos")

    def obtenerinfo(self):
        print("Obteniendo información de carrera...")

class OfertaAcademica:

    def __init__(self, idOferta, periodoAcademico, universidad, carreras, fechaPublicacion, estadoOferta):
        self.__idOferta = idOferta
        self.periodoAcademico = periodoAcademico
        self.universidad = universidad
        self.carreras = carreras
        self.fechaPublicacion = fechaPublicacion
        self.estadoOferta = estadoOferta

    def agregarCarrera(self, carrera):
        print("Agregando carrera a la oferta")

    def eliminarCarrera(self, carrera):
        print("Eliminando carrera de la oferta")

    def listarCarrera():
        print("Mostrando carreras enlistadas")

    def consultarDisponibilidad(self, carrera):
        print("Consultando disponibilidad de la carrera...")

    def publicarOferta(self):
        print("Publicando oferta académica...")


class Periodo:
    pass


class Sede:
    pass


class Laboratorio:
    pass


class Aspirante:
    pass


class Postulacion:
    pass


class Inscripcion:
    pass


class Evaluacion:
    pass


class Puntaje:
    pass


class Monitor:
    pass


class Notificacion:
    pass