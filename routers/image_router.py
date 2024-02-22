from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.models import Image
from schemas.image import ImageBase, ImageCreate, ImageList, ImageUpdate

router = APIRouter()

@router.get("/image", response_model=ImageList)
async def get_all_images(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    images = db.query(Image).offset(skip).limit(limit).all()
    return {"images": images}

@router.post("/image", response_model=ImageBase)
async def create_image(image: ImageCreate, db: Session = Depends(get_db)):
    new_image = Image(**image.model_dump())
    db.add(new_image)
    db.commit()
    db.refresh(new_image)
    return new_image

@router.patch("/image/update/{image_id}", response_model=ImageUpdate)
async def update_image(image_id: int, image_data: ImageUpdate, db: Session = Depends(get_db)):
    existing_image = db.query(Image).filter(Image.id == image_id).first()
    
    if not existing_image:
        raise HTTPException(status_code=404, detail="No se encontró la imagen")
    for key, value in image_data.model_dump().items():
        setattr(existing_image, key, value)
        
    db.commit()
    db.refresh(existing_image)
    
    return existing_image