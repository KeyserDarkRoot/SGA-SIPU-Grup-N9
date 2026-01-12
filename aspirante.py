import uuid
from ConexionBD.api_supabase import crear_cliente

class Aspirante:
    def __init__(self, identificacion, nombres, apellidos, correo, 
                 nota_bachillerato, 
                 es_pueblo_nacionalidad=False, 
                 tiene_discapacidad=False, 
                 es_vulnerable_econom=False,
                 es_residente_local=False): # <--- NUEVO CAMPO POR REGLAMENTO ULEAM
        
        self.id_aspirante = str(uuid.uuid4())
        self.identificacion = identificacion
        self.nombres = nombres
        self.apellidos = apellidos
        self.correo = correo
        
        # Datos Académicos
        self.nota_bachillerato = float(nota_bachillerato)
        
        # Datos de Acción Afirmativa (Política de Cuotas)
        self.es_pueblo_nacionalidad = es_pueblo_nacionalidad
        self.tiene_discapacidad = tiene_discapacidad
        self.es_vulnerable_econom = es_vulnerable_econom
        self.es_residente_local = es_residente_local # Territorialidad
        
        self.puntaje_final_postulacion = 0.0

    def calcular_puntos_adicionales(self):
        """
        Suma puntos de acción afirmativa según Acuerdo SENESCYT 2024-0055.
        Incluye Puntos por Territorialidad (Reglamento Interno).
        """
        puntos_extra = 0
        
        if self.es_pueblo_nacionalidad: puntos_extra += 15
        if self.tiene_discapacidad: puntos_extra += 10
        if self.es_vulnerable_econom: puntos_extra += 15
        if self.es_residente_local: puntos_extra += 5  # Puntos por ser de la zona (ej. Manabí)
        
        # La norma suele poner un techo máximo a los puntos extra (ej. 45 pts)
        return min(puntos_extra, 45)

    def calcular_puntaje_final(self, nota_evaluacion):
        """
        Fórmula: (Nota Examen * Peso) + (Nota Grado * Peso) + Puntos Extra
        Según Reglamento ULEAM/Senescyt.
        """
        peso_eval = 0.50 # Puede variar según la IES
        peso_bach = 0.50
        
        puntos_accion_afirmativa = self.calcular_puntos_adicionales()
        
        self.puntaje_final_postulacion = (nota_evaluacion * peso_eval) + \
                                         (self.nota_bachillerato * peso_bach) + \
                                         puntos_accion_afirmativa
        
        print(f"\n--- CÁLCULO DE PUNTAJE (Normativa 2025) ---")
        print(f"Aspirante: {self.nombres} {self.apellidos}")
        print(f"1. Mérito Académico (50%): {self.nota_bachillerato * peso_bach}")
        print(f"2. Evaluación (50%): {nota_evaluacion * peso_eval}")
        print(f"3. Acción Afirmativa (Territorialidad/Vuln): +{puntos_accion_afirmativa}")
        print(f"TOTAL POSTULACIÓN: {self.puntaje_final_postulacion}")
        
        return self.puntaje_final_postulacion