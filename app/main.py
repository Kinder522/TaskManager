from fastapi import FastAPI, Request, Depends, HTTPException, Form, Cookie, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.User.user_router import UserRouter
from app.database.database import get_db

app = FastAPI(title="Менеджер задач")
templates = Jinja2Templates(directory="app/templates")
# app.include_router(TaskRouter)
app.include_router(UserRouter)


@app.get("/", response_class=HTMLResponse)
def main_page(request: Request, db: Session = Depends(get_db)):
    session_token = request.cookies.get("session_token")

    if not session_token:
        return RedirectResponse(url="/auth/register", status_code=status.HTTP_303_SEE_OTHER)

    try:
        current_user = get_current_user(session_token, db)
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"username": current_user.username}
        )
    except Exception:
        return RedirectResponse(url="/auth/register", status_code=status.HTTP_303_SEE_OTHER)
