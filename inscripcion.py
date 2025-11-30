from datetime import datetime
import uuid
from periodo import Periodo
from ConexionBD.api_supabase import crear_cliente

class Inscripcion:
    def __init__(self, periodo_id, ies_id, tipo_documento, identificacion, nombres, apellidos, carrera_seleccionada, fecha_inscripcion=None, estado="registrado"):
        self.id_inscripcion = str(uuid.uuid4())  # ID único
        self.periodo_id = periodo_id
        self.ies_id = ies_id
        self.tipo_documento = tipo_documento
        self.identificacion = identificacion
        self.nombres = nombres
        self.apellidos = apellidos
        self.carrera_seleccionada = carrera_seleccionada
        self.fecha_inscripcion = fecha_inscripcion or datetime.now().isoformat()
        self.estado = estado
        self.client = crear_cliente()

        
    def validar_periodo(self):
        try:
            # 1) Crear un objeto Periodo "temporal" solo para usar su cliente
            periodo_tmp = Periodo(None, None, None, None)

            # 2) Obtener el periodo activo desde la base de datos
            periodo_activo_data = periodo_tmp.obtener_periodo_activo()


            # 3) Crear un objeto Periodo real con los datos del periodo activo
            periodo_activo = Periodo(
                id_periodo=periodo_activo_data["idperiodo"],
                nombre_periodo=periodo_activo_data["nombreperiodo"],
                fecha_inicio=periodo_activo_data["fechainicio"],
                fecha_fin=periodo_activo_data["fechafin"],
                estado=periodo_activo_data["estado"]
            )

            # 4) Tomar la fecha que vas a validar:
            #    - Usamos la fecha de inscripción (ya viene en isoformat)
            #    - Si por alguna razón no está, usamos la fecha actual
            fecha_a_validar = self.fecha_inscripcion or datetime.now().isoformat()

            # 5) Validar que esa fecha esté dentro del periodo activo
            if periodo_activo.validar_fecha_actual(fecha_a_validar):
                return True
            else:
                return False

        except Exception as e:
            print("Error al validar el periodo:", e)
            return False


    def validar_registro_nacional(self):
        try:
            resultado = self.client.table("registronacional") \
                .select("*") \
                .eq("identificacion", self.identificacion) \
                .execute()

            if resultado.data:
                print("Usted realizó el Registro Nacional.")
                return resultado.data[0]
            else:
                print("Usted no realizó el Registro Nacional.")
                return None
        except Exception as e:
            print("Error al validar registro nacional:", e)
            return None
        


    def guardar_en_supabase(self):
        datos = {
            "periodo_id": self.periodo_id,
            "ies_id": self.ies_id,
            "tipo_documento": self.tipo_documento,
            "identificacion": self.identificacion,
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "fecha_inscripcion": self.fecha_inscripcion,
            "carrera_seleccionada": self.carrera_seleccionada,
            "estado": self.estado
        }

        try:
            self.client.table("inscripciones").insert(datos).execute()
            self.registrarInscripcion()
            self.generar_certificado()
        except Exception as e:
            print(f"Error al guardar inscripción: {e}")

    def registrarInscripcion(self):
        print("Registro exitoso.")

    def generar_certificado(self):
        print(f"Certificado generado para {self.nombres} {self.apellidos} - Identificación: {self.identificacion}")

    def consultarHistorial(self):
        print("Consulta de historial exitosa.")

    def consultarInscripcion(self):
        print(f"Inscripción a {self.carrera_seleccionada} en periodo {self.periodo_id}")

    def __str__(self):
        return f"Inscripción {self.id_inscripcion} - {self.carrera_seleccionada} ({self.estado})"



#FUNCIÓN PARA CONSULTAR PERIODOS DESDE SUPABASE

def obtener_periodos_disponibles(cliente):
    try:
        resultado = cliente.table("periodo").select("nombreperiodo, fechainicio, fechafin, estado").eq("estado", 'activo').execute()
        periodos = resultado.data
        print("\n=== Periodos disponibles ===")
        for i, p in enumerate(periodos, 1):
            print(f"{i}. {p['nombreperiodo']} | {p.get('estado', 'sin estado')} | {p.get('fechainicio', '')} - {p.get('fechafin', '')}")
        return periodos
    except Exception as e:
        print("Error al obtener periodos:", e)
        return None


# BLOQUE PRINCIPAL / MINI MENÚ

def menu_interactivo():
    cliente = crear_cliente()
    # Consultar periodos
    periodos = obtener_periodos_disponibles(cliente)
    if not periodos:
        print("No hay periodos disponibles. No se puede continuar.")
        return

    # Mostrar lista y elegir uno
    while True:
        try:
            opcion = int(input("Seleccione el número del periodo a usar: "))
            if 1 <= opcion <= len(periodos):
                periodo_id = periodos[opcion - 1]["nombreperiodo"]
                break
            else:
                print("Opción inválida. Intente nuevamente.")
        except ValueError:
            print("Debe ingresar un número válido.")
            
    if not Periodo.validar_fecha_en_periodo():
        return
  
    
    print("=== Mini menú de inscripción ===")
    cedula = input("Ingrese la cédula (identificación) a validar: ").strip()

    # Crear un objeto temporal Inscripcion solo para validar registro nacional
    temp_inscripcion = Inscripcion(
        periodo_id="", ies_id="", tipo_documento="", identificacion=cedula,
        nombres="", apellidos="", carrera_seleccionada=""
    )

    registro = temp_inscripcion.validar_registro_nacional()
    if registro:
        # Extraer datos del registro nacional
        nombres = registro.get("nombres") or registro.get("nombre")
        apellidos = registro.get("apellidos") or registro.get("apellido")
        tipo_documento = registro.get("tipo_documento") or "cédula"
        ies_id = input("Ingrese ies_id (ej. 101): ").strip()
        carrera = input("Ingrese la carrera seleccionada: ").strip()

        # Crear inscripción completa
        inscripcion = Inscripcion(
            periodo_id=periodo_id,
            ies_id=ies_id,
            tipo_documento=tipo_documento,
            identificacion=cedula,
            nombres=nombres,
            apellidos=apellidos,
            carrera_seleccionada=carrera
        )

        # Guardar
        inscripcion.guardar_en_supabase()


if __name__ == "__main__":
    menu_interactivo()
