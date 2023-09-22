from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.models import Post, User
from schemas.post import PostBase, PostCreate, PostList

router = APIRouter()

@router.get("/post", response_model=PostList)
def get_all_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = db.query(Post).offset(skip).limit(limit).all()
    return {"posts": posts}

@router.post("/post", response_model=PostBase)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    new_post = Post(**post.dict())
    
    # Obtenemos el usuario referencia
    user = db.query(User).filter_by(id = post.user_id).first()
    
    # Validamos que exista el user
    if not user:
        raise HTTPException(status_code=404, detail="El usuario no existe")
    
    # Agregamos el contador
    user.routes += 1
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post