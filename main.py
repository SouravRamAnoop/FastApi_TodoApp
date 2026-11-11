from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from database import engine, Base
from routers import auth_routes, todo_routes

# Create database tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Authenticated Todo App")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_routes.router)
app.include_router(todo_routes.router)

# Redirect root URL to todos or login
@app.get("/")
def root():
    return RedirectResponse(url="/todos")