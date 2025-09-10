from sqlalchemy.orm import Session
import blog.models as models

def getall(db: Session):
    return db.query(models.BlogPost).all()
