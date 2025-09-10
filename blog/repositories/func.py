from sqlalchemy.orm import Session
import models

def getall(db: Session):
    return db.query(models.BlogPost).all()
