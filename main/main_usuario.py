from app.core.inscripcion import Inscripcion, obtener_periodos_disponibles, obtener_sedes

def menu():
    print("\n===== SISTEMA DE INSCRIPCIÓN U =====")
    print("1. Iniciar inscripción")
    print("2. Salir")

def main():

    while True:
        menu()
        op = input("Seleccione: ")

        if op == "1":

            # 1 INGRESAR CÉDULA
            cedula = input("Ingrese su cédula: ").strip()

            # 2 OBJETO TEMPORAL PARA VALIDAR REGISTRO NACIONAL
            temp = Inscripcion(
                periodo_id="",
                ies_id="",
                tipo_documento="",
                identificacion=cedula,
                nombres="",
                apellidos="",
                carrera_seleccionada="",
                nombre_sede=""
            )

            registro = temp.validar_registro_nacional()

            if not registro:
                print("Debe realizar primero el Registro Nacional.")
                continue

            print("\n✔ Registro nacional encontrado")
            print("Nombre:", registro.get("nombres"))

            # 3 MOSTRAR PERIODOS
            periodos = obtener_periodos_disponibles()
            if not periodos:
                print("No hay periodos disponibles.")
                continue

            while True:
                try:
                    op_p = int(input("Seleccione periodo: "))
                    if 1 <= op_p <= len(periodos):
                        periodo_elegido = periodos[op_p-1]
                        break
                    else:
                        print("Opción inválida.")
                except:
                    print("Ingrese número válido")

            # 4 CREAR INSCRIPCIÓN REAL
            ies = input("ID institución: ")
            carrera = input("Carrera: ")

            

            # MOSTRAR SEDES
            
            sedes = obtener_sedes()

            if not sedes:
                print("No hay sedes registradas.")
                continue

            print("\n=== SEDES DISPONIBLES ===")
            for i,s in enumerate(sedes,1):
                print(f"{i}. {s['nombre_sede']} - {s['direccion']}")

            while True:
                try:
                    op_s = int(input("Seleccione sede: "))
                    if 1 <= op_s <= len(sedes):
                        sede_elegida = sedes[op_s-1]
                        break
                    else:
                        print("Opción inválida")
                except:
                    print("Ingrese número válido")

            ins = Inscripcion(
                periodo_id=periodo_elegido["nombreperiodo"],
                ies_id=ies,
                tipo_documento = registro.get("tipodocumento"),
                identificacion=cedula,
                nombres=registro.get("nombres"),
                apellidos=registro.get("apellidos"),
                carrera_seleccionada=carrera,
                nombre_sede=sede_elegida["nombre_sede"]
            )

            # 5 GUARDAR (AQUÍ SE VALIDA EL PERIODO)
            ins.guardar_en_supabase()

        elif op == "2":
            break

        else:
            print("Opción inválida")

if __name__ == "__main__":
    main()
