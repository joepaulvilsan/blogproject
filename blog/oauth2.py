from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import InvalidTokenError
from typing import Annotated
from blog.database import get_db
import blog.models as models
from blog.schemas import TokenData
import authtoken

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = authtoken.SECRET_KEY
ALGORITHM = authtoken.ALGORITHM


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception

    # 🔑 Query from real DB instead of fake_users_db
    user = db.query(models.User).filter(models.User.email == token_data.email).first()

    if user is None:
        raise credentials_exception
    return user