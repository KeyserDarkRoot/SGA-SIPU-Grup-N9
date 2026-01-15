import os
import sys
from app.database.ConexionBD.api_supabase import crear_cliente
from app.core.periodo import Periodo
from app.core.oferta_academica import OfertaAcademica
from app.core.carreras_universidad import Carrera
from app.core.aspirante import Aspirante
from app.core.inscripcion import Inscripcion
from app.core.evaluacion import Evaluacion
from app.core.postulacion import Postulacion

# Cliente Global para consultas directas en el Main
supabase = crear_cliente()

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def cargar_periodo_activo():
    """Busca en la BD si existe un periodo activo real."""
    print("🔍 Buscando periodo activo en Supabase...")
    try:
        response = supabase.table("periodo").select("*").eq("estado", "activo").execute()
        if response.data:
            data = response.data[0]
            # Creamos el objeto con los datos QUE VIENEN DE LA BD
            p = Periodo(data['idperiodo'], data['nombreperiodo'], data['fechainicio'], data['fechafin'], data['estado'])
            print(f"✅ Periodo cargado: {p.nombre_periodo}")
            return p
        else:
            print("⚠️ No hay periodo activo en la base de datos.")
            return None
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def buscar_aspirante_en_rn(cedula):
    """
    Busca al aspirante en la tabla 'registronacional'.
    Si existe, crea el objeto Aspirante con esos datos.
    """
    print(f"🔍 Buscando cédula {cedula} en Registro Nacional...")
    try:
        response = supabase.table("registronacional").select("*").eq("identificacion", cedula).execute()
        if response.data:
            datos = response.data[0]
            print("✅ Persona encontrada en Registro Nacional.")
            
            # Mapeamos los campos de la BD a la clase Aspirante
            # Asumimos que la BD tiene columnas: identificacion, nombres, apellidos, correo, nota_grado, etc.
            # Ajusta los nombres de las claves ['campo'] según tus columnas reales en Supabase
            
            aspirante = Aspirante(
                identificacion=datos.get('identificacion'),
                nombres=datos.get('nombres'),
                apellidos=datos.get('apellidos'),
                correo=datos.get('correo', 'sin_correo@email.com'),
                nota_bachillerato=float(datos.get('calificacion', 0)), # O nota_grado
                # Aquí mapeamos las condiciones de vulnerabilidad si existen en tu tabla
                es_pueblo_nacionalidad=datos.get('es_pueblo_nacionalidad', False),
                tiene_discapacidad=datos.get('tiene_discapacidad', False),
                es_vulnerable_econom=datos.get('es_vulnerable_econom', False),
                es_residente_local=datos.get('es_residente_local', False)
            )
            return aspirante
        else:
            print("❌ La cédula no existe en la tabla 'registronacional'.")
            return None
    except Exception as e:
        print(f"❌ Error buscando aspirante: {e}")
        return None

def cargar_carrera_desde_db(nombre_carrera):
    """Busca una carrera por nombre en la BD para obtener sus cupos reales"""
    try:
        response = supabase.table("carrera").select("*").ilike("nombrecarrera", f"%{nombre_carrera}%").execute()
        if response.data:
            d = response.data[0]
            return Carrera(d['idcarrera'], d['nombrecarrera'], d['facultad'], d['modalidad'], d['duracion'], d['cuposdisponibles'])
        else:
            print("⚠️ Carrera no encontrada en BD.")
            return None
    except Exception as e:
        print(f"Error cargando carrera: {e}")
        return None

def mostrar_menu():
    print("\n=== SISTEMA SIPU (CONECTADO A BASE DE DATOS) ===")
    print("1. [ADMIN] Verificar/Crear Periodo y Oferta")
    print("2. [ASPIRANTE] Validar Cédula (Registro Nacional)")
    print("3. [PROCESO] Inscribirse (Guardar en BD)")
    print("4. [PROCESO] Rendir Evaluación")
    print("5. [PROCESO] Ver Puntaje Final")
    print("6. [PROCESO] Postulación y Aceptación (Actualiza Cupos)")
    print("7. Salir")
    print("================================================")

