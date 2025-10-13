class RegistroNacional:
    pass



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
    def __init__(self, idLaboratorio, nombre, capacidad, estado):
        self.idLaboratorio = idLaboratorio
        self.nombre = nombre
        self.capacidad = capacidad
        self.estado = estado
        
    def reservar(self):
        if self.estado == "disponible" :
            self.estado = "ocupado"
            print(f"Laboratorio {self.nombre} (ID: {self.idLaboratorio}) ha sido reservado)")
            return True
        else:
            print(f"Laboratorio {self.nombre} esta disponible")
            return False
        
        
        
        

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
    def __init__(self, idMonitor, nombre, carga_asignada):
        self.idMonitor = idMonitor
        self.nombre = nombre
        self.carga_asignada = carga_asignada
        
        
    def asignar_aspirante(self):
        print(f"Aspirante asignado al monitor {self.nombre}")
        
    def verificar_carga(self):
        print(f"Total de aspirantes asignados del monitor {self.nombre} :  {self.carga_asignada} ")
        
    
    

class Notificacion:
    def __init__(self, idNotificacion, mensaje, fecha_envio, estado):
        self.__idNotificacion = idNotificacion
        self.mensaje = mensaje
        self.fecha_envio = fecha_envio
        self.estado = estado
        
    def enviar(self):
        print("Enviando correo al aspirante: ")
    
    def marcarLeido(self):
        print("Marcando correo como leído ")
        