class Laboratorio:
    def __init__(self, id_laboratorio, nombre, capacidad):
        self.id_laboratorio = id_laboratorio
        self.nombre = nombre
        self.capacidad = capacidad
        self.estado = "disponible"

class ServicioReserva:
    def reservar(self, laboratorio):
        # Lógica de validación
        if laboratorio.estado == "disponible":
            laboratorio.estado = "ocupado"
            return True, f"Laboratorio {laboratorio.nombre} reservado con éxito."
        else:
            return False, f"El laboratorio {laboratorio.nombre} no está disponible."
        
        
        