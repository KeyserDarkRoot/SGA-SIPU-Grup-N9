from fastapi import APIRouter
from app.database.ConexionBD.api_supabase import crear_cliente
from app.core.inscripcion import Inscripcion

router_inscripcion=APIRouter()
db=crear_cliente()

@router_inscripcion.get("/datos/{cedula}")
def datos(cedula:str):
 res=db.table("registronacional")\
       .select("*")\
       .eq("identificacion",cedula)\
       .execute()
 return res.data[0]

@router_inscripcion.get("/universidades")
def universidades():
 return db.table("universidad")\
          .select("ies_id,nombre")\
          .execute().data

@router_inscripcion.get("/oferta")
def oferta():
 return db.table("oferta_academica")\
          .select("*")\
          .execute().data

@router_inscripcion.post("/finalizar")
def finalizar(d:dict):

 nueva=Inscripcion(
  periodo_id=None,
  ies_id=d["ies_id"],
  tipo_documento="Cédula",
  identificacion=d["cedula"],
  nombres=d["nombres"],
  apellidos=d["apellidos"],
  carrera_seleccionada=d["carrera"]
 )

 nueva.guardar_en_supabase()
 return {"ok":True}
