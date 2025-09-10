from fastapi import FastAPI, Depends
from blog import models
from blog.database import engine, get_db
from blog.routers import user,blog,authentication
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()




models.Base.metadata.create_all(bind=engine)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(blog.router)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the ConnectSphere API"}



