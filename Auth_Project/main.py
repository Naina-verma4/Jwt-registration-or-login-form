from fastapi import FastAPI
from fastapi import Request #Browser request access karne ke liye.
from fastapi import Form #Form data access karne ke liye.
from fastapi import Depends #Dependency injection ke liye.

from fastapi.templating import Jinja2Templates #HTML templates ko render karne ke liye.

from sqlalchemy.orm import Session # database session ke liye.

from database import SessionLocal
from database import engine # postgreSQL database se connect karne ke liye.
from database import Base

from models import User
from auth import *
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(
    directory="templates"
)
Base.metadata.create_all(bind=engine)

def get_db(): #

    db = SessionLocal() #connecting to database

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html"
    )

@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )

@app.post("/register")
def register(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == email
    ).first() #check if email already exists in database.

    if existing_user:
        return {"message": "Email already exists"}

    user = User(
        name=name,
        email=email,
        password=hash_password(password)
    )

    db.add(user) 
    db.commit()

    return {"message": "Registration Successful"}


@app.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        return {"message": "User not found"}

    if not verify_password(
        password,
        user.password
    ):
        return {"message": "Wrong Password"}

    token = create_access_token(
        {"sub": user.email}
    )
    return templates.TemplateResponse(
    request=request,
    name="dashboard.html",
    context={
        "username": user.name
    }
)