from typing import Optional, List
from fastapi import APIRouter, Depends
from schema.user import CategoriesModel
from sqlalchemy.orm import Session
import database, models
from fastapi_pagination import Page, paginate

router = APIRouter()

get_db = database.get_db


# def fetch_categories(page: Optional[int] = 0, limits: Optional[int] = 1,  db: Session = Depends(get_db)):
@router.get("/categories", response_model=Page[CategoriesModel])
def fetch_categories(db: Session = Depends(get_db)):
    return paginate(db.query(models.Category).all())





@router.get("/categories/{category_id}", response_model=CategoriesModel)
def fetch_category_detail(category_id: int, db: Session = Depends(get_db)):
    categories = db.query(models.Category).filter(models.Category.id == category_id).first()
    return categories


