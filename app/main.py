from fastapi import FastAPI, Request,Depends,HTTPException,Form
from app.database.models import Task,Board,User
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
#from app.routers.task_router import TaskRouter

from app.database.database import get_db

app = FastAPI(title="Менеджер задач")
templates = Jinja2Templates(directory="app/templates")
#app.include_router(TaskRouter)
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    boards = db.query(Board).all()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"tasks": tasks, "boards": boards}
    )