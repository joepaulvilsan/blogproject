from fastapi import APIRouter, status, Response
from fastapi import Depends
from sqlalchemy.orm import Session
import blog.models as models 
from blog.database import get_db
from blog.schemas import showBlogPost, BlogPost,user     
from typing import List
from blog.repositories.func import getall
import blog.oauth2 as oauth2


router = APIRouter()

@router.post("/blogpost/", status_code=status.HTTP_201_CREATED)
async def create_blog_post(blog_post: BlogPost, db: Session = Depends(get_db), current_user: user = Depends(oauth2.get_current_user)):
    new_blog_post = models.BlogPost(
        title=blog_post.title,
        content=blog_post.content,
        id=blog_post.id,  # Assuming id is part of the BlogPost schema
        userid=current_user.id
    )
    db.add(new_blog_post)
    db.commit()
    db.refresh(new_blog_post)
    return new_blog_post



@router.get("/getallblogpost/", response_model=List[showBlogPost])
async def get_all_blog_posts(db: Session = Depends(get_db)):
    return getall(db)
    

@router.get("/blogpost/{blog_post_id}",response_model=showBlogPost)
async def get_blog_post(blog_post_id: int, db: Session = Depends(get_db), response: Response = None):
    blog_post = db.query(models.BlogPost).filter(models.BlogPost.id == blog_post_id).first()
    if not blog_post:
        if response is not None:
            response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Blog post not found"}
    return blog_post

@router.delete("/blogpost/{blog_post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog_post(blog_post_id: int, db: Session = Depends(get_db)):
    blog_post = db.query(models.BlogPost).filter(models.BlogPost.id == blog_post_id).first()
    if not blog_post:
        return {"error": "Blog post not found"}
    db.delete(blog_post)
    db.commit()
    return {"message": "Blog post deleted successfully"}

@router.put("/blogpost/{blog_post_id}", status_code=status.HTTP_200_OK)
async def update_blog_post(blog_post_id: int, blog_post: BlogPost, db: Session = Depends(get_db)):
    existing_blog_post = db.query(models.BlogPost).filter(models.BlogPost.id == blog_post_id).first()
    if not existing_blog_post:
        return {"error": "Blog post not found"}
    
    existing_blog_post.title = blog_post.title
    existing_blog_post.content = blog_post.content
    db.commit()
    db.refresh(existing_blog_post)
    return existing_blog_post


