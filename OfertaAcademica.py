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

    def listarCarrera(self):
        for carrera in self.carreras:
            print(f"- {carrera.nombreCarrera}")

    def consultarDisponibilidad(self, carrera):
        print("Consultando disponibilidad de la carrera...")

    def publicarOferta(self):
        print("Publicando oferta académica...")