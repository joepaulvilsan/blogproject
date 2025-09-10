from sqlalchemy import Column, ForeignKey, Integer, String
from database import Base
from sqlalchemy.orm import relationship

class BlogPost(Base):
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    content = Column(String)
    userid = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates="blog_posts")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    blog_posts = relationship("BlogPost", back_populates="creator")