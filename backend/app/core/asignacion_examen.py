from datetime import date
from app.core.base_core import BaseCore
from app.services.examen_service import ExamenService
from datetime import timedelta
import math

class AsignacionExamen(BaseCore):

    def __init__(self):
        self._service = ExamenService()

    def ejecutar(self, cedula):
        return self._asignar_examen(cedula)

    # ================= PRIVADOS =================

    def _asignar_examen(self, cedula):

        # PROTECCIÓN
        if self._service.ya_tiene_asignacion(cedula):
            raise Exception(
            "Este aspirante ya tiene examen asignado"
            )

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

class GeneradorFechas:

    def generar(self, fecha_inicio, dias):
        fechas=[]
        f = fecha_inicio

        for _ in range(dias):
            fechas.append(f)
            f += timedelta(days=1)

        return fechas


class CalculadorCapacidad:

    def calcular_diaria(self, labs, horarios):
        total=0
        for lab in labs:
            total += lab["capacidad_equipos"]

        return total * len(horarios)



class CalculadorDias:

    def calcular(self, total_asp, capacidad_diaria):
        return math.ceil(
         total_asp / capacidad_diaria
        )


class AsignacionMasiva:

    def __init__(self, service):
        self.srv = service
        self.gen = GeneradorFechas()
        self.cap = CalculadorCapacidad()
        self.dias = CalculadorDias()

    def ejecutar(self, periodo):

        aspirantes = self.srv.listar_aspirantes(periodo)

        labs = self.srv.labs_periodo(periodo)
        horarios = self.srv.horarios()

        capacidad = self.cap.calcular_diaria(
            labs, horarios)

        dias = self.dias.calcular(
            len(aspirantes), capacidad)

        fecha_inicio = self.srv.fecha_config(periodo)

        fechas = self.gen.generar(
            fecha_inicio, dias)

        self.distribuir(
          aspirantes, labs, horarios, fechas)

    def distribuir(self, asp, labs, horarios, fechas):

        i=0
        for a in asp:
            f = fechas[i//len(horarios)]
            h = horarios[i%len(horarios)]
            l = labs[i%len(labs)]

            self.srv.guardar_asignacion({
                "identificacion_aspirante": a["cedula"],
                "laboratorio_id": l["lab_id"],
                "fecha_examen": f,
                "horario_id": h["id_horario"]
                })
            i+=1
