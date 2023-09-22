from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.models import LikeDislikeComment, Comment
from schemas.like_dislike_comment import LikeDislikeCommentBase, LikeDislikeCommentCreate, LikeDislikeCommentList

router = APIRouter()

@router.get("/like_dislike_comment", response_model=LikeDislikeCommentList)
def get_all_like_dislike_comments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    like_dislike_comments = db.query(LikeDislikeComment).offset(skip).limit(limit).all()
    return {"like_dislike_comments": like_dislike_comments}

@router.post("/like_dislike_comment", response_model=LikeDislikeCommentBase)
def create_like_dislike_comment(like_dislike_comment: LikeDislikeCommentCreate, db: Session = Depends(get_db)):
    new_like_dislike_comment = LikeDislikeComment(**like_dislike_comment.dict())
    db.add(new_like_dislike_comment)
    db.commit()
    db.refresh(new_like_dislike_comment)
    
    # Obtenemos el comentario asociado
    comment = db.query(Comment).filter_by(id=like_dislike_comment.comment_id).first()
    
    # Validamos que exista
    if not comment:
        raise HTTPException(status_code=404, detail="El comentario no existe")
    
    # Actualizamos los contadores
    if like_dislike_comment.action == "like":
        comment.like += 1
    elif like_dislike_comment.action == "dislike":
        comment.like += 1
        
    # Actualizamos la base de datos
    db.commit()
    
    return new_like_dislike_comment