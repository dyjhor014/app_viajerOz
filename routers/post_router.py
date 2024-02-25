from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.models import Post, User
from schemas.post import PostBase, PostCreate, PostList, PostUpdate
from auth.auth import get_token_from_request
from decorators.roles.role_verify import role_required

router = APIRouter()

@router.get("/post", response_model=PostList)
@role_required(["admin", "user"])
async def get_all_posts(token: str = Depends(get_token_from_request), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = db.query(Post).offset(skip).limit(limit).all()
    return {"posts": posts}

@router.post("/post", response_model=PostBase)
async def create_post(post: PostCreate, db: Session = Depends(get_db)):
    new_post = Post(**post.model_dump())
    
    # Obtenemos el usuario referencia
    user = db.query(User).filter_by(id=post.user_id).first()
    
    # Validamos que exista el usuario
    if not user:
        raise HTTPException(status_code=404, detail="El usuario no existe")
    
    # Agregamos el contador
    user.routes += 1
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

@router.patch("/post/update/{post_id}", response_model=PostUpdate)
async def update_post(post_id: int, post_data: PostUpdate, db: Session = Depends(get_db)):
    existing_post = db.query(Post).filter(Post.id == post_id).first()
    
    # Validamos que exista el post
    if  not existing_post:
        raise HTTPException(status_code=404, detail="No se encontró el post")
    for key, value in post_data.model_dump().items():
        setattr(existing_post, key, value)
    db.commit()
    db.refresh(existing_post)
    
    return existing_post