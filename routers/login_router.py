from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from config.database import get_db
from schemas.user import UserResponseToken
from models.models import User
from auth.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

router = APIRouter()

# Define una dependencia para obtener el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/login", response_model=UserResponseToken)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(user=form_data.username).first()
    if user.is_active == 0:
        raise HTTPException(status_code=400, detail="Su cuenta no está activada, debe activarla desde su correo electrónico")
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/secure-data")
async def get_secure_data(token: str = Depends(oauth2_scheme)):
    # Esta ruta solo será accesible si se proporciona un token válido
    # Coloca aquí la lógica para manejar la solicitud segura
    return {"message": "Datos seguros accesibles"}

# Otras rutas y lógica de la aplicación

