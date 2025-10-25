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