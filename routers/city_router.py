from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.models import City
from schemas.city import CityBase, CityCreate, CityList, CityUpdate

router = APIRouter()

@router.get("/city", response_model=CityList)
def get_all_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cities = db.query(City).offset(skip).limit(limit).all()
    return {"cities": cities}

@router.post("/city", response_model=CityBase)
def create_city(city: CityCreate, db: Session = Depends(get_db)):
    new_city = City(**city.model_dump())
    db.add(new_city)
    db.commit()
    db.refresh(new_city)
    return new_city

@router.patch("/city/update/{city_id}", response_model=CityUpdate)
async def update_city(city_id: int, city_data: CityUpdate, db: Session = Depends(get_db)):
    existing_city = db.query(City).filter(City.id == city_id).first()
    
    if not existing_city:
        raise HTTPException(status_code=404, detail="City not found")
    
    for field, value in city_data.model_dump().items():
        setattr(existing_city, field, value)
    
    db.commit()
    db.refresh(existing_city)
    
    return existing_city