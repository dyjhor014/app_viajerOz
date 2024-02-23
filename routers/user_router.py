import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.models import User
from schemas.user import UserCreate, UserList
from auth.auth import get_token_from_request
from decorators.roles.role_admin import admin_required

router = APIRouter()

# Endpoint protegido que requiere que el usuario sea administrador / Endpoint de prueba
@router.get("/protected_endpoint")
@admin_required
async def protected_endpoint(token: str = Depends(get_token_from_request), db: Session = Depends(get_db)):
    return {"message": "Bienvenido tienes permiso por ser administrador."}

@router.get("/user", response_model=UserList)
@admin_required
async def get_all_users(token: str = Depends(get_token_from_request), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return {"users": users}

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