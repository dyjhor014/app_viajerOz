import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session
from config.database import get_db
from models.models import User
from schemas.user import UserCreate, UserList
from auth.auth import get_token_from_request
from decorators.roles.role_verify import role_required

router = APIRouter()

@router.get("/user", response_model=UserList)
@role_required(["admin", "user", "moderator"])
async def get_all_users(token: str = Depends(get_token_from_request), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return {"users": users}

@router.get("/user/most_popular")
@role_required(["admin", "user", "moderator"])
async def get_all_users(token: str = Depends(get_token_from_request), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).filter(User.routes >= 1).order_by(desc(User.routes)).offset(skip).limit(limit).all()
    if not users: 
        raise HTTPException(status_code=404, detail="No popular users found")
    
    # Mapear los objetos User a diccionarios
    users_data = []
    for user in users:
        user_data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "user": user.user,
            "group_id": user.group_id,
            "routes": user.routes,
            "status": user.status,
            "created_at": user.created_at,
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