from fastapi import FastAPI
from config.database import engine
from routers import type_group
from models.type_group import TypeGroup
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#Routers
app.include_router(type_group.router)


#StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def main():
    return {"message": "Hello World"}

# Crea las tablas en la base de datos
from models.type_group import TypeGroup
TypeGroup.metadata.create_all(bind=engine)