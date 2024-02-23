import jwt
from fastapi import Depends, HTTPException, Header
from datetime import datetime, timedelta
from decouple import config
from jwt import PyJWTError

# Clave secreta para firmar el token
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300000 #Tiempo de expiracion del token

from fastapi import Header

def get_token_from_request(authorization: str = Header(...)):
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split("Bearer ")[1]
        print("Token recibido:", token)  # Agregar esta línea para imprimir el token
        return token
    return None


# Función para decodificar el token JWT y obtener la información del usuario
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except PyJWTError:
        return None

# Funcion para crear un token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(encoded_jwt+" este es el token")
    return encoded_jwt