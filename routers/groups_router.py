from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.models import Group
from schemas.group_ import GroupBase, GroupCreate, GroupList

router = APIRouter()

@router.get("/group", response_model=GroupList)
def get_all_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    groups = db.query(Group).offset(skip).limit(limit).all()
    return {"groups": groups}

@router.post("/group", response_model=GroupBase)
def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    new_group = Group(**group.dict())
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group

@router.patch("/group/{group_id}",response_model=GroupBase)
async def update_group(group_id: int, group_data: GroupCreate, db: Session = Depends(get_db)):
    existing_group = db.query(Group).filter(Group.id == group_id).first()
    
    if not existing_group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    for field, value in group_data.dict().items():
        setattr(existing_group, field, value)
    
    db.commit()
    db.refresh(existing_group)
    
    return existing_group