from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.models import Image
from schemas.image import ImageBase, ImageCreate, ImageList

router = APIRouter()

@router.get("/image", response_model=ImageList)
def get_all_images(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    images = db.query(Image).offset(skip).limit(limit).all()
    return {"images": images}

@router.post("/image", response_model=ImageBase)
def create_image(image: ImageCreate, db: Session = Depends(get_db)):
    new_image = Image(**image.dict())
    db.add(new_image)
    db.commit()
    db.refresh(new_image)
    return new_image