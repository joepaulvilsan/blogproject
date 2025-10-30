from pydantic import BaseModel,Field
from typing import List

class BlogPostCreate(BaseModel):
    title: str
    content: str
    class Config:
        from_attributes = True
class BlogPost(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        from_attributes = True



class user(BaseModel):
    id: int
    username: str
    email: str
    password: str

    class Config:
        from_attributes = True


class showUser(BaseModel):
    name: str
    email: str
    blogs: List[BlogPost] = Field(default_factory=list)


    class Config:
        from_attributes = True


class showBlogPost(BaseModel):
    title: str
    content: str
    creator: showUser
   

    class Config:
        from_attributes = True

class Login(BaseModel):
    username: str
    password: str   
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
