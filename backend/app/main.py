from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router_auth
from app.api.inscripcion import router_inscripcion
from app.api.dashboard import router_dashboard
from app.api.admin import router_admin
from app.api.examen import router_examen
app = FastAPI(title="SIPU API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_auth, prefix="/auth")
app.include_router(router_inscripcion, prefix="/inscripcion")
app.include_router(router_dashboard, prefix="/dashboard")
app.include_router(router_admin,prefix="/admin")
app.include_router(router_examen, prefix="/examen")
