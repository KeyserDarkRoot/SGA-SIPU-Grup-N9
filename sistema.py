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
    def __init__(self,id_sede, nombre_sede, direccion, capacidad,laboratorio):
        self.id_sede = id_sede
        self.nombre_sede = nombre_sede
        self.direccion = direccion
        self.capacidad = capacidad
        self.laboratorio = []

    def verificar_disponibilidad(self):
        print("Verificando si hay espacio en la sede...")

    def asignar_laboratorio(self,laboratorio):
        print("Asignando laboratorios...")

    def listar_jornadas(self):
        print("Listando jornadas para el uso de los laboratorios...")
    


class Laboratorio:
        def _init_(self, idLaboratorio, nombre, capacidad, estado):
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

class Inscripcion:
    def __init__(self, id_inscripcion,fecha_inscripcion,periodo,carrera_seleccionada,estado):
        self.id_inscripcion = id_inscripcion
        self.fecha = fecha_inscripcion
        self.periodo = periodo
        self.carrera_seleccionada = carrera_seleccionada
        self.estado = estado

    def registrarInscripcion(self):
        print("Registro exitoso.")

    def validarPeriodo(self,):
        print("validacion de periodo")

    def consultarHistorial(self,):
        print("Consulta exitosa.")

    def generarCertificados(self):
        print("Generando certificados de inscripcion....")

    def consultarInscripcion(sel):
        print("consulta exitosa")

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


class Puntaje:
    def __init__(self,puntaje_examen,puntaje_bachillerato,puntaje_accion_afirmativa,total):
        self.puntaje_examen = puntaje_examen
        self.puntaje_bachillerato = puntaje_bachillerato
        self.puntaje_accion_afirmativa = puntaje_accion_afirmativa
        self.total = total

    def Calcular_total(self):
        print("Calculando puntaje total...")

    def aplicar_accion_afirmativa(self):
        print("Aplicando accion afirmativa...")

class Monitor:
     def _init_(self, idMonitor, nombre, carga_asignada):
        self.idMonitor = idMonitor
        self.nombre = nombre
        self.carga_asignada = carga_asignada
        
        
        def asignar_aspirante(self):
            print(f"Aspirante asignado al monitor {self.nombre}")
        
        def verificar_carga(self):
            print(f"Total de aspirantes asignados del monitor {self.nombre} :  {self.carga_asignada} ")
    
class Notificacion:
     def _init_(self, idNotificacion, mensaje, fecha_envio, estado):
        self.__idNotificacion = idNotificacion
        self.mensaje = mensaje
        self.fecha_envio = fecha_envio
        self.estado = estado
        
        def enviar(self):
            print("Enviando correo al aspirante: ")
            def marcarLeido(self):
                print("Marcando correo como leído ")
                