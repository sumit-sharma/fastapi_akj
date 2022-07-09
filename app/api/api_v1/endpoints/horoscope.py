from datetime import datetime
from fastapi.responses import JSONResponse
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Header, Path, Query
from slugify import slugify
from api.deps import RoleChecker, RoutePermission
from core import curd
from core.auth.auth_bearer import JWTBearer
from schema.user import (
    DailyHoroscopeModel,
    InputDailyHoroscopeModel,
    InputSunsignModel,
    SunsignModel,
)
from sqlalchemy.orm import Session
import database, models
from fastapi_pagination import Page, paginate
from schema.user import TestimonialModel


router = APIRouter()

get_db = database.get_db



@router.get("/sunsigns", response_model=Page[SunsignModel])
def fetch_sunsigns(db: Session = Depends(get_db)):
    return paginate(db.query(models.Sunsign).all())


@router.get("/sunsign/{sunsign_id}", response_model=SunsignModel)
def fetch_sunsign(sunsign_id: int, db: Session = Depends(get_db)):
    return curd.check_item(sunsign_id, models.Sunsign, "Sunsign", db)


@router.get("/daily_horoscope/today", response_model=Page[DailyHoroscopeModel])
def fetch_horoscopes(
    category_id: Optional[str] = Query(None),
    sunsign_id: Optional[str] = Query(None), 
    db: Session = Depends(get_db)
):
    today = datetime.today().strftime("%Y-%m-%d")
    horoscope = db.query(models.DailyHoroscope).filter(
        models.DailyHoroscope.published_date == today
    )
    if category_id:
        horoscope = horoscope.filter(models.DailyHoroscope.category_id == category_id)
    
    if sunsign_id:
        horoscope = horoscope.filter(models.DailyHoroscope.sunsign_id == sunsign_id)
        
    return paginate(horoscope.all())


allowed_roles = RoleChecker(["admin"])


@router.post("/sunsign", response_model=SunsignModel)
def create_sunsign(
    item: InputSunsignModel,
    db: Session = Depends(get_db),
    current_user=Depends(allowed_roles),
):

    sunsign = models.Sunsign(
        name=item.name,
        slug=slugify(item.name),
        help_text=item.help_text,
        category_id=item.category_id,
        image_url=item.image_url,
    )
    db.add(sunsign)
    db.commit()
    db.refresh(sunsign)
    return sunsign


@router.put("/sunsign/{sunsign_id}", response_model=SunsignModel)
def edit_sunsign(
    sunsign_id: int,
    item: InputSunsignModel,
    db: Session = Depends(get_db),
    current_user=Depends(allowed_roles),
):

    sunsign = curd.check_item(sunsign_id, models.Sunsign, "Sunsign", db)
    sunsign.name = item.name
    sunsign.slug = slugify(item.name)
    sunsign.help_text = item.help_text
    sunsign.image_url = item.image_url
    db.commit()
    db.refresh(sunsign)
    return sunsign


@router.post("/daily_horoscope", response_model=DailyHoroscopeModel)
def create_daily_horoscope(
    item: InputDailyHoroscopeModel,
    db: Session = Depends(get_db),
    current_user=Depends(allowed_roles),
):
    curd.check_item(item.sunsign_id, models.Sunsign, "Sunsign", db)
    curd.check_item(item.category_id, models.Category, "Category", db)
    curd.check_item(item.language_id, models.Language, "Language", db)
    dailyHoroscope = models.DailyHoroscope(
        sunsign_id=item.sunsign_id,
        content=item.content,
        category_id=item.category_id,
        language_id=item.language_id,
        published_date=item.published_date,
    )
    db.add(dailyHoroscope)
    db.commit()
    db.refresh(dailyHoroscope)
    return dailyHoroscope
