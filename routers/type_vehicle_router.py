from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.models import TypeVehicle
from schemas.type_vehicle import TypeVehicleBase, TypeVehicleCreate, TypeVehicleList

router = APIRouter()

@router.get("/type_vehicle", response_model=TypeVehicleList)
def get_all_type_vehicles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    type_vehicles = db.query(TypeVehicle).offset(skip).limit(limit).all()
    return {"type_vehicles": type_vehicles}

@router.post("/type_vehicle", response_model=TypeVehicleBase)
def create_type_vehicle(type_group: TypeVehicleCreate, db: Session = Depends(get_db)):
    new_type_vehicle = TypeVehicle(**type_group.dict())
    db.add(new_type_vehicle)
    db.commit()
    db.refresh(new_type_vehicle)
    return new_type_vehicle


