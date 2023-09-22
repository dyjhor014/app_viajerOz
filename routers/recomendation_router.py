from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.models import Recomendation, Post
from schemas.recomendation import RecomendationBase, RecomendationCreate, RecomendationList

router = APIRouter()

@router.get("/recomendation", response_model=RecomendationList)
def get_all_recomendations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    recomendations = db.query(Recomendation).offset(skip).limit(limit).all()
    return {"recomendations": recomendations}

@router.post("/recomendation", response_model=RecomendationBase)
def create_recomendation(recomendation: RecomendationCreate, db: Session = Depends(get_db)):
    # Obtener el post asociado a la recomendación
    post = db.query(Post).filter_by(id=recomendation.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="El post asociado no existe")
    # Obtener las ciudades de origen y destino del post
    origin_city_id = post.city_origin
    destination_city_id = post.city_destination

    # Verificar si el city_id proporcionado está en las ciudades de origen o destino del post
    if recomendation.city_id not in [origin_city_id, destination_city_id]:
        raise HTTPException(status_code=400, detail="El city_id proporcionado no esta en ciudad origen o ciudad destino")

    # Crear la recomendación
    new_recomendation = Recomendation(**recomendation.dict())
    db.add(new_recomendation)
    db.commit()
    db.refresh(new_recomendation)

    return new_recomendation
