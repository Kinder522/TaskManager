from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True,index=True)
    board_id = Column(Integer, ForeignKey("boards.id", ondelete="CASCADE"),nullable=False)
    assignee_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"),nullable=True)

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String,default="todo")
    priority = Column(String,default="medium")

    board = relationship("Board", back_populates="tasks")
    assignee = relationship("User", back_populates="tasks")