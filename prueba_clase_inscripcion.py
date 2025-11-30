from inscripcion import Inscripcion
from periodo import Periodo
from ConexionBD.api_supabase import crear_cliente

cliente = crear_cliente()

inscripcion = Inscripcion(
    periodo_id="2025A",
    ies_id=101,
    tipo_documento="cédula",
    identificacion="01020304033",
    nombres="Carlos Andrés",
    apellidos="Mendoza Rojas",
    carrera_seleccionada="Ingeniería Civil"
)

if inscripcion.validar_registro_nacional(cliente):
    if inscripcion.validar_periodo():
        inscripcion.guardar_en_supabase(cliente)
    else:
        print("El periodo no está activo o fuera de fecha.")