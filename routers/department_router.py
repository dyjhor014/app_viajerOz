from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.models import Department
from schemas.department import DepartmentBase, DepartmentCreate, DepartmentList, DepartmentUpdate

router = APIRouter()

@router.get("/department", response_model=DepartmentList)
async def get_all_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    departments = db.query(Department).offset(skip).limit(limit).all()
    return {"departments": departments}

@router.post("/department", response_model=DepartmentBase)
async def create_department(department: DepartmentCreate, db: Session = Depends(get_db)):
    new_department = Department(**department.dict())
    db.add(new_department)
    db.commit()
    db.refresh(new_department)
    return new_department

@router.patch("/department/update/{department_id}", response_model=DepartmentUpdate)
async def update_department(department_id: int, department_data: DepartmentUpdate, db:Session = Depends(get_db)):
    existing_department = db.query(Department).filter(Department.id == department_id).first()
    
    if not existing_department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    for field, value in department_data.model_dump().items():
        setattr(existing_department, field, value)
    
    db.commit()
    db.refresh(existing_department)
    
    return existing_department    