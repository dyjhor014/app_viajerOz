from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.models import CategoryRecomendation, User, Group
from schemas.category_recomendation import CategoryRecomendationBase, CategoryRecomendationCreate, CategoryRecomendationList
from auth.auth import get_user_from_request
from helpers.functions.delete_record import check_user_permissions, delete_record, deactivate_record, get_record_by_id

router = APIRouter()

@router.get("/category_recomendation", response_model=CategoryRecomendationList,
            summary="Obtener lista de categorías de recomendación",
            description="Obtiene una lista de todas las categorías de recomendación disponibles.",
            response_description="Lista de categorías de recomendación")
async def get_all_category_recomendations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtén una lista de categorías de recomendación.

    Parámetros:
    - skip: La cantidad de elementos para omitir.
    - limit: El número máximo de elementos a devolver.

    Respuesta:
    - 200 OK: Devuelve una lista de categorías de recomendación.
    """
    category_recomendations = db.query(CategoryRecomendation).offset(skip).limit(limit).all()
    return {"category_recomendations": category_recomendations}

@router.post("/category_recomendation", response_model=CategoryRecomendationBase,
             summary="Crear una nueva categoría de recomendación",
             description="Crea una nueva categoría de recomendación.",
             response_description="Nueva categoría de recomendación creada")
async def create_category_recomendations(category_recomendation: CategoryRecomendationCreate, db: Session = Depends(get_db)):
    new_category_recomendations = CategoryRecomendation(**category_recomendation.model_dump())
    db.add(new_category_recomendations)
    db.commit()
    db.refresh(new_category_recomendations)
    return new_category_recomendations

@router.patch("/category_recomendation/update/{id}", response_model=CategoryRecomendationCreate,
              summary="Actualizar una categoría de recomendación existente",
              description="Actualiza una categoría de recomendación existente.",
              response_description="Categoría de recomendación actualizada")
async def update_category_recomendation(id: int, category_recomendation_data: CategoryRecomendationCreate, db: Session = Depends(get_db)):
    existing_category_recomendation = db.query(CategoryRecomendation).filter(CategoryRecomendation.id == id).first()
    
    if not existing_category_recomendation:
        raise HTTPException(status_code=404, detail="La categoría de recomendación no existe")
    
    for key, value in category_recomendation_data.model_dump().items():
        setattr(existing_category_recomendation, key, value)
    db.commit()
    db.refresh(existing_category_recomendation)
    
    return existing_category_recomendation

@router.delete("/category_recomendation/delete/{id}")
async def delete_category_recomendation(id: int, user: str = Depends(get_user_from_request), db: Session = Depends(get_db)):
        
    category_recomendation = get_record_by_id(CategoryRecomendation, id, db)
    
    if not category_recomendation:
        raise HTTPException(status_code=404, detail="La categoría de recomendación no existe")
    
    if category_recomendation.status == 0:
        raise HTTPException(status_code=404, detail="El registro se encuentra de baja o no existe")
    
    # Verifica si el usuario es admin o moderator
    role = check_user_permissions(user, db)
    
    if role == 'admin':
        response = delete_record(category_recomendation, db, id)
        return response
    elif role == 'moderator':
        response = deactivate_record(category_recomendation, db, id)
        return response