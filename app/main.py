import logging
from fastapi import FastAPI
import os
from contextlib import asynccontextmanager


from app.api.v1 import auth_routers, task_routers

#Middleware
from fastapi.middleware.cors import CORSMiddleware


#Core
from app.core.log import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Eventos de startup y shutdown de la aplicación."""
    logger.info("Iniciando la aplicación...")
    yield
    logger.info("La aplicación se está apagando.")

app = FastAPI(
    title="API de Tareas (TODOs)",
    description="Una API para gestionar tareas personales.",
    lifespan=lifespan
)

# Incluir routers
app.include_router(auth_routers.router, prefix="/users", tags=["users"])
app.include_router(task_routers.router, prefix="/tasks", tags=["tasks"])


origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:5500",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Bienvenido a la API de Tareas"}