from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.models import Vehicle
from schemas.vehicle import VehicleBase, VehicleCreate, VehicleList, VehicleUpdate

router = APIRouter()

@router.get("/vehicle", response_model=VehicleList)
def get_all_vehicles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    vehicles = db.query(Vehicle).offset(skip).limit(limit).all()
    return {"vehicles": vehicles}

@router.post("/vehicle", response_model=VehicleBase)
def create_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    new_vehicle = Vehicle(**vehicle.model_dump())
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    return new_vehicle

@router.patch("/vehicle/update/{vehicle_id}", response_model=VehicleUpdate)
async def update_vehicle(vehicle_id: int, vehicle_data: VehicleUpdate, db: Session = Depends(get_db)):
    existing_vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    
    if not existing_vehicle:
        raise HTTPException(status_code=404, detail="vehicle not found")
    
    for field, value in vehicle_data.model_dump().items():
        setattr(existing_vehicle, field, value)
    
    db.commit()
    db.refresh(existing_vehicle)
    
    return existing_vehicle