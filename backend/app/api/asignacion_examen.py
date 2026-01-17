from fastapi import APIRouter
from app.core.asignacion_examen import AsignacionMasiva
from app.services.examen_service import ExamenService

router = APIRouter()
service = ExamenService()

@router.post("/ejecutar")
def ejecutar_asignacion(data:dict):

 periodo = data["periodo_id"]

 motor = AsignacionMasiva(service)
 motor.ejecutar(periodo)

 return {
  "ok": True,
  "total": "Asignación masiva completada"
 }
