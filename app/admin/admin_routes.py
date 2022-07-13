from typing import Any, Optional, List
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import paginate, Page
from sqlalchemy.orm import Session, selectinload
from api.deps import RoleChecker, store_astrologer
from api.api_v1.endpoints.user import StatusEnum
from core.validation import unique_user_validation

# from api.deps import get_current_active_user
from schema.user import AstroModel, RouteInAccessModel, RouteAccessModel, UserModel
import database, models
from core.auth.auth_bearer import signJWT
from schema.auth import AdminLoginModel, CreateAstrologerModel, CreateCategoryModel
from passlib.context import CryptContext

router = APIRouter()

get_db = database.get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

allowed_roles = RoleChecker(["admin"])


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authuneticate_user(email, password, db: Session = Depends(get_db)):
    status = False
    user = (
        db.query(models.User)
        .filter(models.User.email == email)
        .options(selectinload(models.User.role))
        .first()
    )
    if user:
        # if verify_password(password, user.password):
        status = user

    return status


# @router.post("/login", response_model=UserModel)
@router.post("/login")
def admin_login(item: AdminLoginModel, db: Session = Depends(get_db)):
    # return {"password" : item.password, "hashed_password": get_password_hash(item.password)}
    user = authuneticate_user(item.email, item.password, db)
    return {"detail": user, "token": signJWT(user.id, db)}


@router.post("/create-astrologer", response_model=AstroModel)
def create_astrologer(
    item: CreateAstrologerModel,
    current_user=Depends(allowed_roles),
    db: Session = Depends(get_db),
):
    """create astrologer from admin panel

    Args:
        item (CreateAstrologerModel): Need user and astrologer data, like experience, about and description
        current_user (_type_, optional): _description_. Defaults to Depends(allowed_roles).
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Returns:
        _type_: _description_
    """
    unique_user_validation(item.country_code, item.mobile, item.email, db)
    itemData = item.dict()
    itemData["role_id"] = 3
    astrologer = store_astrologer(itemData, db)
    user = (
        db.query(models.User, models.Astrologer)
        .join(models.Astrologer, models.User.id == models.Astrologer.user_id)
        .filter(models.Astrologer.id == astrologer.id)
        .first()
    )
    return user


@router.put("/change-astrologer-status/{astrologerId}/{astrologer_status}")
def block_astrologer(
    astrologerId: int,
    astrologer_status: StatusEnum,
    current_user=Depends(allowed_roles),
    db: Session = Depends(get_db),
) -> Any:
    """block astrologer from admin panel. Astrologer can login, but not visible from user panel, can't take calls.

    Args:
        astrologerId (int): astrologerId
        astrologer_status (StatusEnum): 1=> active, 0=>inactive, 2=> block
        current_user (_type_, optional): _description_. Defaults to Depends(allowed_roles).
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: raise 404 exception when invalid astrologerId

    Returns:
        Any: astrologer models
    """
    astrologer = (
        db.query(models.Astrologer).filter(models.Astrologer.id == astrologerId).first()
    )
    if astrologer:
        astrologer.status = astrologer_status
        db.commit()
        db.refresh(astrologer)
        return astrologer
    else:
        raise HTTPException(status_code=404, detail="Astrologer not found")


"""uncomment below route when you want to dynamic database managed role based access control. """
# @router.post("/list-routes", response_model=Page[RouteAccessModel])
# def list_routes(db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
#     return paginate(db.query(models.RouteAccess).all())

# @router.post("/add-routes", response_model=RouteAccessModel)
# def add_routes(item: RouteInAccessModel, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
#     row = db.query(models.RouteAccess).\
#             filter(models.RouteAccess.role_id == item.role_id, models.RouteAccess.route_url == item.route_url).\
#             first()
#     if(not row):
#         row = models.RouteAccess(role_id = item.role_id, route_url = item.route_url)
#         db.add(row)
#         db.commit()
#         db.refresh(row)

#     return row


@router.put("/toggle-block-user/{user_id}", response_model=UserModel)
def toggle_block_user(
    user_id: int, db: Session = Depends(get_db), current_user=Depends(allowed_roles)
) -> models.User:
    """Toggle user to block/unblock action

    Args:
        user_id (int): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).
        current_user (_type_, optional): _description_. Defaults to Depends(allowed_roles).

    Returns:
        models.User: user
    """
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user:
            db.query(models.OauthAccessToken).filter(
                models.OauthAccessToken.user_id == user_id
            ).update({"revoked": 1})
            user.is_blocked = not user.is_blocked
            db.commit()
            db.refresh(user)
            return user
        raise HTTPException(status_code=404, detail="User not found")
    except:
        raise HTTPException(status_code=404, detail="User not found")
