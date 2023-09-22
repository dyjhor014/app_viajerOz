from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.models import Comment
from schemas.comment import CommentBase, CommentCreate, CommentList

router = APIRouter()

@router.get("/comment", response_model=CommentList)
def get_all_comments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    comments = db.query(Comment).offset(skip).limit(limit).all()
    return {"comments": comments}

@router.post("/comment", response_model=CommentBase)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    new_comment = Comment(**comment.dict())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment