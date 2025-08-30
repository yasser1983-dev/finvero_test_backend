import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.db import get_db
from app.repositories import MongoTaskRepository, TaskRepository
from app.routes import router as tasks_router
from app.utils import install_error_handlers


FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")


app = FastAPI(title="To-Do API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN, "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# DI: enlaza la interfaz de repositorio con Mongo en producción
async def get_repo(db: AsyncIOMotorDatabase = Depends(get_db)) -> TaskRepository:
    return MongoTaskRepository(db["tasks"])


app.dependency_overrides[TaskRepository] = get_repo


# Rutas
app.include_router(tasks_router)


# Errores
install_error_handlers(app)

@app.get("/")
async def root():
    return {"status": "ok"}