from abc import ABC, abstractmethod
from app.database.ConexionBD.api_supabase import crear_cliente
from app.core.periodo import Periodo


# Interfaces pequeñas (ISP)

class InterfazOfertaPublicable(ABC):
    """
    Interface pequeña enfocada en operaciones de la oferta en sí.
    Un usuario admin que solo necesite crear/publicar una oferta
    depende únicamente de esta interfaz.
    """

    @abstractmethod
    def crear_oferta(self):
        pass

    @abstractmethod
    def publicarOferta(self):
        pass


class InterfazOfertaGestionCarreras(ABC):
    """
    Interface separada para la gestión de carreras dentro de la oferta.
    Un usuario admin que solo quiera administrar carreras no necesita
    conocer cómo se crea o publica la oferta.
    """

    @abstractmethod
    def agregarCarrera(self, carrera):
        pass

    @abstractmethod
    def listarCarrera(self):
        pass

    @abstractmethod
    def actualizarCarrera(self, idCarrera, nuevos_datos):
        pass

    @abstractmethod
    def eliminarCarrera(self, idCarrera):
        pass
    

# Implementación concreta que une ambas interfaces

class OfertaAcademica(InterfazOfertaPublicable, InterfazOfertaGestionCarreras):
    """
    Clase concreta que implementa DOS interfaces:
    - IOfertaPublicable
    - IOfertaGestionCarreras

    """

    def __init__(self, idOferta, universidad, carreras, fechaPublicacion, estadoOferta):
        self.__idOferta = idOferta         # atributo privado (encapsulamiento)
        self.universidad = universidad
        self.carreras = carreras or []     # por si viene None
        self.fechaPublicacion = fechaPublicacion
        self.estadoOferta = estadoOferta
        self.client = crear_cliente()

    # property simple para el id (encapsulamiento leve)
    @property
    def idOferta(self):
        return self.__idOferta

    @idOferta.setter
    def idOferta(self, valor):
        if not valor:
            raise ValueError("El id de la oferta no puede estar vacío")
        self.__idOferta = valor


    # Implementación de IOfertaPublicable

    def crear_oferta(self):
        """Crea una oferta académica solo si hay un periodo activo."""
        try:
            # usamos Periodo solo para consultar el periodo activo
            periodo_tmp = Periodo(None, None, None, None)
            periodo_activo = periodo_tmp.obtener_periodo_activo()

            if not periodo_activo:
                print("No se puede crear la oferta: no hay un periodo activo.")
                return

            data = {
                "idoferta": self.__idOferta,
                "universidad": self.universidad,
                "fechapublicacion": self.fechaPublicacion,
                "estadooferta": self.estadoOferta,
                "idperiodo": periodo_activo["idperiodo"],
            }

            self.client.table("ofertaacademica").insert(data).execute()
            print(
                f"Oferta académica '{self.universidad}' creada para el periodo "
                f"{periodo_activo['nombreperiodo']}."
            )
        except Exception as e:
            print("Error al crear la oferta académica:", e)

    def publicarOferta(self):
        """Solo muestra un mensaje, pero podría notificar a otros sistemas."""
        print(f"Oferta académica '{self.__idOferta}' publicada con éxito.")


    # Implementación de IOfertaGestionCarreras

    def agregarCarrera(self, carrera):
        try:
            data = {
                "idcarrera": carrera._Carrera__idCarrera,
                "nombrecarrera": carrera.nombreCarrera,
                "facultad": carrera.facultad,
                "modalidad": carrera.modalidad,
                "duracion": carrera.duracion,
                "cuposdisponibles": carrera.cuposDisponibles,
                "idoferta": self.__idOferta,
            }
            self.client.table("carrera").insert(data).execute()
            print(f"Carrera '{carrera.nombreCarrera}' agregada correctamente a la oferta.")
        except Exception as e:
            print("Error al agregar carrera:", e)

    def listarCarrera(self):
        try:
            response = self.client.table("carrera").select("*").eq("idoferta", self.__idOferta).execute()
            if not response.data:
                print(f"No hay carreras registradas para la oferta {self.__idOferta}.")
                return
            print(f"Carreras de la oferta {self.__idOferta}:")
            for c in response.data:
                print(
                    f"- {c['nombrecarrera']} ({c['modalidad']}) - "
                    f"Duración: {c['duracion']} - Cupos: {c['cuposdisponibles']}"
                )
        except Exception as e:
            print("Error al listar carreras:", e)

    def actualizarCarrera(self, idCarrera, nuevos_datos):
        try:
            self.client.table("carrera").update(nuevos_datos).eq("idcarrera", idCarrera).execute()
            print(f"Carrera {idCarrera} actualizada correctamente.")
        except Exception as e:
            print("Error al actualizar carrera:", e)

    def eliminarCarrera(self, idCarrera):
        try:
            self.client.table("carrera").delete().eq("idcarrera", idCarrera).execute()
            print(f"Carrera con ID {idCarrera} eliminada correctamente.")
        except Exception as e:
            print("Error al eliminar carrera:", e)


# Ejemplos de uso que muestran el ISP en acción

def registrar_y_publicar_oferta(oferta):
    """
    Esta función solo necesita un objeto que cumpla la interfaz IOfertaPublicable.
    No le importa cómo se gestionan las carreras.
    """
    oferta.crear_oferta()
    oferta.publicarOferta()


def administrar_carreras(gestor, carrera):
    """
    Esta función solo necesita un objeto que cumpla la interfaz IOfertaGestionCarreras.
    No depende de crear_oferta() ni de publicarOferta().
    """
    gestor.agregarCarrera(carrera)
    gestor.listarCarrera()
