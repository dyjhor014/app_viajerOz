from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.models import Vehicle
from schemas.vehicle import VehicleBase, VehicleCreate, VehicleList

router = APIRouter()

@router.get("/vehicle", response_model=VehicleList)
def get_all_vehicles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    vehicles = db.query(Vehicle).offset(skip).limit(limit).all()
    return {"vehicles": vehicles}

@router.post("/vehicle", response_model=VehicleBase)
def create_vehicle(type_group: VehicleCreate, db: Session = Depends(get_db)):
    new_vehicle = Vehicle(**type_group.dict())
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    return new_vehicle