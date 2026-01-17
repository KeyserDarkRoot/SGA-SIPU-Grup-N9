from app.core.base_core import BaseCore
from app.services.admin_service import AdminService
from app.core.asignacion_examen import AsignacionExamen

class AsignacionMasiva(BaseCore):

    def __init__(self):
        self.service = AdminService()
        self.asignador = AsignacionExamen()

    def ejecutar(self, idperiodo):

        aspirantes = self.service.obtener_inscritos_periodo(
            idperiodo
        )

        if not aspirantes:
            raise Exception("No hay inscritos")

        total = 0

        for a in aspirantes:
            self.asignador.ejecutar(
                a["identificacion"]
            )
            total += 1

        return {
            "msg":"Asignación masiva completada",
            "total": total
        }
