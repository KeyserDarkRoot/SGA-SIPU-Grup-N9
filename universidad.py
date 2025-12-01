from abc import ABC, abstractmethod

# Interfaz para permitir extender la funcionalidad SIN modificar Universidad
class IMostrarInformacion(ABC):
    @abstractmethod
    def mostrar(self):
        pass

# Clase Universidad con soporte para OCP
class Universidad:
    def __init__(self, id_universidad, nombre, direccion):
        self.__id_universidad = id_universidad
        self.__nombre = nombre
        self.__direccion = direccion
        self.__sedes = []
        self.__informadores = []   # Necesario para aplicar OCP

    # Getters
    def get_id_universidad(self):
        return self.__id_universidad

    def get_nombre(self):
        return self.__nombre

    def get_direccion(self):
        return self.__direccion

    def get_sedes(self):
        return self.__sedes

    # Setters
    def set_nombre(self, nombre):
        if nombre != "":
            self.__nombre = nombre
        else:
            print("El nombre no puede estar vacío.")

    def set_direccion(self, direccion):
        if direccion != "":
            self.__direccion = direccion
        else:
            print("La dirección no puede estar vacía.")

    # Métodos
    def agregar_sede(self, sede):
        if sede not in self.__sedes:
            self.__sedes.append(sede)
            print("Sede agregada:", sede)
        else:
            print("Esa sede ya existe.")

    def eliminar_sede(self, sede):
        if sede in self.__sedes:
            self.__sedes.remove(sede)
            print("Sede eliminada:", sede)
        else:
            print("No se encontró la sede especificada.")

    # Metodo que permite el OCP
    #Permite extender la información que muestra la universidad sin modificar esta clase#
    def agregar_informador(self, informador: IMostrarInformacion): 
        self.__informadores.append(informador)

    def mostrar_informacion(self):
        print("ID:", self.__id_universidad)
        print("Nombre:", self.__nombre)
        print("Dirección:", self.__direccion)

        print("\n Información para aspirantes")
        for inf in self.__informadores:
            inf.mostrar()


# Clases externas que amplían la funcionalidad (OCP)

class MostrarProcesoInscripcion(IMostrarInformacion):
    def mostrar(self):
        print("Proceso de inscripción:")
        print("- Crear cuenta de aspirante")
        print("- Subir documentos")
        print("- Agendar examen de ingreso")
        print("- Revisión de requisitos")


class MostrarRequisitosGenerales(IMostrarInformacion):
    def mostrar(self):
        print("Requisitos generales:")
        print("- Cédula de identidad")
        print("- Certificado de bachiller")
        print("- Foto tamaño carnet")


class MostrarCalendarioAdmision(IMostrarInformacion):
    def mostrar(self):
        print("Calendario de admisión:")
        print("- Inscripciones: 5 al 20 de abril")
        print("- Examen: 30 de abril")
        print("- Resultados: 10 de mayo")
