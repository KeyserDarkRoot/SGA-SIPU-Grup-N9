class Monitor:
     def _init_(self, idMonitor, nombre, carga_asignada):
        self.idMonitor = idMonitor
        self.nombre = nombre
        self.carga_asignada = carga_asignada
        
        
        def asignar_aspirante(self):
            print(f"Aspirante asignado al monitor {self.nombre}")
        
        def verificar_carga(self):
            print(f"Total de aspirantes asignados del monitor {self.nombre} :  {self.carga_asignada} ")