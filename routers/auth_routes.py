from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from models import User
from auth import hash_password, verify_password, get_current_user

router = APIRouter(tags=["Auth"])
templates = Jinja2Templates(directory="templates")

@router.get("/register")
def register_page(request: Request, db: Session = Depends(get_db)):
    if get_current_user(request, db):
        return RedirectResponse(url="/todos", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse(request, "register.html", {})

@router.post("/register")
def register_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    mobilenumber: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Check if username or email already exists
    existing_user = db.query(User).filter(
        (User.username == username.strip()) | (User.email == email.strip())
    ).first()
    
    if existing_user:
        return templates.TemplateResponse(
            request, "register.html", {"error": "Username or Email is already taken."}
        )

    new_user = User(
        username=username.strip(),
        email=email.strip(),
        mobilenumber=mobilenumber.strip(),
        hashed_password=hash_password(password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    response = RedirectResponse(url="/todos", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="user_id", value=str(new_user.id), httponly=True)
    return response

@router.get("/login")
def login_page(request: Request, db: Session = Depends(get_db)):
    if get_current_user(request, db):
        return RedirectResponse(url="/todos", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse(request, "login.html", {})

@router.post("/login")
def login_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username.strip()).first()
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            request, "login.html", {"error": "Invalid username or password."}
        )

    response = RedirectResponse(url="/todos", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="user_id", value=str(user.id), httponly=True)
    return response

@router.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="user_id")
    return response