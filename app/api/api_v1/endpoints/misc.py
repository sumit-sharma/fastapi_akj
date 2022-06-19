import datetime
from enum import Enum
from typing import Optional, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schema.user import LanguageModel
import database, models
from fastapi_pagination import Page, paginate
from schema.misc import CreateLanguageModel, PageModel, EditPageModel

router = APIRouter()

get_db = database.get_db


# def fetch_categories(page: Optional[int] = 0, limits: Optional[int] = 1,  db: Session = Depends(get_db)):
@router.get("/page", response_model=Page[PageModel])
def fetch_page_list(db: Session = Depends(get_db)):
    return paginate(db.query(models.Page).all())


class pageEnum(str, Enum):
    terms = "terms"
    privacy = "privacy"
    faq_user = "faq-user"


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


@router.get("/languages", response_model=Page[LanguageModel])
def fetch_languages(db: Session = Depends(get_db)):
    return paginate(db.query(models.Language).all())



@router.get("/language/{language_id}", response_model=LanguageModel)
def show_category(language_id: int, db: Session = Depends(get_db)):
    language = db.query(models.Language).filter(models.Language.id == language_id).first()
    return language



@router.post("/language", response_model=LanguageModel)
def create_category(item: CreateLanguageModel, db: Session = Depends(get_db)):
    language = models.Language(name=item.name)
    db.add(language)
    db.commit()
    db.refresh(language)
    return language


@router.put("/language/{language_id}", response_model=LanguageModel)
def edit_language(language_id: int, item: CreateLanguageModel, db: Session = Depends(get_db)):
    language = db.query(models.Language).filter(models.Language.id == language_id).first()
    language.name= item.name
    db.commit()
    db.refresh(language)
    return language

 
