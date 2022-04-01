import api.api_v1.endpoints
from typing import Optional, List, Union
from fastapi import APIRouter, Depends, Query
from core.auth.auth_bearer import JWTBearer
from schema.user import AstrologerModel, UserModel, AstroModel 
from sqlalchemy.orm import Session
import database, models
from fastapi_pagination import Page, paginate

router = APIRouter()

get_db = database.get_db


@router.get("/astrologer", response_model=Page[AstroModel])
# @router.get("/astrologer")
# def astrologer_list(token: str = Depends(JWTBearer()), db: Session = Depends(get_db)):
def astrologer_list(category: Optional[list[int]] = Query(None), db: Session = Depends(get_db)):
    print(category)
    for x in category:
        print(x)
    # fil = filter(models.Astrologer.category.any(id = 1) | models.Astrologer.category.any(id = 4)).\
    
    users = db.query(models.User, models.Astrologer).\
                join(models.Astrologer, models.User.id == models.Astrologer.user_id).\
                filter(models.User.role_id == 3).\
                filter(models.Astrologer.category.any(id = 1) | models.Astrologer.category.any(id = 4)).\
                all()
                # filter(models.Astrologer.category.any(id = 2)).\
                # join(models.Category, models.Astrologer.category_id == models.Category.id).\
    # print(users)
    return paginate(users)
    return users



