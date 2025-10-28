from ConexionBD.api_supabase import crear_cliente
from periodo import Periodo

class OfertaAcademica:
    def __init__(self, idOferta, universidad, carreras, fechaPublicacion, estadoOferta):
        self.__idOferta = idOferta
        self.universidad = universidad
        self.carreras = carreras
        self.fechaPublicacion = fechaPublicacion
        self.estadoOferta = estadoOferta
        self.client = crear_cliente()

    # Crear una oferta académica solo si hay un periodo activo
    def crear_oferta(self):
        try:
            periodo = Periodo(None, None, None, None)
            periodo_activo = periodo.obtener_periodo_activo()

            if not periodo_activo:
                print(" No se puede crear la oferta: no hay un periodo activo.")
                return

            data = {
                "idoferta": self.__idOferta,
                "universidad": self.universidad,
                "fechapublicacion": self.fechaPublicacion,
                "estadooferta": self.estadoOferta,
                "idperiodo": periodo_activo["idperiodo"]
            }
            self.client.table("ofertaacademica").insert(data).execute()
            print(f"Oferta académica '{self.universidad}' creada para el periodo {periodo_activo['nombreperiodo']}.")
        except Exception as e:
            print("Error al crear la oferta académica:", e)

    # Agregar carreras a la oferta
    def agregarCarrera(self, carrera):
        try:
            data = {
                "idcarrera": carrera._Carrera__idCarrera,
                "nombrecarrera": carrera.nombreCarrera,
                "facultad": carrera.facultad,
                "modalidad": carrera.modalidad,
                "duracion": carrera.duracion,
                "cuposdisponibles": carrera.cuposDisponibles,
                "idoferta": self.__idOferta
            }
            self.client.table("carrera").insert(data).execute()
            print(f"Carrera '{carrera.nombreCarrera}' agregada correctamente a la oferta.")
        except Exception as e:
            print("Error al agregar carrera:", e)


    # Leer carreras vinculadas a esta oferta
    def listarCarrera(self):
        try:
            response = self.client.table("carrera").select("*").eq("idoferta", self.__idOferta).execute()
            if not response.data:
                print(f"No hay carreras registradas para la oferta {self.periodoAcademico}.")
                return
            print(f"Carreras de la oferta {self.periodoAcademico}:")
            for c in response.data:
                print(f"- {c['nombrecarrera']} ({c['modalidad']}) - Duración: {c['duracion']} - Cupos: {c['cuposdisponibles']}")
        except Exception as e:
            print("Error al listar carreras:", e)

    # Actualizar carrera
    def actualizarCarrera(self, idCarrera, nuevos_datos):
        try:
            response = self.client.table("carrera").update(nuevos_datos).eq("idcarrera", idCarrera).execute()
            print(f"Carrera {idCarrera} actualizada correctamente.")
        except Exception as e:
            print("Error al actualizar carrera:", e)

    # Eliminar carrera
    def eliminarCarrera(self, idCarrera):
        try:
            response = self.client.table("carrera").delete().eq("idcarrera", idCarrera).execute()
            print(f"Carrera con ID {idCarrera} eliminada correctamente.")
        except Exception as e:
            print("Error al eliminar carrera:", e)

    def publicarOferta(self):
        print(f"Oferta académica '{self.periodoAcademico}' publicada con éxito.")