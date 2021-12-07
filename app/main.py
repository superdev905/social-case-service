from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.API.v1 import router as V1_Routes
from app.database.main import get_database

app = FastAPI(title="Servicio de Casos sociales")

app.include_router(V1_Routes.router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
async def startup():
    get_database()
