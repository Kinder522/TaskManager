from fastapi import APIRouter, Depends, HTTPException, Response,status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database.models import User
from app.User.user_crud import get_user_by_username
from app.core.security import get_password_hash, verify_password, create_access_token
from app.User.User_schemas import UserCreate, UserLogin


UserRouter = APIRouter(prefix="", tags=["Auth"])




@UserRouter.post("/api/auth/register", status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_username(db, name=user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Этот логин уже занят")

    hashed_pwd = get_password_hash(user_data.password)
    new_user = User(username=user_data.username,email=user_data.email, password_hash=hashed_pwd)
    db.add(new_user)
    db.commit()
    return {"status": "User created successfully"}


@UserRouter.post("/api/auth/login")
def login(response: Response, user_data: UserLogin, db: Session = Depends(get_db)):
    # Ищем юзера в базе
    user = get_user_by_username(db, name=user_data.username)
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    # Создаем токен, зашивая туда ID пользователя
    token = create_access_token(data={"user_id": user.id})

    # ЗАПИСЫВАЕМ ТОКЕН В КУКИ
    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,  # Защита: JavaScript на фронтенде не сможет украсть куку
        max_age=86400,  # Время жизни в секундах (1 день)
        samesite="lax"  # Защита от CSRF-атак
    )

    return {"message": "Успешный вход!"}


@UserRouter.post("/logout")
def logout(response: Response):
    response.delete_cookie("session_token")
    return {"message": "Вы вышли из системы"}