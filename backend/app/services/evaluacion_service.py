from datetime import datetime
import uuid
from app.database.ConexionBD.api_supabase import crear_cliente

class EvaluacionService:

    def __init__(self):
        self.db = crear_cliente()

    def registrar_evaluacion(self, data:dict):

        registro = {
            "id_evaluacion": str(uuid.uuid4()),
            "ies_id": None,
            "identificacion": str(data["identificacion"]),
            "modalidad_evaluacion": int(data["modalidad"]),
            "fecha_evaluacion": datetime.now().strftime("%Y-%m-%d"),
            "examen_suficiencia": str(data["examen"]),
            "tipo_evaluacion": str(data["tipo"]),
            "asistencia_evaluacion": int(data["asistio"]),
            "puntaje_evaluacion_actual": float(data["puntaje"]),
            "deshonestidad_academica": int(data["deshonestidad"]),
            "padece_discapacidad": int(data["discapacidad"]),
            "evaluacion_adaptada": str(data["adaptada"])
        }

        self.db.table("evaluacion").insert(registro).execute()
        return registro

