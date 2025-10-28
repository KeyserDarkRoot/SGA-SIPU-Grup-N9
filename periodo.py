from datetime import datetime
from ConexionBD.api_supabase import crear_cliente

class Periodo:
    def __init__(self, id_periodo, nombre_periodo, fecha_inicio, fecha_fin, estado="inactivo"):
        self.id_periodo = id_periodo
        self.nombre_periodo = nombre_periodo
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado
        self.client = crear_cliente()

    # Crear un nuevo periodo académico
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
            print(f"Periodo '{self.nombre_periodo}' creado correctamente.")
        except Exception as e:
            print("Error al crear el periodo:", e)

    # Activar un periodo (solo uno puede estar activo a la vez)
    def activar_periodo(self):
        try:
            # Cerrar otros periodos activos
            self.client.table("periodo").update({"estado": "cerrado"}).eq("estado", "activo").execute()
            # Activar este
            self.client.table("periodo").update({"estado": "activo"}).eq("idperiodo", self.id_periodo).execute()
            self.estado = "activo"
            print(f"Periodo {self.nombre_periodo} activado correctamente.")
        except Exception as e:
            print("Error al activar el periodo:", e)

    def cerrar_periodo(self):
        try:
            self.client.table("periodo").update({"estado": "cerrado"}).eq("idperiodo", self.id_periodo).execute()
            self.estado = "cerrado"
            print(f"Periodo {self.nombre_periodo} cerrado.")
        except Exception as e:
            print("Error al cerrar el periodo:", e)

    # Verificar si hay un periodo activo
    def obtener_periodo_activo(self):
        try:
            response = self.client.table("periodo").select("*").eq("estado", "activo").execute()
            if response.data:
                print(f"Periodo activo: {response.data[0]['nombreperiodo']}")
                return response.data[0]
            else:
                print("No hay ningún periodo activo.")
                return None
        except Exception as e:
            print("Error al verificar el periodo activo:", e)
            return None

    # Validar si una fecha está dentro del rango del periodo
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
