from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.models import City
from schemas.city import CityBase, CityCreate, CityList

router = APIRouter()

@router.get("/city", response_model=CityList)
def get_all_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cities = db.query(City).offset(skip).limit(limit).all()
    return {"cities": cities}

@router.post("/city", response_model=CityBase)
def create_city(city: CityCreate, db: Session = Depends(get_db)):
    new_city = City(**city.dict())
    db.add(new_city)
    db.commit()
    db.refresh(new_city)
    return new_city