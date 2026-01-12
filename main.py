import os
from periodo import Periodo
from oferta_academica import OfertaAcademica
from carreras_universidad import Carrera
from aspirante import Aspirante
from inscripcion import Inscripcion
from evaluacion import Evaluacion
from postulacion import Postulacion

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    print("\n=== SISTEMA DE ADMISIÓN SIPU (Normativa 2025) ===")
    print("1. [ADMIN] Iniciar Periodo y Oferta")
    print("2. [ASPIRANTE] Registro y Puntos Acción Afirmativa")
    print("3. [PROCESO] Inscripción")
    print("4. [PROCESO] Evaluación (Examen)")
    print("5. [PROCESO] Ver Puntaje Final")
    print("6. [PROCESO] Postulación y Aceptación")
    print("7. Salir")
    print("=================================================")

def main():
    periodo_actual = None
    oferta_actual = None
    carrera_software = None
    mi_aspirante = None
    mi_inscripcion = None
    mi_evaluacion = None
    postulacion_actual = None
    puntaje_examen = 0

    while True:
        mostrar_menu()
        opcion = input("Seleccione: ")

        if opcion == "1":
            periodo_actual = Periodo("PER-2025", "2025-1", "2025-01-01", "2025-06-30")
            periodo_actual.crear_periodo()
            periodo_actual.activar_periodo()
            oferta_actual = OfertaAcademica("OFE-001", "ULEAM", [], "2025-02-01", "activa")
            oferta_actual.crear_oferta()
            carrera_software = Carrera(101, "Software", "Ingeniería", "Presencial", "9 Sem", 50)
            oferta_actual.agregarCarrera(carrera_software)
            print("Sistema inicializado.")

        elif opcion == "2":
            cedula = input("Ingrese Cédula: ")
            # Pregunta clave ULEAM
            es_local = input("¿Reside en la provincia de la sede? (S/N): ").upper() == "S"

            mi_aspirante = Aspirante(
                identificacion=cedula,
                nombres="Estudiante", apellidos="Prueba", correo="test@email.com",
                nota_bachillerato=900,
                es_pueblo_nacionalidad=True, 
                tiene_discapacidad=False,
                es_vulnerable_econom=False,
                es_residente_local=es_local
            )
            print("Datos cargados.")

        elif opcion == "3":
            if mi_aspirante:
                mi_inscripcion = Inscripcion(periodo_actual.id_periodo, 100, 1, mi_aspirante.identificacion, mi_aspirante.nombres, mi_aspirante.apellidos, "Software")
                if mi_inscripcion.validar_periodo(): mi_inscripcion.guardar_en_supabase()

        elif opcion == "4":
            if mi_inscripcion:
                mi_evaluacion = Evaluacion(mi_inscripcion.id_inscripcion, periodo_actual)
                puntaje_examen = mi_evaluacion.rendir_examen()

        elif opcion == "5":
            if mi_evaluacion:
                mi_aspirante.calcular_puntaje_final(puntaje_examen)

        elif opcion == "6":
            if mi_aspirante and mi_aspirante.puntaje_final_postulacion > 0:
                postulacion_actual = Postulacion("POS-001", mi_aspirante, carrera_software)
                postulacion_actual.procesar_asignacion(puntaje_corte_referencial=800)

                if postulacion_actual.estado == "ASIGNADO":
                    decision = input(">>> ¿ACEPTA EL CUPO? (S/N): ")
                    postulacion_actual.decision_aspirante(decision)
            else:
                print("Falta puntaje.")

        elif opcion == "7":
            break

if __name__ == "__main__":
    main()