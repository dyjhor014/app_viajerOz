import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session
from config.database import get_db
from models.models import User, Post, Group
from schemas.user import UserCreate, UserList
from auth.auth import get_token_from_request, get_user_from_request
from decorators.roles.role_verify import role_required
from helpers.qr.qr_generate import generate_qr_code
from schemas.post import PostBase

router = APIRouter()

@router.get("/user", response_model=UserList)
@role_required(["admin", "user", "moderator"])
async def get_all_users(token: str = Depends(get_token_from_request), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return {"users": users}

@router.get("/user/find/{id}")
@role_required(["admin", "user", "moderator"])
async def get_user_for_id(id: int, token: str = Depends(get_token_from_request), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="No user found")
    
    user_data = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "user": user.user,
        "group_id": user.group_id,
        "routes": user.routes,
    }
    return user_data

@router.get("/user/me")
async def get_current_user_data(user: str = Depends(get_user_from_request), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user == user).first()
    print(f"El usuario es {user}")
    #Generamos la ruta dinamica para crear el codigo QR
    text = f"http://127.0.0.1:8000/user/find/{user.id}"
    folder_path = f"static/images/user/{user.id}/"  # Ruta a la carpeta donde deseas guardar el archivo
    file_name = "codigo_qr.png"  # Nombre del archivo
    file_path = generate_qr_code(text, folder_path, file_name)
    
    user_data = {
        "name": user.name,
        "email": user.email,
        "user": user.user,
        "group_id": user.group_id,
        "routes": user.routes,
        "qr_code": file_path
    }
    return user_data
    

@router.get("/user/most_popular")
async def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).filter(User.routes >= 1).order_by(desc(User.routes)).offset(skip).limit(limit).all()
    if not users: 
        raise HTTPException(status_code=404, detail="No popular users found")
    
    users_data = []
    for user in users:
        # Consulta para obtener las publicaciones asociadas a este usuario
        user_posts = db.query(Post).filter(Post.user_id == user.id).all()
        
        # Obtener el nombre del grupo del usuario si tiene grupo asignado
        group_name = user.group.name if user.group else None

        posts_base = [PostBase(
            id=post.id,
            title=post.title,
            date=post.date,
            brief=post.brief,
            content=post.content,
            city_origin=post.city_origin,
            city_destination=post.city_destination,
            like=post.like,
            dislike=post.dislike,
            comments=post.comments,
            status=post.status,
            created_at=post.created_at,
            user_id=post.user_id,
            category_id=post.category_id
        ).model_dump() for post in user_posts]

        user_data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "user": user.user,
            "group_id": user.group_id,
            "group": group_name,
            "routes": user.routes,
            "status": user.status,
            "created_at": user.created_at,
            "posts": posts_base
        }
        users_data.append(user_data)

    return {"users": users_data}


@router.post("/user/register", response_model=UserCreate)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Validamos que no exista registrado el mismo email
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail=f"Email {existing_email.email} already registered")
    # Validamos que no exista registrado el mismo usuario
    existing_user = db.query(User).filter(User.user == user.user).first()
    if existing_user:
        raise HTTPException(status_code=400, detail=f"Username {existing_user.user} already in use")
    # Obtener la contraseña sin hashear desde el objeto UserCreate
    password = user.password.encode('utf-8')  # Codifica la contraseña a bytes
    
    # Hashea la contraseña
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    
    # Crea un nuevo objeto User con la contraseña hasheada
    new_user = User(**user.model_dump())
    
    # Asigna la contraseña hasheada al campo password
    new_user.password = hashed_password.decode('utf-8')
    
    # Agrega el nuevo usuario a la base de datos
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user