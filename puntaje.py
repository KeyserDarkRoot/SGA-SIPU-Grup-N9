class Puntaje:
    def __init__(self,puntaje_examen,puntaje_bachillerato,puntaje_accion_afirmativa,total):
        self.puntaje_examen = puntaje_examen
        self.puntaje_bachillerato = puntaje_bachillerato
        self.puntaje_accion_afirmativa = puntaje_accion_afirmativa
        self.total = total

    def Calcular_total(self):
        print("Calculando puntaje total...")

    def aplicar_accion_afirmativa(self):
        print("Aplicando accion afirmativa...")