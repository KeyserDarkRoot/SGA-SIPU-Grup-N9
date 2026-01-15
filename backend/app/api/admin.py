from fastapi import APIRouter
from app.database.ConexionBD.api_supabase import crear_cliente
from app.core.periodo import Periodo
from app.core.oferta_academica import OfertaAcademica

router_admin=APIRouter()
db=crear_cliente()

@router_admin.post("/periodo")
def crear_periodo(d:dict):

 p=Periodo(d["nombre"],d["inicio"],d["fin"])
 db.table("periodo").insert({
  "nombre":p.nombre,
  "fecha_inicio":p.fecha_inicio,
  "fecha_fin":p.fecha_fin
 }).execute()

 return {"ok":True}

@router_admin.post("/oferta")
def crear_oferta(d:dict):

 o=OfertaAcademica(
  d["bloque"],
  d["carrera"],
  int(d["cupos"])
 )

 db.table("oferta_academica").insert({
  "BloqueConocimiento":o.bloque,
  "nombre_carrera":o.carrera,
  "cupos_disponibles":o.cupos
 }).execute()

 return {"ok":True}

@router_admin.post("/universidad")
def crear_universidad(d:dict):

 db.table("universidad").insert({
  "nombre":d["nombre"],
  "direccion":d["direccion"]
 }).execute()

 return {"ok":True}

@router_admin.get("/postulaciones")
def postulaciones():
 return db.table("inscripciones").select("*").execute().data


def verificar_admin(user):
    if user.get("rol") != "Admin":
        raise Exception("Acceso denegado")
