from typing import Optional, List
from fastapi import APIRouter, Depends
from schema.user import CategoriesModel
from sqlalchemy.orm import Session
import database, models
from fastapi_pagination import Page, paginate

router = APIRouter()

get_db = database.get_db


@router.get("/test")
def fetch_categories(db: Session = Depends(get_db)):
    return "user"

