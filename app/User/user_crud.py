from sqlalchemy.orm import Session
from app.database.models import User

def get_user_by_username(db: Session,name: str):
    return db.query(User).filter(User.username == name).first()

def get_user_by_id(db: Session, id: int):
    return db.query(User).filter(User.id == id).first()