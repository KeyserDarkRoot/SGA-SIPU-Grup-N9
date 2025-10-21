class Aspirante:
    def __init__(self, id_aspirante, cedula, nombres, apellidos, correo, telefono, fecha_nacimiento, nota_bachillerato):
        self.id_aspirante = id_aspirante
        self.cedula = cedula
        self.nombres = nombres
        self.apellidos = apellidos
        self.correo = correo
        self.telefono = telefono
        self.fecha_nacimiento = fecha_nacimiento
        self.nota_bachillerato = float(nota_bachillerato)
        self.puntaje_examen = 0.0
        self.puntaje_postulacion = 0.0

    def registrar(self):
        print(f"Aspirante {self.nombres} {self.apellidos} registrado con cédula {self.cedula}")

    def actualizar_contacto(self, nuevo_correo, nuevo_telefono):
        self.correo = nuevo_correo
        self.telefono = nuevo_telefono
        print(f"Contacto actualizado: {self.correo}, {self.telefono}")

    def calcular_puntaje(self, puntaje_examen):
        self.puntaje_examen = float(puntaje_examen)
        self.puntaje_postulacion = (self.nota_bachillerato * 0.4) + (self.puntaje_examen * 0.6)
        print(f"Puntaje total de {self.nombres}: {self.puntaje_postulacion}")
        return self.puntaje_postulacion

    def generar_comprobante(self):
        print(f"Comprobante generado para {self.nombres} ({self.cedula})")
