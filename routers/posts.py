from fastapi import APIRouter

router = APIRouter(prefix="/posts",
                   tags=["Posts"],
                   responses={404: {"message": "No se ha encontrado"}})

posts_list = [{"id": 1, "user_id":1, "category_id": 1, "title": "Mi primer viaje", "brief": "El primer viaje al interior del pais", "content": "asjdasjdsajsadjdasjkdasjkdjkjdkdjaskdkjasdjkasjdaskdjaskdjaskdjask", "city_origin":"Lima", "city_destination": "Oxapampa", "status": 1, "created_at":"25/03/2023", "like":20, "dislike":2}]

@router.get("/")
async def posts():
    return posts_list