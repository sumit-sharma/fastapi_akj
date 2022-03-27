from typing import Optional, List
from fastapi import APIRouter, Depends
from core.auth.auth_bearer import JWTBearer
from schema.user import AstrologerModel, CategoriesModel
from sqlalchemy.orm import Session
import database, models
from fastapi_pagination import Page, paginate

router = APIRouter()

get_db = database.get_db


@router.get("/astrologer", response_model=Page[AstrologerModel])
# @router.get("/astrologer")
# def astrologer_list(token: str = Depends(JWTBearer()), db: Session = Depends(get_db)):
def astrologer_list(db: Session = Depends(get_db)):
    users = db.query(models.User).filter(models.User.role_id == 3).all()
    return users



