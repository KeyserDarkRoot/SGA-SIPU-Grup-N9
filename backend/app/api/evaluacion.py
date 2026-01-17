from fastapi import APIRouter
from app.services.evaluacion_service import EvaluacionService
from app.database.ConexionBD.api_supabase import crear_cliente

router_eval = APIRouter()
service = EvaluacionService()
db = crear_cliente()

# ===================== RENDIR EXAMEN =====================

@router_eval.post("/rendir")
def rendir_examen(data:dict):

    try:
        res = service.registrar_evaluacion(data)
        return {"ok": True, "data": res}

    except Exception as e:
        print("❌ ERROR EVALUACION:", e)
        return {
            "ok": False,
            "error": str(e)
        }


# ===================== VERIFICAR SI YA RINDIÓ =====================

@router_eval.get("/verificar/{cedula}")
def verificar_evaluacion(cedula:str):

    res = db.table("evaluacion")\
            .select("id_evaluacion")\
            .eq("identificacion", cedula)\
            .execute()

    if res.data:
        return {"ok": True}
    
    return {"ok": False}


@router_eval.get("/periodo-activo")
def periodo_activo():

    res = db.table("periodo")\
            .select("idperiodo")\
            .eq("estado","activo")\
            .execute()

    return res.data[0] if res.data else None


@router_eval.get("/ies/{cedula}")
def obtener_ies(cedula:str):

    res = db.table("inscripciones")\
            .select("ies_id")\
            .eq("identificacion", cedula)\
            .execute()

    return res.data[0] if res.data else None


@router_eval.get("/config-modalidad")
def obtener_modalidad():

    try:
        # periodo activo
        p = db.table("periodo")\
              .select("idperiodo")\
              .eq("estado","activo")\
              .execute()

        if not p.data:
            return {"error": "No hay periodo activo"}

        idp = p.data[0]["idperiodo"]

        # configuracion
        cfg = db.table("configuracion_sistema")\
                .select("valor")\
                .eq("tipo_config","MODALIDAD_EXAMEN")\
                .eq("idperiodo",idp)\
                .eq("estado","ACTIVO")\
                .execute()

        if not cfg.data:
            return {"error": "No existe configuración de examen"}

        return cfg.data[0]

    except Exception as e:
        print("❌ ERROR CONFIG MODALIDAD:", e)
        return {"error": str(e)}
