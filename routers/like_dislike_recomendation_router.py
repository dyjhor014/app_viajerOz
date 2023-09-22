from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.models import LikeDislikeRecomendation, Recomendation
from schemas.like_dislike_recomendation import LikeDislikeRecomendationBase, LikeDislikeRecomendationCreate, LikeDislikeRecomendationList

router = APIRouter()

@router.get("/like_dislike_recomendation", response_model=LikeDislikeRecomendationList)
def get_all_like_dislike_recomendations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    like_dislike_recomendations = db.query(LikeDislikeRecomendation).offset(skip).limit(limit).all()
    return {"like_dislike_recomendations": like_dislike_recomendations}

@router.post("/like_dislike_recomendation", response_model=LikeDislikeRecomendationBase)
def create_like_dislike_recomendation(like_dislike_recomendation: LikeDislikeRecomendationCreate, db: Session = Depends(get_db)):
    # Crear una nueva entrada en la tabla LikeDislikeRecomendation
    new_like_dislike_recomendation = LikeDislikeRecomendation(**like_dislike_recomendation.dict())
    db.add(new_like_dislike_recomendation)
    db.commit()
    db.refresh(new_like_dislike_recomendation)
    
    # Obtener la recomendación asociada
    recomendation = db.query(Recomendation).filter_by(id=like_dislike_recomendation.recomendation_id).first()
    
    # Verificamos que exista
    if not recomendation:
        raise HTTPException(status_code=404, detail="La recomendación asociada no existe")
    
    # Actualizar los contadores de "like" o "dislike" en la recomendación
    if like_dislike_recomendation.action == "like":
        recomendation.like += 1
    elif like_dislike_recomendation.action == "dislike":
        recomendation.dislike += 1
    
    # Realizar la actualización en la base de datos
    db.commit()
    
    return new_like_dislike_recomendation