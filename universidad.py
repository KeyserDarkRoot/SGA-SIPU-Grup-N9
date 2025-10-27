class Universidad:
    def __init__(self, id_universidad, nombre, direccion,):
        self.__id_universidad = id_universidad
        self.__nombre = nombre
        self.__direccion = direccion
        self.__sedes = []

    # Uso de Get
    def get_id_universidad(self):
        return self.__id_universidad

    def get_nombre(self):
        return self.__nombre

    def get_direccion(self):
        return self.__direccion

    def get_sedes(self):
        return self.__sedes

    # Uso de set
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

    def cargar_oferta(self):
        print("Cargando oferta académica de", self.__nombre)

    def mostrar_informacion(self):
        print("ID:", self.__id_universidad)
        print("Nombre:", self.__nombre)
        print("Dirección:", self.__direccion)
        if len(self.__sedes) > 0:
            print("Sedes:")
            for s in self.__sedes:
                print("-", s)
        else:
            print("No hay sedes registradas.")