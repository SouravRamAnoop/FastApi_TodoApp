from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from models import Todo
from auth import get_current_user

router = APIRouter(tags=["Todos"])
templates = Jinja2Templates(directory="templates")

# GET All User's Todos (Dashboard)
@router.get("/todos")
def list_todos(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    user_todos = db.query(Todo).filter(Todo.user_id == user.id).all()
    return templates.TemplateResponse(request, "todos.html", {"user": user, "todos": user_todos})

# POST Create Todo
@router.post("/todos/create")
def create_todo(request: Request, title: str = Form(...), db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    if title.strip():
        new_todo = Todo(title=title.strip(), user_id=user.id)
        db.add(new_todo)
        db.commit()

    return RedirectResponse(url="/todos", status_code=status.HTTP_303_SEE_OTHER)

# POST Toggle Completed Status
@router.post("/todos/toggle/{todo_id}")
def toggle_todo(request: Request, todo_id: int, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user.id).first()
    if todo:
        todo.completed = not todo.completed
        db.commit()

    return RedirectResponse(url="/todos", status_code=status.HTTP_303_SEE_OTHER)

# GET Edit Page
@router.get("/todos/edit/{todo_id}")
def edit_todo_page(request: Request, todo_id: int, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user.id).first()
    if not todo:
        return RedirectResponse(url="/todos", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(request, "edit_todo.html", {"user": user, "todo": todo})

# POST Update Todo
@router.post("/todos/update/{todo_id}")
def update_todo(request: Request, todo_id: int, title: str = Form(...), db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user.id).first()
    if todo and title.strip():
        todo.title = title.strip()
        db.commit()

    return RedirectResponse(url="/todos", status_code=status.HTTP_303_SEE_OTHER)

# POST Delete Todo
@router.post("/todos/delete/{todo_id}")
def delete_todo(request: Request, todo_id: int, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user.id).first()
    if todo:
        db.delete(todo)
        db.commit()

    return RedirectResponse(url="/todos", status_code=status.HTTP_303_SEE_OTHER)