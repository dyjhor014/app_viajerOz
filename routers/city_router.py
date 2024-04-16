from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.models import City, Post
from schemas.city import CityBase, CityCreate, CityList, CityUpdate, CitiesPost, map_post_to_postbase
from decorators.roles.role_verify import role_required
from auth.auth import get_token_from_request
from typing import List
from sqlalchemy import func

router = APIRouter()

@router.get("/city", response_model=CityList)
#@role_required(["admin"])
async def get_all_cities(token: str = Depends(get_token_from_request), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cities = db.query(City).offset(skip).limit(limit).all()
    return {"cities": cities}

@router.get("/city/find_by_name/{name}", response_model=CityList)
@role_required(["admin", "user", "moderator"])
async def get_all_cities(name: str, token: str = Depends(get_token_from_request), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cities = db.query(City).filter(City.name.like("%"+name+"%")).offset(skip).limit(limit).all()
    if  not cities: 
        raise HTTPException(status_code=404, detail="Not Found")
    return {"cities": cities}

@router.post("/city", response_model=CityBase)
async def create_city(city: CityCreate, db: Session = Depends(get_db)):
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

@router.get("/cities/most_visited", response_model=List[CitiesPost])
async def get_most_visited_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    city_stats = db.query(Post.city_destination, func.count(Post.city_destination)).group_by(Post.city_destination).all()

    sorted_cities = sorted(city_stats, key=lambda x: x[1], reverse=True)

    most_visited_cities = []

    for city_id, visit_count in sorted_cities[skip: skip + limit]:
        city_details = db.query(City).filter(City.id == city_id).first()
        city_posts = db.query(Post).filter(Post.city_destination == city_id).all()

        posts_base = [map_post_to_postbase(post) for post in city_posts]

        city_base = CitiesPost(
            id=city_details.id,
            name=city_details.name,
            description=city_details.description,
            department_id=city_details.department_id,
            status=city_details.status,
            created_at=city_details.created_at,
            posts=posts_base
        )

        most_visited_cities.append(city_base)

    return most_visited_cities