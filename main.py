from fastapi import FastAPI
from routers import products, posts, groups, users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#Routers
app.include_router(products.router)
app.include_router(posts.router)
app.include_router(groups.router)
app.include_router(users.router)

#StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def main():
    return {"message": "Hello World"}
