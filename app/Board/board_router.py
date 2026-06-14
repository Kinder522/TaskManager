from fastapi import APIRouter, Depends,HTTPException,status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database.database import get_db
from app.database.models import Board
from app.Board.Board_schemas import BoardResponse,BoardCreate


BoardRouter = APIRouter(prefix="/api/boards", tags=["Boards"])


@BoardRouter.get("", response_model=list[BoardResponse])
def get_user_boards(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    boards = db.query(Board).filter(Board.owner_id == user_id).all()
    return boards


@BoardRouter.post("/create", response_model=BoardResponse, status_code=status.HTTP_201_CREATED)
def create_board(board_data: BoardCreate,user_id: int = Depends(get_current_user),  db: Session = Depends(get_db)):
    new_board = Board(name=board_data.name, owner_id=user_id)
    db.add(new_board)
    db.commit()
    db.refresh(new_board)
    return new_board


@BoardRouter.delete("/{board_id}")
def delete_board(
        board_id: int,
        db: Session = Depends(get_db),
        user_id: int = Depends(get_current_user)
):
    board = db.query(Board).filter(Board.id == board_id, Board.owner_id == user_id).first()

    if not board:
        raise HTTPException(status_code=404, detail="Доска не найдена или у вас нет прав на её удаление")

    db.delete(board)
    db.commit()
    return {"message": "Доска успешно удалена"}