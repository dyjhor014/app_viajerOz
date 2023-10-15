from fastapi import FastAPI
from config.database import engine
from routers import category_recomendation_router, category_router, city_router, comment_router, department_router, groups_router, image_router, like_dislike_comment_router, like_dislike_post_router, like_dislike_recomendation_router, post_router, recomendation_router, type_group_router, type_vehicle_router, user_router, vehicle_router, login_router
from fastapi.staticfiles import StaticFiles
from models.models import TypeGroup, Group, User, TypeVehicle, Vehicle, Category, Department, City, Post, Image, LikeDislikePost, Comment, LikeDislikeComment, CategoryRecomendation, Recomendation, LikeDislikeRecomendation
from auth.middleware_auth import custom_middleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Agrega el middleware de manejo de tokens JWT
app.middleware("http")(custom_middleware)

#Routers
app.include_router(type_group_router.router)
app.include_router(groups_router.router)
app.include_router(user_router.router)
app.include_router(type_vehicle_router.router)
app.include_router(vehicle_router.router)
app.include_router(category_router.router)
app.include_router(department_router.router)
app.include_router(city_router.router)
app.include_router(post_router.router)
app.include_router(image_router.router)
app.include_router(like_dislike_post_router.router)
app.include_router(comment_router.router)
app.include_router(like_dislike_comment_router.router)
app.include_router(category_recomendation_router.router)
app.include_router(recomendation_router.router)
app.include_router(like_dislike_recomendation_router.router)
app.include_router(login_router.router)

#StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def main():
    return {"message": "Bienvenido a la API Blog ViajerOz by: Dyjhor\nParece ser que todo funciona correctamente"}

# Create tables in Database
TypeGroup.metadata.create_all(bind=engine)
Group.metadata.create_all(bind=engine)
User.metadata.create_all(bind=engine)
TypeVehicle.metadata.create_all(bind=engine)
Vehicle.metadata.create_all(bind=engine)
Category.metadata.create_all(bind=engine)
Department.metadata.create_all(bind=engine)
City.metadata.create_all(bind=engine)
Post.metadata.create_all(bind=engine)
Image.metadata.create_all(bind=engine)
LikeDislikePost.metadata.create_all(bind=engine)
Comment.metadata.create_all(bind=engine)
LikeDislikeComment.metadata.create_all(bind=engine)
CategoryRecomendation.metadata.create_all(bind=engine)
Recomendation.metadata.create_all(bind=engine)
LikeDislikeRecomendation.metadata.create_all(bind=engine)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)