from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True,index=True,autoincrement=True)
    username = Column(String(50), nullable=False,unique=True)
    email = Column(String(50), nullable=False,unique=True)
    password_hash = Column(String, nullable=False)

    boards = relationship("Board", back_populates="owner")
    tasks = relationship("Task", back_populates="assignee")
