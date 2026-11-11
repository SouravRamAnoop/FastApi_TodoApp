Full-Stack Todo Application (FastAPI + Jinja2)

A traditional server-rendered full-stack web application built with FastAPI and Jinja2 templates, backed by SQLite.

Features

User Authentication: Secure registration and login system powered by password hashing (bcrypt).

Server-Rendered Views: HTML pages dynamically generated and rendered using Jinja2 templates.

Persistent Storage: SQLite database managed via SQLAlchemy ORM.
Task Management: Create, view, complete, and delete personal tasks securely tied to individual user accounts.

Tech Stack

Backend: Python, FastAPI, Uvicorn
Database: SQLite, SQLAlchemy
Frontend: Jinja2 Templates, HTML5, CSS3

Project Structure

project-root/
│
├── database.py       # Database configuration and session management
├── models.py         # SQLAlchemy database models (User, Todo)
├── auth.py           # Password hashing and verification utilities
├── main.py           # FastAPI application and route handlers
├── templates/        # Jinja2 HTML templates
│   ├── login.html
│   ├── register.html
│   └── base.html
│   └── todos.html.     
└── static/           # CSS stylesheets and static assets
    └── style.css

Getting Started & Installation

Clone the repository: 

git clone "repository link"

Create and activate a virtual environment: 
python -m venv venv

On Windows:
venv\Scripts\activate

On macOS/Linux:
source venv/bin/activate

Install dependencies: 
pip install fastapi uvicorn sqlalchemy bcrypt jinja2 python-multipart

Run the application: uvicorn main:app --reload

Open in browser: Navigate to http://127.0.0.1:8000 to use the application.
