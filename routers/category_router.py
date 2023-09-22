from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.models import Category
from schemas.category import CategoryBase, CategoryCreate, CategoryList

router = APIRouter()

@router.get("/category", response_model=CategoryList)
def get_all_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = db.query(Category).offset(skip).limit(limit).all()
    return {"categories": categories}

@router.post("/category", response_model=CategoryBase)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    new_category = Category(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category