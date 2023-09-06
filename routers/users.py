from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# entidad user

class User(BaseModel):
    id: int
    name: str
    email: str
    usuario: str
    password: str
    foto: str
    rol: int
    grupo: str
    fecha_alta: str

users_list = [User(id= 1, name= "Jordy Cruz", email= "jordycs93@gmail.com", usuario = "dyjhor", password = "*********", foto = "/img/perfil.jpg", rol = "1", grupo = "Satan's Kings", fecha_alta = "25/03/2023"),
              User(id= 2, name= "Aris Agui", email= "arisagui@gmail.com", usuario = "aris", password = "*********", foto = "/img/perfil2.jpg", rol = "1", grupo = "Satan's Kings", fecha_alta = "25/03/2023")]

@router.get("/usersjson")
async def usersjson():
    return [{"name": "Jordy Cruz", "email": "jordycs93@gmail.com", "usuario": "dyjhor", "password": "*********", "foto": "/img/perfil.jpg", "rol": "1", "grupo": "Satan's Kings", "fecha_alta": "25/03/2023"}, 
            {"name": "Aris Agui", "email": "arisagui@gmail.com", "usuario": "aris", "password": "*********", "foto": "/img/perfil1.jpg", "rol": "1", "grupo": "Satan's Kings", "fecha_alta": "25/03/2023"}]

@router.get("/users")
async def users():
    return users_list

@router.get("/user/{id}")
async def user(id:int):
    return search_user(id)

@router.post("/user/")
async def user(user:User):
    if type(search_user(user.id)) == User:
        return {"error" : "usuario ya existe"}
    else:
        users_list.append(user)

@router.delete("/user/{id}")
async def user(id:int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
            return {"message" : f"Se ha eliminado el usuario id {id}"}
    if not found:
        return {"error" : "No se ha eliminado el usuario"}

# función para buscar user
def search_user(id:int):
    users = filter(lambda user:user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error" : "Usuario no encontrado"}
        