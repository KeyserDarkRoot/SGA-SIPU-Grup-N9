from datetime import date
from app.core.base_core import BaseCore
from app.services.examen_service import ExamenService


class AsignacionExamen(BaseCore):

    def __init__(self):
        self._service = ExamenService()

    def ejecutar(self, cedula):
        return self._asignar_examen(cedula)

    # ================= PRIVADOS =================

    def _asignar_examen(self, cedula):

        # 1 Obtener sede del aspirante
        sede = self._service.obtener_sede_aspirante(cedula)

        if not sede:
            raise Exception("Aspirante no inscrito")

        # 2 Obtener carrera prioridad
        carrera = self._service.obtener_carrera_prioridad(cedula)

        if not carrera:
            raise Exception("No tiene carreras")

        # 3 Obtener tipo examen
        tipo = self._service.obtener_tipo_examen(
            carrera["ofa_id"]
        )

        if not tipo:
            raise Exception("Tipo examen no encontrado")

        # 4️ Laboratorios de su sede
        labs = self._service.obtener_laboratorios_sede(sede)

        if not labs:
            raise Exception("No hay laboratorios en su sede")

        # 5️ Horarios activos
        horarios = self._service.obtener_horarios()

        if not horarios:
            raise Exception("No hay horarios configurados")

        # 6️ DISTRIBUCIÓN INTELIGENTE
        for lab in labs:

            for h in horarios:

                usados = self._service.contar_asignados(
                    lab["lab_id"],
                    h["id_horario"]
                )

                if usados < lab["capacidad_equipos"]:

                    data = {
                        "identificacion_aspirante": cedula,
                        "tipo_examen_id": tipo["id_tipo"],
                        "laboratorio_id": lab["lab_id"],
                        "horario_id": h["id_horario"],
                        "fecha_examen": date.today().isoformat()
                    }

                    self._service.guardar_asignacion(data)
                    return data

        # 7️ Si todo lleno
        raise Exception(
         "No existen cupos disponibles"
        )
