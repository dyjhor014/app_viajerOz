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


