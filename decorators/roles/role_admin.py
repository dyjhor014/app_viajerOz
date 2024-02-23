# Decorador para verificar si el usuario es administrador
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import SessionLocal
from models.models import User
from auth.auth import decode_token, get_token_from_request
from functools import wraps

def admin_required(func):
    @wraps(func)
    async def wrapper(*args, token: str = Depends(get_token_from_request), db: Session = Depends(SessionLocal), **kwargs):
        try:
            # Decodificar el token para obtener el identificador del usuario
            payload = decode_token(token)
            if not payload:
                raise HTTPException(status_code=401, detail="Token de acceso inválido")
            
            # Obtener el identificador del usuario del payload
            user = payload.get("sub")
            if not user:
                raise HTTPException(status_code=401, detail="Identificador de usuario no encontrado en el token")
            
            # Consultar la base de datos para obtener el objeto User correspondiente
            username = db.query(User).filter(User.user == user).first()
            # Obtener el rol del usuario
            role = username.role
            
            # Imprimir el usuario y su rol
            print("Usuario:", username.user)
            print("Rol:", role)
            if not username:
                raise HTTPException(status_code=404, detail="Usuario no encontrado en la base de datos")
            
            # Verificar si el usuario es administrador
            if role != "admin":
                print("El usuario no es admin")
                raise HTTPException(status_code=403, detail="Permiso denegado, necesitas ser admin para tener acceso.")
            # Ejecutar la función original del endpoint
            return await func(*args, db=db, **kwargs)
        except Exception as e:
            print("Excepción:", e)
            raise
        finally:
            db.close()
    
    return wrapper