def main():
    periodo_actual = None
    carrera_seleccionada = None
    mi_aspirante = None
    mi_inscripcion = None
    mi_evaluacion = None
    postulacion_actual = None
    puntaje_examen = 0

    while True:
        mostrar_menu()
        opcion = input("Seleccione: ")

        if opcion == "1":
            # Intentamos cargar de la BD primero
            periodo_actual = cargar_periodo_activo()
            
            if not periodo_actual:
                resp = input("¿Desea crear un nuevo periodo en la BD? (S/N): ")
                if resp.upper() == "S":
                    # Crear nuevo
                    periodo_actual = Periodo("2025-1", "Periodo 2025-1", "2025-01-01", "2025-06-30", "activo")
                    periodo_actual.crear_periodo() # Guarda en BD
                    
                    # Crear Oferta y Carrera por defecto para pruebas
                    oferta = OfertaAcademica("OFE-001", "ULEAM", [], "2025-02-01", "activa")
                    oferta.crear_oferta()
                    
                    carrera_seleccionada = Carrera(101, "Software", "Ingeniería", "Presencial", "9 Sem", 50, "OFE-001")
                    oferta.agregarCarrera(carrera_seleccionada) # Guarda en BD
            else:
                # Si ya existe el periodo, cargamos una carrera de prueba de la BD
                carrera_seleccionada = cargar_carrera_desde_db("Software")
                if not carrera_seleccionada:
                     # Si no existe en BD, creamos el objeto localmente para que no falle el flujo
                     carrera_seleccionada = Carrera(101, "Software", "Ingeniería", "Presencial", "9 Sem", 50)

        elif opcion == "2":
            if not periodo_actual:
                print("⚠️ Primero debe cargar el periodo (Opción 1).")
                continue
                
            cedula = input("Ingrese Cédula para validar: ")
            # AQUÍ ES LA MAGIA: Busca en tu tabla real
            mi_aspirante = buscar_aspirante_en_rn(cedula)
            
            if mi_aspirante:
                print(f"👋 Bienvenido/a {mi_aspirante.nombres} {mi_aspirante.apellidos}")
                print(f"📊 Nota Bachillerato registrada: {mi_aspirante.nota_bachillerato}")

        elif opcion == "3":
            if mi_aspirante and periodo_actual:
                # Verificar si ya está inscrito
                chk = supabase.table("inscripciones").select("*").eq("identificacion", mi_aspirante.identificacion).execute()
                if chk.data:
                    print("⚠️ Usted ya tiene una inscripción registrada.")
                    mi_inscripcion = Inscripcion(
                        periodo_id=periodo_actual.id_periodo,
                        ies_id=100,
                        tipo_documento=1,
                        identificacion=mi_aspirante.identificacion,
                        nombres=mi_aspirante.nombres,
                        apellidos=mi_aspirante.apellidos,
                        carrera_seleccionada=carrera_seleccionada.nombreCarrera if carrera_seleccionada else "Software"
                    )
                    mi_inscripcion.id_inscripcion = chk.data[0]['id_inscripcion'] # Recuperamos ID real
                else:
                    # Nueva inscripción
                    mi_inscripcion = Inscripcion(
                        periodo_id=periodo_actual.id_periodo,
                        ies_id=100,
                        tipo_documento=1,
                        identificacion=mi_aspirante.identificacion,
                        nombres=mi_aspirante.nombres,
                        apellidos=mi_aspirante.apellidos,
                        carrera_seleccionada=carrera_seleccionada.nombreCarrera if carrera_seleccionada else "Software"
                    )
                    if mi_inscripcion.validar_periodo(): 
                        mi_inscripcion.guardar_en_supabase() # Guarda en BD real
            else:
                print("❌ Faltan datos del aspirante o periodo.")

        elif opcion == "4":
            if mi_inscripcion:
                mi_evaluacion = Evaluacion(mi_inscripcion.id_inscripcion, periodo_actual)
                puntaje_examen = mi_evaluacion.rendir_examen()
            else:
                print("❌ Debe inscribirse primero.")

        elif opcion == "5":
            if mi_evaluacion and mi_aspirante:
                mi_aspirante.calcular_puntaje_final(puntaje_examen)
            else:
                print("❌ Falta rendir evaluación.")

        elif opcion == "6":
            if mi_aspirante and mi_aspirante.puntaje_final_postulacion > 0:
                if not carrera_seleccionada:
                    print("⚠️ Cargando datos de carrera...")
                    carrera_seleccionada = cargar_carrera_desde_db("Software")

                postulacion_actual = Postulacion("POS-001", mi_aspirante, carrera_seleccionada)
                postulacion_actual.procesar_asignacion(puntaje_corte_referencial=800)
                
                if postulacion_actual.estado == "ASIGNADO":
                    decision = input(">>> ¿ACEPTA EL CUPO? (Se actualizará la BD) (S/N): ")
                    # Esto llamará a asignarCupos() que ahora tiene un UPDATE real a Supabase
                    postulacion_actual.decision_aspirante(decision)
            else:
                print("❌ No cumple requisitos para postular.")

        elif opcion == "7":
            print("Saliendo...")
            break

if __name__ == "__main__":
    main()