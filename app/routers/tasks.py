from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.models import Task
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.auth.dependencies import obter_usuario_id



router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(tarefa: TaskCreate,usuario_id: int = Depends(obter_usuario_id),db: Session = Depends(get_db)):
    nova_tarefa = Task(title=tarefa.title,description=tarefa.description,user_id=usuario_id)

    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)

    return nova_tarefa

@router.get("/", response_model=list[TaskResponse])
def list_tasks(usuario_id: int = Depends(obter_usuario_id),db: Session = Depends(get_db)):
    tarefas = (db.query(Task).filter(Task.user_id == usuario_id).all())

    return tarefas

@router.get("/{task_id}", response_model=TaskResponse)
def buscar_tarefa(task_id: int,usuario_id: int = Depends(obter_usuario_id),db: Session = Depends(get_db)):
    tarefa = (db.query(Task).filter(Task.id == task_id,Task.user_id == usuario_id).first())

    if not tarefa:raise HTTPException(status_code=404,detail="Tarefa não encontrada.")

    return tarefa

@router.put("/{task_id}", response_model=TaskResponse)
def atualizar_tarefa(task_id: int, dados: TaskUpdate, usuario_id: int = Depends(obter_usuario_id), db: Session = Depends(get_db)):
    tarefa = db.query(Task).filter(Task.id == task_id, Task.user_id == usuario_id).first()

    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")

    tarefa.title = dados.title
    tarefa.description = dados.description
    tarefa.completed = dados.completed

    db.commit()
    db.refresh(tarefa)

    return tarefa

@router.delete("/{task_id}", status_code=200)
def excluir_tarefa(task_id: int, usuario_id: int = Depends(obter_usuario_id), db: Session = Depends(get_db)):
    tarefa = db.query(Task).filter(Task.id == task_id, Task.user_id == usuario_id).first()

    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")

    db.delete(tarefa)
    db.commit()

    return {"detail": "Tarefa excluída com sucesso."}