from fastapi import FastAPI, Depends
from blog import models
from blog.database import engine, get_db
from blog.routers import user,blog,authentication
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware  # <-- 1. IMPORT THIS
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()




models.Base.metadata.create_all(bind=engine)

origins = [
    # The URL for your new frontend (get this from Render after you deploy it)
    "https://my-blog-frontend-e2i4.onrender.com", 
    
    # URLs for local development (if you need them)
    "http://localhost:3000",
    "http://localhost:5173", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Which URLs are allowed
    allow_credentials=True,    # Allows cookies (for auth)
    allow_methods=["*"],         # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],         # Allows all headers
)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(blog.router)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the blog project"}



