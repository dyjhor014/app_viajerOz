from fastapi import FastAPI
from config.database import engine
from routers import groups_router, type_group_router, user_router
from fastapi.staticfiles import StaticFiles
#from models import type_group_model, group_model
from models.models import TypeGroup, Group, User

app = FastAPI()

#Routers
app.include_router(type_group_router.router)
app.include_router(groups_router.router)
app.include_router(user_router.router)


#StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def main():
    return {"message": "Bienvenido a la API Blog ViajerOz by: Dyjhor"}

# Create tables in Database
TypeGroup.metadata.create_all(bind=engine)
Group.metadata.create_all(bind=engine)
User.metadata.create_all(bind=engine)