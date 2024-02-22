# auth/middleware_auth.py
import jwt
from fastapi import Request, HTTPException, Response
from jwt import PyJWTError
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST
from auth.auth import SECRET_KEY, ALGORITHM

async def get_current_user(request: Request):
    # Obtiene el usuario del estado de la solicitud
    user = getattr(request.state, "user", None)
    return user

async def custom_middleware(request: Request, call_next):
    # Obtener la ruta de la solicitud
    path = request.url.path

    # Verificar si la ruta es /docs, /redoc o /openapi.json y no aplicar autenticación en esos casos
    if path.startswith("/docs") or path.startswith("/redoc") or path.startswith("/openapi.json") or path.startswith("/login") or path.startswith("/user"):
        response = await call_next(request)
        return response

    try:
        authorization = request.headers.get('Authorization')
        if not authorization or not authorization.startswith("Bearer "):
            # Retorna una respuesta 401 en lugar de lanzar una excepción.
            return Response(content="No se proporciono autorizacion", status_code=HTTP_401_UNAUTHORIZED)
        
        token = authorization.split("Bearer ")[1]

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = payload.get("sub")
        if user is None:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Token JWT no válido.")
        
        request.state.user = user
    except (PyJWTError, ValueError):
        return Response(content="Token incorrecto", status_code=HTTP_400_BAD_REQUEST)
    
    response = await call_next(request)
    return response