from fastapi import APIRouter, Depends,status,HTTPException
from blog.schemas import Login,Token
from datetime import timedelta
from blog.authtoken import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from blog.database import get_db
from sqlalchemy.orm import Session
import blog.models as models
import blog.hashing as hashing
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Authentication"]
)
@router.post("/login/")
async def login(login: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == login.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username or password")

    if not hashing.verify_password(login.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")