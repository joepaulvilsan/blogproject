



from fastapi import APIRouter,status
from fastapi import Depends
from sqlalchemy.orm import Session
import blog.models as models 
from blog.database import get_db
from blog.schemas import showUser
from typing import List
from blog.schemas import user
import blog.hashing as hashing
router = APIRouter(
    tags=["Users"]
)


@router.get("/getallusers/", response_model=List[showUser])
async def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.post("/createuser/", status_code=status.HTTP_201_CREATED, response_model=showUser)
async def create_user(user: user, db: Session = Depends(get_db)):
    hashed_password = hashing.hash_password(user.password)
    new_user = models.User(
        id=user.id,
        name=user.username,
        email=user.email,
        password=hashed_password  # Store the hashed password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user