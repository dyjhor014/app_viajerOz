from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import  JSONResponse
from sqlalchemy.orm import Session
from config.database import get_db
from models.models import LikeDislikeRecomendation, Recomendation
from schemas.like_dislike_recomendation import LikeDislikeRecomendationBase, LikeDislikeRecomendationCreate, LikeDislikeRecomendationList, LikeDislikeRecomendationUpdate

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

@router.patch("/like_dislike_recomendation/update/{id}", response_model=LikeDislikeRecomendationUpdate)
async def update_like_dislike_recomendation(id: int, like_dislike_recomendation_data: LikeDislikeRecomendationUpdate, db: Session = Depends(get_db)):
    existing_like_dislike_recomendation = db.query(LikeDislikeRecomendation).filter(LikeDislikeRecomendation.id==id).first()

    if not existing_like_dislike_recomendation:
        raise HTTPException(status_code=404, detail="Like/Dislike recomendation not found")
    
    # Buscamos la recomendacion
    recomendation = db.query(Recomendation).filter(Recomendation.id == existing_like_dislike_recomendation.recomendation_id).first()
    
    if existing_like_dislike_recomendation.action == like_dislike_recomendation_data.action:
        if like_dislike_recomendation_data.action == "like":
            recomendation.like -= 1
        else:
            recomendation.dislike -= 1
        db.delete(existing_like_dislike_recomendation)
        db.commit()
        db.refresh(recomendation)
        return JSONResponse(content={"message" : f"{like_dislike_recomendation_data.action} recomendation successfully deleted"}, status_code=200)
    if existing_like_dislike_recomendation.action != like_dislike_recomendation_data.action:
        existing_like_dislike_recomendation.action = like_dislike_recomendation_data.action
        if like_dislike_recomendation_data.action == "like":
            recomendation.dislike -= 1
            recomendation.like += 1
        else:
            recomendation.like -= 1
            recomendation.dislike += 1
        db.add(existing_like_dislike_recomendation)
        db.commit()
        db.refresh(existing_like_dislike_recomendation)
    
    return existing_like_dislike_recomendation