from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.models import Category
from schemas.category import CategoryBase, CategoryCreate, CategoryList, CategoryUpdate

router = APIRouter()

@router.get("/category", response_model=CategoryList)
def get_all_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = db.query(Category).offset(skip).limit(limit).all()
    return {"categories": categories}

@router.post("/category", response_model=CategoryBase)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    new_category = Category(**category.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.patch("/category/update/{category_id}", response_model=CategoryUpdate)
async def  update_category(category_id: int, category_data: CategoryUpdate, db: Session = Depends(get_db)):
    existing_category = db.query(Category).filter(Category.id == category_id).first()
    if not existing_category:
        raise HTTPException(status_code=404, detail="Category not found")
    if category_data.name and  category_data.description is not None:
        for field, value in category_data.model_dump().items():
            setattr(existing_category, field, value) 
        db.commit()
        db.refresh(existing_category)
        
        return existing_category
    else:
        raise HTTPException(status_code=422, detail={"error":"At least one of the fields must be provided."})
