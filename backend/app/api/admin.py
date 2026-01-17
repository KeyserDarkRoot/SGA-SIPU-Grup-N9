from fastapi import APIRouter, HTTPException
from app.database.ConexionBD.api_supabase import crear_cliente
from app.core.periodo import Periodo
from app.core.oferta_academica import OfertaAcademica

router_admin = APIRouter()
db = crear_cliente()

# --- GESTIÓN DE PERIODOS ---
@router_admin.post("/periodo")
def crear_periodo(d: dict):
    try:
        # [POO] Instanciación de la clase Periodo
        p = Periodo(d.get("id"), d["nombre"], d["inicio"], d["fin"])
        p.crear_periodo()
        return {"ok": True, "msg": "Periodo creado"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- ENDPOINT NUEVO: DATOS AUXILIARES (Para los Combos) ---
@router_admin.get("/datos_auxiliares")
def datos_auxiliares():
    """Devuelve las Sedes y Periodos para llenar las listas desplegables"""
    try:
        sedes = db.table("sede").select("sede_id, nombre_sede").execute().data
        periodos = db.table("periodo").select("idperiodo, nombreperiodo").execute().data
        return {"sedes": sedes, "periodos": periodos}
    except Exception as e:
        return {"sedes": [], "periodos": []}

# --- ENDPOINT NUEVO: CREAR OFERTA COMPLETA (10 CAMPOS) ---
@router_admin.post("/oferta")
def crear_oferta(d: dict):
    try:
        # Validación de campos obligatorios
        campos_req = ["ofa_id", "nombre_carrera", "periodo_id", "cupos_disponibles", 
                      "sede_id", "estado_oferta", "fecha_publicacion", 
                      "BloqueConocimiento", "modalidad", "jornada"]
        
        faltantes = [c for c in campos_req if c not in d]
        if faltantes:
            raise HTTPException(status_code=400, detail=f"Faltan datos: {', '.join(faltantes)}")

        # [POO] Creación del Objeto OfertaAcademica con los 10 atributos
        o = OfertaAcademica(
            ofa_id=int(d["ofa_id"]),
            nombre_carrera=d["nombre_carrera"],
            periodo_id=int(d["periodo_id"]),
            cupos_disponibles=int(d["cupos_disponibles"]),
            sede_id=d["sede_id"],
            estado_oferta=d["estado_oferta"],
            fecha_publicacion=d["fecha_publicacion"],
            BloqueConocimiento=d["BloqueConocimiento"],
            modalidad=d["modalidad"],
            jornada=int(d["jornada"])
        )
        
        # [POO] Llamada al método del objeto
        o.crear_oferta()

        return {"ok": True, "msg": "Oferta creada correctamente"}
    except Exception as e:
        print("Error API Oferta:", e)
        raise HTTPException(status_code=400, detail=str(e))

# --- OTROS ENDPOINTS ---
@router_admin.post("/universidad")
def crear_universidad(d: dict):
    db.table("universidad").insert({"nombre":d["nombre"], "direccion":d["direccion"]}).execute()
    return {"ok": True}

@router_admin.get("/postulaciones")
def postulaciones():
    return db.table("inscripciones").select("*").execute().data