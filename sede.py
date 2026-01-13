from typing import List

class Sede:
    def __init__(self, sede_id: str, nombre_sede: str, direccion: str, capacidad_total: int, ies_id: int = None):
        self.sede_id = sede_id
        self.nombre_sede = nombre_sede
        self.direccion = direccion
        self.capacidad_total = capacidad_total
        self.ies_id = ies_id
    
    # Verificar disponibilidad de la sede usando GestionLaboratorio
    def verificar_disponibilidad(self, gestion_lab) -> dict:
        """Verifica la disponibilidad de espacios en la sede"""
        # Filtrar laboratorios manualmente ya que tu GestionLaboratorio no tiene obtener_laboratorios_por_sede
        laboratorios = [lab for lab in gestion_lab.laboratorios if hasattr(lab, 'sede_id') and lab.sede_id == self.sede_id]
        
        total_equipos = sum(lab.capacidad for lab in laboratorios)
        labs_disponibles = len([lab for lab in laboratorios if lab.estado == 'disponible'])
        
        info = {
            'capacidad_total': self.capacidad_total,
            'total_laboratorios': len(laboratorios),
            'laboratorios_disponibles': labs_disponibles,
            'total_equipos': total_equipos,
            'disponible': labs_disponibles > 0
        }
        
        print(f"=== Disponibilidad de {self.nombre_sede} ===")
        print(f"Capacidad total: {info['capacidad_total']}")
        print(f"Laboratorios totales: {info['total_laboratorios']}")
        print(f"Laboratorios disponibles: {info['laboratorios_disponibles']}")
        print(f"Total de equipos: {info['total_equipos']}")
        print(f"Estado: {'Disponible' if info['disponible'] else 'No disponible'}")
        
        return info
    
    # Listar laboratorios por estado
    def listar_laboratorios_por_estado(self, gestion_lab, estado: str = 'disponible') -> List:
        """Lista laboratorios filtrados por estado"""
        laboratorios = [lab for lab in gestion_lab.laboratorios if hasattr(lab, 'sede_id') and lab.sede_id == self.sede_id]
        labs_filtrados = [lab for lab in laboratorios if lab.estado == estado]
        
        print(f"\n=== Laboratorios en estado: {estado} ===")
        for lab in labs_filtrados:
            piso = lab.piso if hasattr(lab, 'piso') else 'N/A'
            print(f"- {lab.nombre} | Piso: {piso} | Capacidad: {lab.capacidad}")
        
        return labs_filtrados
    
    # Listar laboratorios por piso
    def listar_laboratorios_por_piso(self, gestion_lab, piso: int) -> List:
        """Lista laboratorios de un piso específico"""
        laboratorios = [lab for lab in gestion_lab.laboratorios if hasattr(lab, 'sede_id') and lab.sede_id == self.sede_id]
        labs_filtrados = [lab for lab in laboratorios if hasattr(lab, 'piso') and lab.piso == piso]
        
        print(f"\n=== Laboratorios en piso {piso} ===")
        for lab in labs_filtrados:
            print(f"- {lab.nombre} | Estado: {lab.estado} | Capacidad: {lab.capacidad}")
        
        return labs_filtrados
    
    # Calcular capacidad disponible
    def calcular_capacidad_disponible(self, gestion_lab) -> int:
        """Calcula la capacidad total de equipos disponibles en laboratorios disponibles"""
        laboratorios = [lab for lab in gestion_lab.laboratorios if hasattr(lab, 'sede_id') and lab.sede_id == self.sede_id]
        capacidad = sum(lab.capacidad for lab in laboratorios if lab.estado == 'disponible')
        print(f"Capacidad disponible en {self.nombre_sede}: {capacidad} equipos")
        return capacidad
    
    # Mostrar información completa
    def mostrar_informacion_completa(self, gestion_lab):
        """Muestra toda la información de la sede y sus laboratorios"""
        laboratorios = [lab for lab in gestion_lab.laboratorios if hasattr(lab, 'sede_id') and lab.sede_id == self.sede_id]
        
        print(f"\n{'='*60}")
        print(f"SEDE: {self.nombre_sede}")
        print(f"{'='*60}")
        print(f"ID: {self.sede_id}")
        print(f"Dirección: {self.direccion}")
        print(f"Capacidad total: {self.capacidad_total}")
        
        print(f"\nLaboratorios ({len(laboratorios)}):")
        
        if laboratorios:
            for lab in laboratorios:
                piso = lab.piso if hasattr(lab, 'piso') else 'N/A'
                print(f"\n  📍 {lab.nombre}")
                print(f"     - Piso: {piso}")
                print(f"     - Capacidad: {lab.capacidad} equipos")
                print(f"     - Estado: {lab.estado}")
        else:
            print("  No hay laboratorios registrados")
        
        print(f"{'='*60}\n")
    
    # Obtener laboratorio con mayor capacidad
    def obtener_laboratorio_mayor_capacidad(self, gestion_lab):
        """Encuentra el laboratorio con mayor capacidad de equipos"""
        laboratorios = [lab for lab in gestion_lab.laboratorios if hasattr(lab, 'sede_id') and lab.sede_id == self.sede_id]
        
        if not laboratorios:
            print("No hay laboratorios disponibles")
            return None
        
        lab_mayor = max(laboratorios, key=lambda x: x.capacidad)
        print(f"Laboratorio con mayor capacidad: {lab_mayor.nombre} ({lab_mayor.capacidad} equipos)")
        return lab_mayor 
 