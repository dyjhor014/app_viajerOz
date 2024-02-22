from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.models import Comment
from schemas.comment import CommentBase, CommentCreate, CommentList, CommentUpdate

router = APIRouter()

@router.get("/comment", response_model=CommentList)
async def get_all_comments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    comments = db.query(Comment).offset(skip).limit(limit).all()
    return {"comments": comments}

@router.post("/comment", response_model=CommentBase)
async def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    new_comment = Comment(**comment.model_dump())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.patch("/comment/update/{comment_id}", response_model=CommentUpdate)
async def  update_comment(comment_id: int, comment_data: CommentUpdate, db: Session = Depends(get_db)):
    existing_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    
    if not existing_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
        
    for key, value in comment_data.model_dump().items():
        setattr(existing_comment, key, value)
            
    db.commit()
    db.refresh(existing_comment)
    return existing_comment