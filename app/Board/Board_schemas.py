from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BoardBase(BaseModel):
    name: str
    description: Optional[str] = None


class BoardCreate(BoardBase):
    owner_id: int


class BoardResponse(BoardBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True