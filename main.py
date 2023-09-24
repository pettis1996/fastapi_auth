import uvicorn
from fastapi import Body, FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import PostSchema, UserSchema, UserLoginSchema   

from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import jwtBearer
from app import crud
from app.models import User,Post
from app.schemas import UserSchema, UserCreateSchema
from app.database import SessionLocal, engine
from app import database

posts = [
    {
        "id": 1, 
        "title": "penguins",
        "text": "some content about penguins goes here"
    },
    {
        "id": 2, 
        "title": "tigers",
        "text": "some content about tigers goes here"
    },
    {
        "id": 3, 
        "title": "deers",
        "text": "some content about deers goes here"
    },
]

users = []

database.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", tags=["test"])
def greet():
    return {"detail": "Hello World."}

@app.get("/posts", tags=["posts"])
def get_posts():
    return {"data": posts}

@app.get("/posts/{id}", tags=["posts"])
def get_post_by_id(id: int):
    if id > len(posts):
        return {
            "error": "Post with this ID does not exist."
        }
    
    for post in posts:
        if post["id"] == id:
            return {
                "data": post
            }
        
@app.post("/posts", dependencies=[Depends(jwtBearer())], tags=["posts"])
def add_post(post: PostSchema):
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {
        "info": "Post Added."
    }

@app.get("/users/", response_model=list[UserSchema])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.post("/user/signup", tags=["users"])
def user_signup(user: UserSchema = Body(default=None)):
    if user in users:
        raise HTTPException(status_code=405, detail="User already exists.")
    users.append(user)
    return user

def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
        return False
    
@app.post("/user/login", tags=["users"])
def user_login(user: UserLoginSchema = Body(default=None)):
    if check_user(user):
        return signJWT(user.email)
    else:
        return {
            "error": "Invalid Login Details."
        }
    
@app.post("/users/", response_model=UserSchema, tags=["users"])
def create_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

