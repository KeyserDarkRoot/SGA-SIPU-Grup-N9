class Monitor:
    def __init__(self, idMonitor, nombre, carga_asignada):
        self.idMonitor = idMonitor
        self.nombre = nombre
        self.carga_asignada = carga_asignada

    def asignar_aspirante(self):
        self.carga_asignada += 1
        print(f"Aspirante asignado al monitor {self.nombre}")

    def verificar_carga(self):
        print(f"Total de aspirantes asignados al monitor {self.nombre}: {self.carga_asignada}")