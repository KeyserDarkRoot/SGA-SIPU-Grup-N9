import random

class Evaluacion:
    def __init__(self, id_inscripcion, periodo, modalidad="Virtual"):
        self.id_inscripcion = id_inscripcion
        self.periodo = periodo
        self.modalidad = modalidad
        self.asistio = False
        self.deshonestidad_academica = False
        self.puntaje_obtenido = 0.0
    
    def rendir_examen(self):
        """
        Simula la toma del examen según normativa SNNA.
        Valida ASISTENCIA y DESHONESTIDAD_ACADEMICA.
        """
        print(f"Iniciando evaluación ({self.modalidad})...")
        self.asistio = True
        
        # Simulación de puntaje aleatorio entre 600 y 1000
        puntaje_bruto = random.randint(600, 1000)
        
        # Simulación aleatoria de copia (5% de probabilidad de ser detectado)
        # En la vida real, esto vendría de un reporte del supervisor
        if random.random() < 0.05:
            self.deshonestidad_academica = True
            print("⚠️ ALERTA: Se ha detectado deshonestidad académica.")
        
        if self.deshonestidad_academica:
            self.puntaje_obtenido = 0.0
            print("Resultado: ANULADO por deshonestidad (Nota: 0).")
        else:
            self.puntaje_obtenido = float(puntaje_bruto)
            print(f"Examen finalizado. Puntaje: {self.puntaje_obtenido} / 1000")
            
        return self.puntaje_obtenido

    def generar_acta(self):
        estado = "ANULADO" if self.deshonestidad_academica else "VALIDO"
        return f"Acta {self.id_inscripcion}: {self.puntaje_obtenido} pts ({estado})"