from typing import Optional, List
from fastapi import APIRouter, Depends
from schema.user import CategoriesModel
from sqlalchemy.orm import Session
import database, models
from fastapi_pagination import Page, paginate
from schema.auth import  CreateCategoryModel
from slugify import slugify



router = APIRouter()

get_db = database.get_db

# def fetch_categories(page: Optional[int] = 0, limits: Optional[int] = 1,  db: Session = Depends(get_db)):
@router.get("/categories", response_model=Page[CategoriesModel])
def fetch_categories(db: Session = Depends(get_db)):
    return paginate(db.query(models.Category).all())



@router.get("/categories/{category_id}", response_model=CategoriesModel)
def show_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    return category



@router.post("/category", response_model=CategoriesModel)
def create_category(item: CreateCategoryModel, db: Session = Depends(get_db)):
    category = models.Category(name=item.name, slug=slugify(item.name), description=item.description, image_url=item.image_url)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.put("/category/{categoryId}", response_model=CategoriesModel)
def edit_category(category_id: int, item: CreateCategoryModel, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()

    category.name= item.name
    category.slug=slugify(item.name)
    category.description=item.description
    category.image_url=item.image_url
    db.commit()
    db.refresh(category)
    return category

 
