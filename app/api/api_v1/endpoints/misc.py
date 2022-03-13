import datetime
from enum import Enum
from typing import Optional, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import database, models
from fastapi_pagination import Page, paginate
from schema.misc import PageModel, EditPageModel


router = APIRouter()

get_db = database.get_db


# def fetch_categories(page: Optional[int] = 0, limits: Optional[int] = 1,  db: Session = Depends(get_db)):
@router.get("/page", response_model=Page[PageModel])
def fetch_page_list(db: Session = Depends(get_db)):
    return paginate(db.query(models.Page).all())


class pageEnum(str, Enum):
    terms = "terms"
    privacy = "privacy"


@router.get("/page/{slug}", response_model=PageModel)
def show_page(slug: pageEnum, db: Session = Depends(get_db)):
    page = db.query(models.Page).filter(models.Page.slug == slug).first()
    return page



@router.put("/page/{slug}", response_model=PageModel)
def edit_page(slug: pageEnum, item: EditPageModel, db: Session = Depends(get_db)):
    page = db.query(models.Page).filter(models.Page.slug == slug).first()
    page.content=item.content
    page.title=item.title
    page.meta=item.meta
    page.updated_at=datetime.datetime.now()
    db.commit()
    db.refresh(page)
    return page
