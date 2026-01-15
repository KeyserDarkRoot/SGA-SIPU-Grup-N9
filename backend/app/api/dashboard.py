from fastapi import APIRouter
from app.database.ConexionBD.api_supabase import crear_cliente

router_dashboard = APIRouter()
db = crear_cliente()

@router_dashboard.get("/estado/{cedula}")
def estado(cedula:str):

    res=db.table("registronacional")\
          .select("estadoregistronacional")\
          .eq("identificacion",cedula)\
          .execute()

    if res.data:
        return {"estado":res.data[0]["estadoregistronacional"].upper()}

    return {"estado":"NO REGISTRADO"}
