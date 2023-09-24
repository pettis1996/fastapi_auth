from pydantic import BaseModel, Field, EmailStr

class PostSchema(BaseModel):
    id: int 
    title: str 
    text: str 
    owner_id: int

   
    class Config:
        schema_extra = {
            "post_demo": {
                "title": "some title here",
                "text": "some content here"
            }
        }
        orm_mode = True

class UserSchema(BaseModel):
    id: int
    fullname: str 
    email: EmailStr 
    password: str 
    is_active: bool 
    posts: list[PostSchema] = []
    class Config:
        the_schema = {
            "user_demo": {
                "id": 1,
                "fullname": "John",
                "email": "john@doe.com",
                "password": "password",
                "is_active": True,
                "posts": []
            },
        }
        orm_mode=True

class UserLoginSchema(BaseModel):
    email: EmailStr 
    password: str 
    class Config:
        the_schema = {
            "user_demo": {  
                "email": "john@doe.com",
                "password": "password",
            }
        }