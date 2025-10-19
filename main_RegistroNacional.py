import os
import pandas as pd
from datetime import datetime
from ConexionBD.api_supabase import crear_cliente

class RegistroNacional:
    def __init__(self):
        self.client = crear_cliente()
        if self.client:
            print("Conexión a Supabase establecida correctamente.")
        else:
            print("No se pudo conectar a Supabase.")

    def mostrar_datos(self):
        if not self.client:
            print("No hay cliente Supabase disponible.")
            return

        try:
            resultado = self.client.table("registronacional").select("*").execute()
            if resultado.data:
                for fila in resultado.data:
                    print(fila)
            else:
                print("No hay registros en la tabla registronacional.")
        except Exception as e:
            print("Error al obtener registros:", e)



    def consultar_registro(self):
        
        #Consulta un registro por número de identificación.
        
        if not self.client:
            print("No hay cliente Supabase disponible.")
            return

        identificacion = input("Ingrese el número de identificación: ").strip()

        try:
            resultado = (
                self.client.table("registronacional").select("*").eq("identificacion", identificacion).execute()
            )

            if resultado.data:
                print("\nRegistro encontrado:")
                for campo, valor in resultado.data[0].items():
                    print(f"{campo}: {valor}")
            else:
                print("No se encontró ningún registro con esa identificación.")
        except Exception as e:
            print("Error al consultar el registro:", e)



    def exportar_excel(self, nombre_archivo="registronacional.xlsx"):
        
        # Exporta todos los registros a un archivo Excel dentro de la carpeta Datos_RegistroNacional.
        
        if not self.client:
            print("No hay cliente Supabase disponible.")
            return

        try:
            resultado = self.client.table("registronacional").select("*").execute()
            if not resultado.data:
                print("No hay registros para exportar.")
                return

            # Crear carpeta si no existe
            carpeta = "Datos_RegistroNacional"
            os.makedirs(carpeta, exist_ok=True)

            #Crea el nombre del archivo con fecha de la creacion, osea la actual
            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            nombre_archivo = f"registros_{fecha_actual}.xlsx"


            # Ruta completa del archivo
            ruta_archivo = os.path.join(carpeta, nombre_archivo)

            # Exportar a Excel
            df = pd.DataFrame(resultado.data)
            df.to_excel(ruta_archivo, index=False)

            print(f"Datos exportados correctamente a: {ruta_archivo}")

        except Exception as e:
            print("Error al exportar a Excel:", e)


    def menu(self):

        # Menú interactivo para ejecutar las funciones de RegistroNacional.
  
        while True:
            print("\n===== MENÚ REGISTRO NACIONAL =====")
            print("1. Consultar un registro")
            print("2. Exportar todos los registros a Excel")
            print("3. Salir")
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self.consultar_registro()
            elif opcion == "2":
                self.exportar_excel()
            elif opcion == "3":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción no válida. Intente nuevamente.")


#Solo usar si se desea consultar o extraer los datos de la base de datos a un archivo exel!! (Quitar las comillas)

if __name__ == "__main__":
    rn = RegistroNacional()
    rn.menu()

