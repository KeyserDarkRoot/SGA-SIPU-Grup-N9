from fastapi import APIRouter, HTTPException, Response # <--- OJO: Importar Response
from app.database.ConexionBD.api_supabase import crear_cliente
from app.core.periodo import Periodo
from app.core.oferta_academica import OfertaAcademica
from app.core.reportes import ReporteAsignadosCSV # <--- Importar la nueva clase
from app.core.asignacion_examen import AsignacionMasiva
from datetime import date

router_admin = APIRouter()
db = crear_cliente()
core_masivo = AsignacionMasiva()
# --- 1. DASHBOARD INICIO ---
@router_admin.get("/home_stats")
def home_stats():
    try:
        per = db.table("periodo").select("nombreperiodo").eq("estado", "activo").execute()
        periodo_actual = per.data[0]['nombreperiodo'] if per.data else "No hay periodo activo"
        ins = db.table("inscripciones").select("*", count="exact", head=True).execute()
        total = ins.count
        return {"periodo": periodo_actual, "aspirantes": total}
    except Exception as e:
        print("Error stats:", e)
        return {"periodo": "Error BD", "aspirantes": 0}

# --- 2. GESTIÓN DE PERIODOS (ACTUALIZADO) ---
@router_admin.post("/periodo")
def crear_periodo(d: dict):
    try:
        p = Periodo(
            id_periodo=None,  # 👈 IMPORTANTE
            nombre_periodo=d["nombre"],
            fecha_inicio=d["inicio"],
            fecha_fin=d["fin"]
        )

        r = p.crear_periodo()
        return {"ok": True, "msg": "Periodo creado", "data": r}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router_admin.get("/periodos/listar")
def listar_periodos_gestion():
    """Retorna todos los periodos para mostrarlos en la tabla de gestión"""
    try:
        res = db.table("periodo").select("*").order("idperiodo", desc=True).execute()
        return res.data
    except Exception as e:
        return []

