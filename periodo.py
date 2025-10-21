from datetime import datetime

class Periodo:
    def __init__(self, id_periodo, nombre_periodo, fecha_inicio, fecha_fin, estado="inactivo"):
        self.id_periodo = id_periodo
        self.nombre_periodo = nombre_periodo
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado

    def activar_periodo(self):
        self.estado = "activo"
        print(f"Periodo {self.nombre_periodo} activado.")

    def cerrar_periodo(self):
        self.estado = "cerrado"
        print(f"Periodo {self.nombre_periodo} cerrado.")

    def validar_fecha_actual(self, fecha_actual_str):
        inicio = datetime.fromisoformat(self.fecha_inicio)
        fin = datetime.fromisoformat(self.fecha_fin)
        fecha_actual = datetime.fromisoformat(fecha_actual_str)
        if inicio <= fecha_actual <= fin:
            print("La fecha está dentro del periodo.")
            return True
        else:
            print("La fecha no corresponde al periodo actual.")
            return False
