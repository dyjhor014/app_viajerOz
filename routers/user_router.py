import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.models import User
from schemas.user import UserBase, UserCreate, UserList

router = APIRouter()

@router.get("/user", response_model=UserList)
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return {"users": users}

@router.post("/user", response_model=UserBase)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Obtener la contraseña sin hashear desde el objeto UserCreate
    password = user.password.encode('utf-8')  # Codifica la contraseña a bytes
    
    # Hashea la contraseña
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    
    # Crea un nuevo objeto User con la contraseña hasheada
    new_user = User(**user.dict())
    
    # Asigna la contraseña hasheada al campo password
    new_user.password = hashed_password.decode('utf-8')
    
    # Agrega el nuevo usuario a la base de datos
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

