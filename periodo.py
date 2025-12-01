from datetime import datetime
from abc import ABC, abstractmethod
from ConexionBD.api_supabase import crear_cliente



# Interface / ABCSS

class TienePeriodo(ABC):
    """
    Interface sencilla para entidades que trabajan con un periodo.

    """

    @property
    @abstractmethod
    def periodo_id(self):
        """Identificador del periodo que usa la entidad."""
        pass

    @abstractmethod
    def validar_periodo(self):
        """Valida que la entidad se esté usando en un periodo correcto."""
        pass

class Periodo:
    def __init__(self, id_periodo, nombre_periodo, fecha_inicio, fecha_fin, estado="inactivo"):
        # Usamos _ para mostrar encapsulamiento con @property
        self._id_periodo = id_periodo
        self._nombre_periodo = nombre_periodo
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self._estado = estado
        self.client = crear_cliente()

    #Properties (encapsulamiento)

    @property
    def id_periodo(self):
        return self._id_periodo

    @id_periodo.setter
    def id_periodo(self, valor):
        if not valor:
            raise ValueError("El id_periodo no puede estar vacío")
        self._id_periodo = valor

    @property
    def nombre_periodo(self):
        return self._nombre_periodo

    @nombre_periodo.setter
    def nombre_periodo(self, valor):
        if not valor:
            raise ValueError("El nombre del periodo no puede estar vacío")
        self._nombre_periodo = valor

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, valor):
        if valor not in ("activo", "inactivo", "cerrado"):
            raise ValueError("Estado de periodo no válido")
        self._estado = valor

    # Metodos de instancia

    def crear_periodo(self):
        try:
            data = {
                "idperiodo": self.id_periodo,
                "nombreperiodo": self.nombre_periodo,
                "fechainicio": self.fecha_inicio,
                "fechafin": self.fecha_fin,
                "estado": self.estado
            }
            self.client.table("periodo").insert(data).execute()
            print("Periodo creado correctamente.")
        except Exception as e:
            print("Error al crear el periodo:", e)

    def activar_periodo(self):
        try:
            # cerrar otros periodos activos
            self.client.table("periodo").update({"estado": "cerrado"}).eq("estado", "activo").execute()
            # activar este
            self.client.table("periodo").update({"estado": "activo"}).eq("idperiodo", self.id_periodo).execute()
            self.estado = "activo"
            print("Periodo activado correctamente.")
        except Exception as e:
            print("Error al activar el periodo:", e)

    def cerrar_periodo(self):
        try:
            self.client.table("periodo").update({"estado": "cerrado"}).eq("idperiodo", self.id_periodo).execute()
            self.estado = "cerrado"
            print("Periodo cerrado.")
        except Exception as e:
            print("Error al cerrar el periodo:", e)

    def validar_fecha_actual(self, fecha_actual_str):
        """
        Método de INSTANCIA: usa los datos del objeto (self).
        """
        inicio = datetime.fromisoformat(self.fecha_inicio)
        fin = datetime.fromisoformat(self.fecha_fin)
        fecha_actual = datetime.fromisoformat(fecha_actual_str)

        if inicio <= fecha_actual <= fin:
            print("La fecha está dentro del periodo.")
            return True
        else:
            print("La fecha no corresponde al periodo.")
            return False

    # Metodo de clase

    @classmethod
    def obtener_periodo_activo(cls):
        """
        Ejemplo de MÉTODO DE CLASE:
        - No usamos self, usamos cls.
        - No necesitamos hacer Periodo() antes de llamarlo.

        Devuelve un diccionario con los datos del periodo activo o None.
        """
        client = crear_cliente()
        try:
            response = client.table("periodo").select("*").eq("estado", "activo").execute()
            if response.data:
                print("Periodo activo:", response.data[0]["nombreperiodo"])
                return response.data[0]
            else:
                print("No hay ningún periodo activo.")
                return None
        except Exception as e:
            print("Error al verificar el periodo activo:", e)
            return None

    # Metodo estatico

    @staticmethod
    def validar_fecha_en_periodo(fecha_a_validar=None):
        """
        Ejemplo de MÉTODO ESTÁTICO:
        - No recibe self ni cls.
        - Solo usa la BD y la fecha como parámetro.

        Si no se pasa fecha, se usa la fecha actual.
        """
        client = crear_cliente()
        try:
            response = client.table("periodo").select("*").eq("estado", "activo").execute()
            if not response.data:
                print("No hay ningún periodo activo.")
                return False

            datos = response.data[0]
            inicio = datetime.fromisoformat(datos["fechainicio"])
            fin = datetime.fromisoformat(datos["fechafin"])

            if fecha_a_validar is None:
                fecha_a_validar = datetime.now().isoformat()

            fecha = datetime.fromisoformat(fecha_a_validar)

            if inicio <= fecha <= fin:
                print("La fecha está dentro del periodo activo.")
                return True
            else:
                print("La fecha NO corresponde al periodo activo.")
                return False
        except Exception as e:
            print("Error al validar el periodo:", e)
            return False


# Función de polimorfismo con la interface

def validar_entidad_con_periodo(entidad):
    """
    Ejemplo de POLIMORFISMO con la interface TienePeriodo.

    Podemos llamar a entidad.validar_periodo() y entidad.periodo_id
    sin importar si es una Inscripcion, una OfertaAcademica, etc.
    """
    if entidad.validar_periodo():
        print("Entidad válida para el periodo:", entidad.periodo_id)
    else:
        print("Entidad fuera de periodo.")
