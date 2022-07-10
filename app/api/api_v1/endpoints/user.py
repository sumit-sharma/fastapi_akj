import datetime
from enum import Enum
from token import OP
import api.api_v1.endpoints
from typing import Optional, List, Union
from fastapi import APIRouter, Depends, Query
from core.auth.auth_bearer import JWTBearer, decodeJWT
from schema.user import AstroModelWithRateStatics, AstrologerModel, RatingInModel, UserModel, AstroModel
from sqlalchemy.orm import Session
from sqlalchemy.sql import text, func, case
from sqlalchemy import inspect
import database, models
from fastapi_pagination import Page, paginate

router = APIRouter()

get_db = database.get_db


def fetch_rating_detail(user_id, db: Session = Depends(get_db)):
    rate_data_detail = (
        db.query(
            func.count(case((models.Rating.rate == 1, 1))).label('star_1'),
            func.count(case((models.Rating.rate == 2, 1))).label('star_2'),
            func.count(case((models.Rating.rate == 3, 1))).label('star_3'),
            func.count(case((models.Rating.rate == 4, 1))).label('star_4'),
            func.count(case((models.Rating.rate == 5, 1))).label('star_5'),
        )
        .filter(models.Rating.user_id == user_id)
        .group_by(models.Rating.user_id)
        .first()
    )
    return rate_data_detail


def avg_rate(user_id, save=False, db: Session = Depends(get_db)):
    rate_data = (
        db.query(
            func.count(models.Rating.rate).label("count"),
            func.ifnull(func.avg(models.Rating.rate), 0).label("avg"),
        )
        .filter(models.Rating.user_id == user_id)
        .first()
    )
    if save:
        row = (
            db.query(models.Astrologer)
            .filter(models.Astrologer.user_id == user_id)
            .first()
        )
        row.rating = rate_data.avg
        row.rating_count = rate_data.count
        row.updated_at = datetime.datetime.now()
        db.add(row)
        db.commit()
    return rate_data


class StatusEnum(str, Enum):
    active = 1
    inactive = 0
    block = 2


@router.get("/astrologer", response_model=Page[AstroModel])
# @router.get("/astrologer")
# def astrologer_list(token: str = Depends(JWTBearer()), db: Session = Depends(get_db)):
def astrologer_list(
    astrologer_status: StatusEnum = Query(1),
    search: Optional[str] = Query(None),
    category: Optional[list[int]] = Query(None),
    language: Optional[list[int]] = Query(None),
    db: Session = Depends(get_db),
):
    users = (
        db.query(models.User, models.Astrologer)
        .join(models.Astrologer, models.User.id == models.Astrologer.user_id)
        .filter(models.User.role_id == 3)
        .filter(models.Astrologer.status == astrologer_status)
    )
    if category:
        users = users.filter(
            models.Astrologer.category.any(models.Category.id.in_(category))
        )
    if language:
        # join to pivot table and filter throught is said to be faster than conventional "any" technique
        users = users.join(models.LanguageUser).filter(
            models.LanguageUser.language_id.in_(language)
        )

    if search:
        users = users.filter(
            models.User.first_name.like("%" + search + "%")
            | models.User.last_name.like("%" + search + "%")
        )

    users = users.all()
    return paginate(users)


@router.post("/rate-astrologer")
def rate_astrologer(
    item: RatingInModel,
    token: str = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    authtoken = decodeJWT(token)
    row = (
        db.query(models.Rating)
        .filter(
            models.Rating.user_id == item.user_id,
            models.Rating.created_by == authtoken["user_id"],
        )
        .first()
    )
    if row:
        row.rate = item.rate
        row.remark = item.remark
        row.updated_at = datetime.datetime.now()
    else:
        row = models.Rating(
            user_id=item.user_id,
            created_by=authtoken["user_id"],
            rate=item.rate,
            remark=item.remark,
        )

    db.add(row)
    db.commit()
    db.refresh(row)
    """ save updated  to astrologer table
    """
    return avg_rate(item.user_id, True, db)


@router.get("/astrologer-detail/{astrologer_id}", response_model=Union[AstroModelWithRateStatics, AstroModel])
def astrologer_detail(
    astrologer_id: int,
    db: Session = Depends(get_db),
):
    
    astrologer = (
        db.query(models.User, models.Astrologer)
        .join(models.Astrologer, models.User.id == models.Astrologer.user_id)
        .filter(models.Astrologer.id == astrologer_id)
        .first()
    )
    # print(type(astrologer) is dict)
    if astrologer:        
        astrologer = astrologer._asdict()
        rating_statics_data = fetch_rating_detail(astrologer["User"].id, db)
        astrologer["rate_statics"] = rating_statics_data
    
    return astrologer
