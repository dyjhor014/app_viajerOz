from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.models import TypeGroup
from schemas.type_group import TypeGroupList, TypeGroupCreate, TypeGroupBase

router = APIRouter()

@router.get("/type_group", response_model=TypeGroupList)
def get_all_type_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    type_groups = db.query(TypeGroup).offset(skip).limit(limit).all()
    return {"type_groups": type_groups}

@router.post("/type_group", response_model=TypeGroupBase)
def create_type_group(type_group: TypeGroupCreate, db: Session = Depends(get_db)):
    new_type_group = TypeGroup(**type_group.dict())
    db.add(new_type_group)
    db.commit()
    db.refresh(new_type_group)
    return new_type_group

@router.patch("/type_group/{type_group_id}", response_model=TypeGroupBase)
def update_type_group(type_group_id: int, type_group_data: TypeGroupCreate, db: Session = Depends(get_db)):
    existing_type_group = db.query(TypeGroup).filter(TypeGroup.id == type_group_id).first()
    
    if not existing_type_group:
        raise HTTPException(status_code=404, detail="TypeGroup not found")
    
    for field, value in type_group_data.dict().items():
        setattr(existing_type_group, field, value)
    
    db.commit()
    db.refresh(existing_type_group)
    
    return existing_type_group


