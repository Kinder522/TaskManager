from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status,Cookie
from sqlalchemy.orm import Session
import bcrypt
from app.User.user_crud import get_user_by_id
from app.database.database import get_db

# Настройки безопасности
SECRET_KEY = "67" # Поменяй на свою строку
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # Кука будет жить 1 день

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(session_token: str | None = Cookie(None), db: Session = Depends(get_db)):
    # 1. Проверяем, есть ли кука вообще
    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Куки нет, авторизуйтесь!"
        )

    try:
        # 2. Расшифровываем JWT-токен из куки
        payload = jwt.decode(session_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Токен сломан")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Токен просрочен или неверен")

    # 3. Идем в базу через CRUD, чтобы проверить, существует ли еще такой юзер
    # (Для этого в user_crud надо будет написать функцию get_user_by_id)
    user = get_user_by_id(db, id=user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Пользователь не найден")

    return user_id