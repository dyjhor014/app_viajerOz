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

# Función para obtener el token de autorización del encabezado de la solicitud
def get_token_from_request(authorization: str = Header(...)):
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split("Bearer ")[1]
        return token
    raise HTTPException(status_code=401, detail="Credenciales de autenticación no proporcionadas")

# Función para decodificar el token JWT y obtener la información del usuario
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except PyJWTError as e:
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
    return encoded_jwt

# Funcion para crear un token de activación
def create_activation_token(email: str):
    # Definir los datos que se incluirán en el token (en este caso, solo el email)
    data = {"email": email}
    
    # Definir el tiempo de expiración del token (por ejemplo, 24 horas)
    expires_delta = timedelta(hours=24)
    
    # Generar el token con los datos y el tiempo de expiración
    activation_token = create_access_token(data, expires_delta)
    
    return activation_token

# Función para obtener el usuario desde el token de autorización del encabezado de la solicitud
def get_user_from_request(authorization: str = Header(...)):
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split("Bearer ")[1]
        payload = decode_token(token)  # Cambia esta línea
        if payload:
            user = payload.get("sub")
            if user:
                return user
    raise HTTPException(status_code=401, detail="Credenciales de autenticación no proporcionadas")
