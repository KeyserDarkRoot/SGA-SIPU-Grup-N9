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