from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import  JSONResponse
from sqlalchemy.orm import Session
from config.database import get_db
from models.models import LikeDislikePost, Post
from schemas.post import PostBase
from schemas.like_dislike_post import LikeDislikePostBase, LikeDislikePostCreate, LikeDislikePostList, LikeDislikePostUpdate

router = APIRouter()

@router.get("/like_dislike_post", response_model=LikeDislikePostList)
async def get_all_like_dislike_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    like_dislike_posts = db.query(LikeDislikePost).offset(skip).limit(limit).all()
    return {"like_dislike_posts": like_dislike_posts}

@router.post("/like_dislike_post", response_model=LikeDislikePostBase)
async def create_like_dislike_post(like_dislike_post: LikeDislikePostCreate, db: Session = Depends(get_db)):
    new_like_dislike_post = LikeDislikePost(**like_dislike_post.dict())
    db.add(new_like_dislike_post)
    db.commit()
    db.refresh(new_like_dislike_post)

    # Obtener el post asociado
    post = db.query(Post).filter_by(id=like_dislike_post.post_id).first()
    
    # Verificamos que exista
    if not post:
        raise HTTPException(status_code=404, detail="El post indicado no existe")
    
    # Actualizar los contadores de "like" o "dislike" en el post
    if like_dislike_post.action == "like":
        post.like += 1 
    elif like_dislike_post.action == "dislike":
        post.dislike += 1
    
    # Realizar actualización en la base de datos
    db.commit()
    
    return new_like_dislike_post

@router.patch("/like_dislike_post/update/{id}", response_model=LikeDislikePostUpdate, status_code=200)
async def update_like_dislike_post(id: int, like_dislike_post_data: LikeDislikePostUpdate ,db: Session = Depends(get_db)):
    existing_like_dislike_post = db.query(LikeDislikePost).filter_by(id=id).first()
    
    if existing_like_dislike_post is None:
        raise HTTPException(status_code=404, detail="Like/Dislike post not found")
    
    # Buscamos el post asociado
    post = db.query(Post).filter(Post.id == existing_like_dislike_post.post_id).first()
    
    if existing_like_dislike_post.action == like_dislike_post_data.action:
        if like_dislike_post_data.action == "like":
            post.like -= 1
        else:
            post.dislike -= 1
        db.delete(existing_like_dislike_post)
        db.commit()
        db.refresh(post)
        return JSONResponse(content={"message": f"{like_dislike_post_data.action} post successfully deleted"}, status_code=200)
    if existing_like_dislike_post.action != like_dislike_post_data.action:
        existing_like_dislike_post.action = like_dislike_post_data.action
        if like_dislike_post_data.action == "like":
            post.dislike -= 1
            post.like += 1
        else:
            post.like -= 1
            post.dislike += 1
        db.add(existing_like_dislike_post)
        db.commit()
        db.refresh(existing_like_dislike_post)
    return existing_like_dislike_post