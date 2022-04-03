import api.api_v1.endpoints
from typing import Optional, List, Union
from fastapi import APIRouter, Depends, Query
from core.auth.auth_bearer import JWTBearer
from schema.user import AstrologerModel, UserModel, AstroModel 
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
import database, models
from fastapi_pagination import Page, paginate

router = APIRouter()

get_db = database.get_db


@router.get("/astrologer", response_model=Page[AstroModel])
# @router.get("/astrologer")
# def astrologer_list(token: str = Depends(JWTBearer()), db: Session = Depends(get_db)):
def astrologer_list(category: Optional[list[int]] = Query(None), language: Optional[list[int]] = Query(None), db: Session = Depends(get_db)):
    users = db.query(models.User, models.Astrologer).\
                join(models.Astrologer, models.User.id == models.Astrologer.user_id).\
                filter(models.User.role_id == 3)
    if(category):
        users = users.filter(models.Astrologer.category.any(models.Category.id.in_(category)))
    if(language):
        # join to pivot table and filter throught is said to be faster than conventional "any" technique
        users = users.join(models.LanguageUser).filter(models.LanguageUser.language_id.in_(language)) 
    
    users = users.all()        
    return paginate(users)
    return users



