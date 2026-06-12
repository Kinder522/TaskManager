from pydantic import BaseModel
from typing import Optional


class BoardCreate(BaseModel):
    name: str

class BoardUpdate(BaseModel):
    name: Optional[str] = None


class BoardResponse(BaseModel):
    id: int
    name: str
    owner_id: int

    class Config:
        from_attributes = True
