from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.models import CategoryRecomendation
from schemas.category_recomendation import CategoryRecomendationBase, CategoryRecomendationCreate, CategoryRecomendationList

router = APIRouter()

@router.get("/category_recomendation", response_model=CategoryRecomendationList)
def get_all_category_recomendations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    category_recomendations = db.query(CategoryRecomendation).offset(skip).limit(limit).all()
    return {"category_recomendations": category_recomendations}

@router.post("/category_recomendation", response_model=CategoryRecomendationBase)
def create_category_recomendations(category_recomendation: CategoryRecomendationCreate, db: Session = Depends(get_db)):
    new_category_recomendations = CategoryRecomendation(**category_recomendation.dict())
    db.add(new_category_recomendations)
    db.commit()
    db.refresh(new_category_recomendations)
    return new_category_recomendations