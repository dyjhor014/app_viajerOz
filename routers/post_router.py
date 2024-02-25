from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from config.database import get_db
from models.models import Post, User
from schemas.post import PostBase, PostCreate, PostList, PostUpdate
from auth.auth import get_token_from_request
from decorators.roles.role_verify import role_required

router = APIRouter()

@router.get("/post", response_model=PostList)
@role_required(["admin", "user", "moderator"])
async def get_all_posts(token: str = Depends(get_token_from_request), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = db.query(Post).offset(skip).limit(limit).all()
    return {"posts": posts}

@router.get("/post/find_for_user/{id}")
@role_required(["admin", "user", "moderator"])
async def get_all_posts(id: int, token: str = Depends(get_token_from_request), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = db.query(Post).filter(Post.user_id == id).order_by(desc(Post.like)).offset(skip).limit(limit).all()
    if not posts: 
        raise HTTPException(status_code=404, detail="User  has no posts")
    # Mapear los objetos User a diccionarios
    posts_data = []
    for post in posts:
        post_data = {
            "id": post.id,
            "category_id": post.category_id,
            "title": post.title,
            "date": post.date,
            "brief": post.brief,
            "content": post.content,
            "city_origin": post.city_origin,
            "city_destination": post.city_destination,
        }
        posts_data.append(post_data)
    return {"posts": posts_data}

@router.post("/post", response_model=PostBase)
@role_required(["admin", "user", "moderator"])
async def create_post(post: PostCreate, token: str = Depends(get_token_from_request), db: Session = Depends(get_db)):
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
@role_required(["admin", "user", "moderator"])
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