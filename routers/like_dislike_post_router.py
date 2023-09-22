from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.models import LikeDislikePost
from schemas.like_dislike_post import LikeDislikePostBase, LikeDislikePostCreate, LikeDislikePostList

router = APIRouter()

@router.get("/like_dislike_post", response_model=LikeDislikePostList)
def get_all_like_dislike_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    like_dislike_posts = db.query(LikeDislikePost).offset(skip).limit(limit).all()
    return {"like_dislike_posts": like_dislike_posts}

@router.post("/like_dislike_post", response_model=LikeDislikePostBase)
def create_like_dislike_post(like_dislike_post: LikeDislikePostCreate, db: Session = Depends(get_db)):
    new_like_dislike_post = LikeDislikePost(**like_dislike_post.dict())
    db.add(new_like_dislike_post)
    db.commit()
    db.refresh(new_like_dislike_post)
    return new_like_dislike_post