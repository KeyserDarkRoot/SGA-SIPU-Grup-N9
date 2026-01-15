from backend.app.core.periodo import Periodo
from backend.app.core.oferta_academica import OfertaAcademica
from backend.app.core.carreras_universidad import Carrera

def menu():
    print("\n===== PANEL ADMINISTRADOR =====")
    print("1. Crear periodo")
    print("2. Activar periodo")
    print("3. Cerrar periodo")
    print("4. Crear oferta académica")
    print("5. Agregar carrera")
    print("6. Listar carreras")
    print("7. Salir")

def main():

    periodo_actual = None
    oferta_actual = None

    while True:
        menu()
        op = input("Seleccione: ")

        # 1 CREAR PERIODO
        if op == "1":
            idp = input("ID periodo: ")
            nom = input("Nombre periodo: ")
            fi = input("Fecha inicio (YYYY-MM-DD): ")
            ff = input("Fecha fin (YYYY-MM-DD): ")

            periodo_actual = Periodo(idp, nom, fi, ff)
            periodo_actual.crear_periodo()

        # 2 ACTIVAR
        elif op == "2":
            if periodo_actual:
                periodo_actual.activar_periodo()
            else:
                print("Primero cree un periodo.")

        # 3 CERRAR
        elif op == "3":
            if periodo_actual:
                periodo_actual.cerrar_periodo()
            else:
                print("No hay periodo cargado.")

        # 4 CREAR OFERTA
        elif op == "4":
            idof = input("ID oferta: ")
            uni = input("Universidad: ")
            fecha = input("Fecha publicación: ")

            oferta_actual = OfertaAcademica(
                idof, uni, [], fecha, "activa"
            )
            oferta_actual.crear_oferta()

        # 5 AGREGAR CARRERA
        elif op == "5":

            if not oferta_actual:
                print("Primero cree una oferta.")
                continue

            idc = int(input("ID carrera: "))
            nom = input("Nombre carrera: ")
            fac = input("Facultad: ")
            mod = input("Modalidad: ")
            dur = input("Duración: ")
            cup = int(input("Cupos: "))

            carrera = Carrera(idc, nom, fac, mod, dur, cup)
            oferta_actual.agregarCarrera(carrera)

        # 6 LISTAR
        elif op == "6":
            if oferta_actual:
                oferta_actual.listarCarrera()
            else:
                print("No existe oferta.")

        elif op == "7":
            break

        else:
            print("Opción inválida")

if __name__ == "__main__":
    main()
