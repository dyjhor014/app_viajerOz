from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.models import Department
from schemas.department import DepartmentBase, DepartmentCreate, DepartmentList

router = APIRouter()

@router.get("/department", response_model=DepartmentList)
def get_all_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    departments = db.query(Department).offset(skip).limit(limit).all()
    return {"departments": departments}

@router.post("/department", response_model=DepartmentBase)
def create_department(department: DepartmentCreate, db: Session = Depends(get_db)):
    new_department = Department(**department.dict())
    db.add(new_department)
    db.commit()
    db.refresh(new_department)
    return new_department