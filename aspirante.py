from ConexionBD.api_supabase import crear_cliente
import uuid
class Aspirante:
    def __init__(self, id_aspirante, identificacion, nombres, apellidos, correo, celular, fechanacimiento, calificacion):
        self.id_aspirante = id_aspirante
        self.identificacion = identificacion
        self.nombres = nombres
        self.apellidos = apellidos
        self.correo = correo
        self.celular = celular
        self.fecha_nacimiento = fechanacimiento
        self.calificacion = float(calificacion)
        self.puntaje_examen = None
        self.puntaje_postulacion = None

    def registrar(self):
        print(f"Aspirante {self.nombres} {self.apellidos} registrado con cédula {self.identificacion}")

    def actualizar_contacto(self, nuevo_correo, nuevo_celular):
        self.correo = nuevo_correo
        self.celular = nuevo_celular
        print(f"Contacto actualizado: {self.correo}, {self.celular}")

    def calcular_puntaje(self, puntaje_examen, porcentaje_bachillerato, porcentaje_examen):
        self.puntaje_examen = float(puntaje_examen)
        self.puntaje_postulacion = (self.calificacion * porcentaje_bachillerato) + \
                                   (self.puntaje_examen * porcentaje_examen)
        print(f"Puntaje total de {self.nombres}: {self.puntaje_postulacion}")
        return self.puntaje_postulacion

    def generar_comprobante(self):
        print(f"Comprobante generado para {self.nombres} ({self.identificacion})")
        
    @staticmethod
    def cargar_aspirantes_desde_supabase():
        cliente = crear_cliente()
        try:
            respuesta = cliente.table("registronacional").select("*").execute()
            registros = respuesta.data

            aspirantes = []
            for registro in registros:
                aspirante = Aspirante(
                    id_aspirante=str(uuid.uuid4()),
                    identificacion=registro["identificacion"],
                    nombres=registro["nombres"],
                    apellidos=registro["apellidos"],
                    correo=registro["correo"],
                    celular=registro["celular"],
                    fechanacimiento=registro["fechanacimiento"],
                    calificacion=registro["calificacion"]
                )
                print(f"Aspirante creado: {aspirante.nombres} {aspirante.apellidos} ({aspirante.identificacion})")
                aspirantes.append(aspirante)

            return aspirantes

        except Exception as e:
            print("Error al cargar aspirantes:", e)
            return []

#Ejemplo de uso
if __name__ == "__main__":
    aspirantes = Aspirante.cargar_aspirantes_desde_supabase()

for a in aspirantes:
    a.registrar()
    a.calcular_puntaje(puntaje_examen=800, porcentaje_bachillerato=0.4, porcentaje_examen=0.6)
    a.generar_comprobante()