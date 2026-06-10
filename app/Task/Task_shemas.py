from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM


class TaskCreate(TaskBase):
    board_id: int
    assignee_id: Optional[int] = None


class TaskResponse(TaskBase):
    id: int
    board_id: int
    assignee_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True