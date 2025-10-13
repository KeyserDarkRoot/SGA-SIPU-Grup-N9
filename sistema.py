class RegistroNacional:
    pass


class Universidad:
    pass


class Carrera:
    pass


class Periodo:
    pass


class OfertaAcademica:
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
    pass


class Aspirante:
    pass


class Postulacion:
    pass


class Inscripcion:
    pass


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
    pass


class Notificacion:
    pass