from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic.types import conint


class Userout(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime

    class Config:
        orm_mode = True


class Post(BaseModel):
    title : str
    content : str
    id : int
    owner_id : int
    owner: Userout

class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    pass


class Response(Post):
    pass
    owner: Userout

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

class User(BaseModel):
    email : EmailStr
    password : str

class UserCreate(User):
    pass


class UserLogin(BaseModel):
    email: EmailStr
    password : str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir : conint(le=1)

class VoteDel(BaseModel):
    post_id: int