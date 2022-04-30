import datetime
import api.api_v1.endpoints
from typing import Optional, List, Union
from fastapi import APIRouter, Depends, Query
from core.auth.auth_bearer import JWTBearer, decodeJWT
from schema.user import AstrologerModel, RatingInModel, UserModel, AstroModel 
from sqlalchemy.orm import Session
from sqlalchemy.sql import text, func
import database, models
from fastapi_pagination import Page, paginate

router = APIRouter()

get_db = database.get_db

def fetch_user_rating(user_id, db: Session = Depends(get_db)):
    rate_data = db.query(func.count(models.Rating.rate).label('count'), func.ifnull(func.avg(models.Rating.rate), 0)).filter(models.Rating.user_id == user_id).first()
    return rate_data    
        



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


def avg_rate(user_id, save=False, db: Session = Depends(get_db)):
    rate_data = db.query(func.count(models.Rating.rate).label('count'), func.ifnull(func.avg(models.Rating.rate), 0).label('avg') ).filter(models.Rating.user_id == user_id).first()
    if save:
        row = db.query(models.Astrologer).filter(models.Astrologer.user_id == user_id).first()
        row.rating = rate_data.avg
        row.rating_count = rate_data.count
        row.updated_at=datetime.datetime.now()
        db.add(row)
        db.commit()                    
    return rate_data        
    




@router.post("/rate-astrologer")
def rate_astrologer(item: RatingInModel, token: str = Depends(JWTBearer(['admin'])), db: Session = Depends(get_db)):    
    authtoken =  decodeJWT(token)
    row = db.query(models.Rating).filter(models.Rating.user_id == item.user_id, models.Rating.created_by == authtoken['user_id']).first()
    if(row):
        row.rate = item.rate
        row.remark = item.remark
        row.updated_at = datetime.datetime.now()
    else:
        row = models.Rating(user_id = item.user_id, created_by = authtoken['user_id'], rate = item.rate, remark = item.remark)
        
    db.add(row)
    db.commit()
    db.refresh(row)
    """ save updated  to astrologer table
    """    
    return avg_rate(item.user_id, True, db)
    



