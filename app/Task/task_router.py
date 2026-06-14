from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.Task.Task_shemas import TaskCreate, TaskResponse
from app.database.models import Task

TaskRouter = APIRouter(prefix="", tags=["tasks"])


@TaskRouter.get("/api/boards/{board_id}/tasks", response_model=List[TaskResponse])
def get_task(board_id: int, db: Session = Depends(get_db)):
    boards = db.query(Task).filter(Task.board_id == board_id).all()
    return boards


@TaskRouter.post("/api/boards/{board_id}/tasks",response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(board_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(title=task.title, board_id=board_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task