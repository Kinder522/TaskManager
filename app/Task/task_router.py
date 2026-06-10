from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.Task import task as task_crud, Task_shemas as task_schema

TaskRouter = APIRouter(prefix="/tasks", tags=["tasks"])

@TaskRouter.post("/", response_model=task_schema.TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: task_schema.TaskCreate, db: Session = Depends(get_db)):
    return task_crud.create_task(db, task)

@TaskRouter.get("/", response_model=List[task_schema.TaskResponse])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = task_crud.get_tasks(db, skip=skip, limit=limit)
    return tasks

@TaskRouter.get("/{task_id}", response_model=task_schema.TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = task_crud.get_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@TaskRouter.put("/{task_id}", response_model=task_schema.TaskResponse)
def update_task(task_id: int, task: task_schema.TaskCreate, db: Session = Depends(get_db)):
    db_task = task_crud.update_task(db, task_id, task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@TaskRouter.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task_crud.delete_task(db, task_id)
    return None