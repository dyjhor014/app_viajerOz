import jwt
from fastapi import Depends
from datetime import datetime, timedelta
from decouple import config

# Clave secreta para firmar el token
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300000 #Tiempo de expiracion del token

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