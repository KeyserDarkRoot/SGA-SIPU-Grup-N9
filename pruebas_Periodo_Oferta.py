from periodo import Periodo
from oferta_academica import OfertaAcademica
from carreras_universidad import Carrera

# Crear y activar un periodo
p1 = Periodo(1, "2025A", "2025-01-01", "2025-06-30")
p1.crear_periodo()
p1.activar_periodo()

# Crear oferta académica dentro del periodo activo
oferta = OfertaAcademica(1, "Universidad Central", [], "2025-01-10", "activa")
oferta.crear_oferta()

# Crear carreras
c1 = Carrera(1, "Ingeniería en Software", "Facultad de Ingeniería", "Presencial", "8 semestres", 50)
c2 = Carrera(2, "Diseño Web", "Facultad de Artes", "Virtual", "6 semestres", 30)

# Agregar carreras a la oferta
oferta.agregarCarrera(c1)
oferta.agregarCarrera(c2)

# Cerrar un periodo
p1 = Periodo(1, "2025A", "2025-01-01", "2025-06-30")
p1.cerrar_periodo()

