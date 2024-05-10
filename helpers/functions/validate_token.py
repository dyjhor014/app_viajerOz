import jwt
from fastapi import Depends, HTTPException
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from config.database import get_db
from models.models import User
from auth.auth import SECRET_KEY

# Función para verificar la vigencia de un token
def is_token_valid(token, db: Session):
    try:
        # Decodificar el token
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        # Obtener el tiempo de expiración del token
        expiration_time = decoded_token.get("exp")
        email = decoded_token.get("email")
        user = db.query(User).filter(User.email == email).first()
        if user.activation_token != token or user.activation_token is None:
            raise HTTPException(status_code=404, detail="El token no es valido")
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no existe")
        print(email)
        # Verificar si el tiempo de expiración es posterior al tiempo actual
        tiempo_actual = datetime.utcnow().timestamp()
        print(tiempo_actual)
        if expiration_time and expiration_time > tiempo_actual:
            user.is_active = 1
            user.activation_token = None
            db.commit()
            db.refresh(user)
            return True
    except jwt.ExpiredSignatureError:
        # El token ha expirado
        pass
    except jwt.InvalidTokenError:
        # El token es inválido por alguna razón
        pass
    return False