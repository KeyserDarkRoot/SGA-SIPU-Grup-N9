from abc import ABC, abstractmethod

class MonitorBase(ABC):
    @abstractmethod
    def asignar_aspirante(self):
        pass

    @abstractmethod
    def verificar_carga(self):
        pass


# Clase hija 1
class MonitorPresencial(MonitorBase):
    def __init__(self, nombre):
        self.nombre = nombre
        self.carga_asignada = 0

    def asignar_aspirante(self):
        self.carga_asignada += 1
        print(f"Aspirante asignado presencialmente al monitor {self.nombre}")

    def verificar_carga(self):
        print(f"{self.nombre} tiene {self.carga_asignada} aspirantes asignados en persona.")


# Clase hija 2
class MonitorVirtual(MonitorBase):
    def __init__(self, nombre):
        self.nombre = nombre
        self.carga_asignada = 0

    def asignar_aspirante(self):
        self.carga_asignada += 1
        print(f"Aspirante asignado virtualmente al monitor {self.nombre}")

    def verificar_carga(self):
        print(f"{self.nombre} tiene {self.carga_asignada} aspirantes asignados virtualmente.")


# Ejemplo uso del polimorfismo
if __name__ == "__main__":
    presencial = MonitorPresencial("Carlos")
    virtual = MonitorVirtual("Ana")

    # Lista con diferentes tipos de monitores
    monitores = [presencial, virtual]

    # Polimorfismo: todos usan el mismo método, pero con comportamientos distintos
    for m in monitores:
        m.asignar_aspirante()
        m.verificar_carga()