@router_admin.put("/periodo/estado")
def cambiar_estado_periodo(d: dict):
    """
    Lógica de Negocio:
    Si activamos un periodo, debemos DESACTIVAR todos los demás primero.
    Solo puede haber un periodo activo a la vez.
    """
    try:
        nuevo_estado = d["nuevo_estado"] # 'activo' o 'cerrado'
        id_periodo = d["idperiodo"]

        # Si vamos a activar uno, primero apagamos todo
        if nuevo_estado == "activo":
            db.table("periodo").update({"estado": "cerrado"}).neq("idperiodo", 0).execute()

        # Actualizamos el objetivo
        db.table("periodo").update({"estado": nuevo_estado}).eq("idperiodo", id_periodo).execute()
        
        return {"ok": True, "msg": f"Periodo {nuevo_estado} correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router_admin.get("/datos_auxiliares")
def datos_auxiliares():
    try:
        sedes = db.table("sede").select("sede_id, nombre_sede").execute().data
        periodos = db.table("periodo").select("idperiodo, nombreperiodo").execute().data
        return {"sedes": sedes, "periodos": periodos}
    except Exception as e:
        return {"sedes": [], "periodos": []}

# --- 3. OFERTA ACADÉMICA ---
@router_admin.post("/oferta")
def crear_oferta(d: dict):
    try:
        res_id = db.table("oferta_academica").select("ofa_id").order("ofa_id", desc=True).limit(1).execute()
        next_id = (res_id.data[0]["ofa_id"] + 1) if res_id.data else 1
        campos_req = ["nombre_carrera", "periodo_id", "cupos_disponibles", "sede_id", "estado_oferta", "fecha_publicacion", "BloqueConocimiento", "modalidad", "jornada"]
        faltantes = [c for c in campos_req if c not in d]
        if faltantes: raise HTTPException(status_code=400, detail=f"Faltan datos: {', '.join(faltantes)}")

        o = OfertaAcademica(
            ofa_id=next_id, nombre_carrera=d["nombre_carrera"], periodo_id=int(d["periodo_id"]),
            cupos_disponibles=int(d["cupos_disponibles"]), sede_id=d["sede_id"],
            estado_oferta=d["estado_oferta"], fecha_publicacion=d["fecha_publicacion"],
            BloqueConocimiento=d["BloqueConocimiento"], modalidad=d["modalidad"], jornada=int(d["jornada"])
        )
        o.crear_oferta()
        return {"ok": True, "msg": f"Oferta creada con ID {next_id}"}
    except Exception as e:
        print("Error API Oferta:", e)
        raise HTTPException(status_code=400, detail=str(e))

# --- 4. ASPIRANTES ---
@router_admin.get("/aspirante/buscar/{criterio}")
def buscar_aspirante(criterio: str):
    try:
        res = db.table("inscripciones").select("*").ilike("identificacion", f"%{criterio}%").execute()
        return res.data
    except Exception as e:
        return []

@router_admin.put("/aspirante/estado")
def cambiar_estado_aspirante(d: dict):
    try:
        # 1. Recibimos el ID como String (Texto) porque es un UUID
        id_uuid = str(d["id_inscripcion"]) 

        # 2. Actualizamos la columna 'estado' (según tu foto de la BD)
        res = db.table("inscripciones")\
                .update({"estado": d["nuevo_estado"]})\
                .eq("id_inscripcion", id_uuid)\
                .execute()
        
        # 3. Verificación
        if not res.data:
            # Si data está vacío, es que no encontró el ID
            raise HTTPException(status_code=404, detail="No se encontró el estudiante con ese ID")

        return {"ok": True, "msg": "Estado actualizado correctamente"}

    except Exception as e:
        print(f"Error al actualizar estado: {e}")
        raise HTTPException(status_code=400, detail=str(e))
@router_admin.put("/aspirante/nota")
def actualizar_nota(d: dict):
    try:
        db.table("inscripciones").update({"puntaje_final": int(d["nota"])}).eq("id_inscripcion", d["id_inscripcion"]).execute()
        return {"ok": True, "msg": "Nota actualizada"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router_admin.get("/postulaciones")
def postulaciones():
    return db.table("inscripciones").select("*").execute().data

# --- 6. REPORTES ---
@router_admin.get("/reportes/stats")
def obtener_reportes():
    try:
        data = db.table("inscripciones").select("carrera_seleccionada, estado_inscripcion").execute().data
        conteo_carreras = {}
        for d in data:
            c = d.get("carrera_seleccionada", "Desconocida")
            conteo_carreras[c] = conteo_carreras.get(c, 0) + 1
        conteo_estados = {"ASIGNADO": 0, "RECHAZADO": 0, "REGISTRADO": 0, "INVALIDADO": 0}
        for d in data:
            e = d.get("estado_inscripcion", "REGISTRADO")
            conteo_estados[e] = conteo_estados.get(e, 0) + 1
        return {"carreras": {"labels": list(conteo_carreras.keys()), "values": list(conteo_carreras.values())}, "estados": {"labels": list(conteo_estados.keys()), "values": list(conteo_estados.values())}}
    except Exception as e:
        return {"carreras": {"labels":[], "values":[]}, "estados": {"labels":[], "values":[]}}


## Cambiar para exportar CSV de asignados    
@router_admin.get("/asignacion/exportar/{periodo_id}")
def exportar_asignados(periodo_id: int):
    """
    Genera un archivo CSV con la lista de estudiantes ASIGNADOS en el periodo.
    Usa Polimorfismo (ReporteAsignadosCSV).
    """
    try:
        # 1. Obtener carreras del periodo
        ofertas = db.table("oferta_academica").select("nombre_carrera").eq("periodo_id", periodo_id).execute().data
        carreras = [o["nombre_carrera"] for o in ofertas]
        
        if not carreras:
            raise HTTPException(status_code=404, detail="No hay carreras en este periodo")

        # 2. Obtener estudiantes ASIGNADOS de esas carreras
        # Nota: Supabase 'in' usa paréntesis: .in_("columna", [lista])
        asignados = db.table("inscripciones")\
            .select("*")\
            .in_("carrera_seleccionada", carreras)\
            .eq("estado_inscripcion", "ASIGNADO")\
            .execute().data

        # 3. Usar Polimorfismo para generar el reporte
        reporteador = ReporteAsignadosCSV()
        csv_content = reporteador.generar(asignados)

        # 4. Retornar como archivo descargable
        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=Listado_Asignados_P{periodo_id}.csv"}
        )

    except Exception as e:
        print("Error exportando:", e)
        raise HTTPException(status_code=500, detail=str(e))
    
@router_admin.post("/asignar-examenes/{idperiodo}")
def asignar_examenes(idperiodo:int):

    try:
        r = core_masivo.ejecutar(idperiodo)
        return {"ok":True,"data":r}

    except Exception as e:
        return {"ok":False,"error":str(e)}

# --- 7. CONFIGURACIÓN EXAMEN ---
@router_admin.post("/config-examen")
def configurar_examen(data:dict):

    # Eliminar configuraciones previas para el mismo periodo
    db.table("config_examen")\
        .update({"estado":"INACTIVO"})\
        .eq("periodo_id", data["periodo_id"])\
        .execute()


    payload = {
        "periodo_id": data["periodo_id"],
        "fecha_inicio": data["fecha_inicio"],
        "estado": "ACTIVO"   # 👈 CLAVE
    }

    db.table("config_examen")\
      .insert(payload)\
      .execute()

    return {
      "ok": True,
      "msg": "Fecha de inicio guardada correctamente"
    }


@router_admin.post("/asignacion/ejecutar")
def ejecutar_asignacion(data: dict):

    periodo = data["periodo_id"]

    # Validar estado del periodo
    p = db.table("periodo")\
          .select("estado")\
          .eq("idperiodo", periodo)\
          .limit(1)\
          .execute()

    if not p.data:
        raise HTTPException(404,"Periodo no existe")

    if p.data[0]["estado"] != "cerrado":
        raise HTTPException(
            status_code=400,
            detail="Debe CERRAR el periodo antes de asignar"
        )

    core = AsignacionMasiva()
    
    # Validar si ya se ejecutó la asignación    
    asig = db.table("asignacion_examen")\
        .select("asignacion_id")\
        .eq("periodo_id", periodo)\
        .limit(1)\
        .execute()

    if asig.data:
        raise HTTPException(
            400,
            "La asignación ya fue ejecutada"
        )

    core.ejecutar(periodo)

    return {
        "ok": True,
        "msg": "Asignación masiva ejecutada correctamente"
    }

@router_admin.get("/asignacion/existe/{periodo}")
def existe_asignacion(periodo:int):

 r = db.table("asignacion_examen")\
       .select("asignacion_id")\
       .eq("periodo_id", periodo)\
       .limit(1)\
       .execute()

 return {"existe": True if r.data else False}


