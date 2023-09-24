from pydantic import BaseModel, Field, EmailStr

class PostSchema(BaseModel):
    id: int = Field(default=None)
    title: str = Field(default=None)
    text: str = Field(default=None)
    class Config:
        schema_extra = {
            "post_demo": {
                "title": "some title here",
                "text": "some content here"
            }
        }

class UserSchema(BaseModel):
    fullname: str = Field(default=None)
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)
    class Config:
        the_schema = {
            "user_demo": {
                "fullname": "John",
                "email": "john@doe.com",
                "password": "password",
            },
        }

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)
    class Config:
        the_schema = {
            "user_demo": {  
                "email": "john@doe.com",
                "password": "password",
            }
        }