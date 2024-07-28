# Sofia Starinnova Completed: 6/25/24

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# Database setup
DATABASE_URL = "sqlite:///./db.sqlite"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    complete = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)

# Static files and templates setup
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Routes
@app.get("/", response_class=HTMLResponse)
async def read_todos(request: Request):
    session = SessionLocal()
    todo_list = session.query(Todo).all()
    session.close()
    return templates.TemplateResponse("base.html", {"request": request, "todo_list": todo_list})

@app.post("/add", response_class=RedirectResponse)
async def add_todo(title: str = Form(...)):
    session = SessionLocal()
    new_todo = Todo(title=title)
    session.add(new_todo)
    session.commit()
    session.close()
    return RedirectResponse(url="/", status_code=303)

@app.get("/update/{todo_id}", response_class=RedirectResponse)
async def update(todo_id: int):
    session = SessionLocal()
    todo = session.query(Todo).filter(Todo.id == todo_id).first()
    todo.complete = not todo.complete
    session.commit()
    session.close()
    return RedirectResponse(url="/", status_code=303)

@app.get("/delete/{todo_id}", response_class=RedirectResponse)
async def delete(todo_id: int):
    session = SessionLocal()
    todo = session.query(Todo).filter(Todo.id == todo_id).first()
    session.delete(todo)
    session.commit()
    session.close()
    return RedirectResponse(url="/", status_code=303)
