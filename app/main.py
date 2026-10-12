from fastapi import FastAPI

from app.database.connection import Base, engine
from app.database import models
from app.routers.users import router as users_router
from app.routers.auth import router as auth_router
from app.routers.tasks import router as tasks_router



Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="TaskFlow API",
    description="API REST para gerenciamento de tarefas",
    version="1.0.0"
)


app.include_router(users_router)
app.include_router(auth_router)
app.include_router(tasks_router)


@app.get("/")
def inicio():
    return {
        "mensagem": "TaskFlow API está funcionando!",
        "versao": "1.0.0"
    }


@app.get("/health")
def health():
    return {
        "status": "online"
    }