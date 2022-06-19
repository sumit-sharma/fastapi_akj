import logging
from typing import Any, List, Optional
from fastapi import Depends, HTTPException, Security, status, Request, Path
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
import starlette
import database, models
from core.auth.auth_bearer import JWTBearer, decodeJWT
from fastapi.security import HTTPBearer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

get_db = database.get_db

oauth2 = JWTBearer()

# check user
def check_user(country_code, mobile, db: Session = Depends(get_db)):
    status = False
    user = (
        db.query(models.User)
        .filter(models.User.country == country_code, models.User.phone == mobile)
        .first()
    )
    if user:
        status = user

    return status


# check user
def check_email(email, db: Session = Depends(get_db)):
    status = False
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        status = user

    return status


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2),
) -> Any:
    # return token
    result = decodeJWT(token)
    uid =  ""
    if "uid" in result.keys():
        uid =  result["uid"]
    oauthToken = (
        db.query(models.OauthAccessToken)
        .filter(models.OauthAccessToken.id == uid)
        .filter(models.OauthAccessToken.revoked == 0)
        .first()
    )
    if oauthToken:
        user = db.query(models.User).filter(models.User.id == result["user_id"]).first()
        return user
    else:
        raise HTTPException(status_code=403, detail="Invalid token or expired token.")


def store_user(
    item: List,
    db: Session = Depends(get_db),
) -> Any:
    last_name = item["last_name"][0] if not item["last_name"] is None else ""
    short_name = (item["first_name"][0] + last_name).strip()
    user = models.User(
        country=item["country_code"],
        phone=item["mobile"],
        first_name=item["first_name"],
        last_name=item["last_name"],
        email=item["email"],
        role_id=item["role_id"],
        shortName=short_name,
        dob=item["dob"],
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def store_astrologer(
    item: List,
    db: Session = Depends(get_db),
) -> Any:
    user = store_user(item, db)

    if user.id:
        astrologer = models.Astrologer(
            user_id=user.id,
            experience=item["experience"],
            about=item["about"],
            status=0,
            # rating = item["rating"],
            # rating_count = item["rating_count"]
        )
        db.add(astrologer)
        db.commit()
        db.refresh(astrologer)
        return astrologer


def update_user(id: int, item: List, db: Session = Depends(get_db)) -> Any:

    last_name = item.last_name[0] if not item.last_name is None else ""
    short_name = (item.first_name[0] + last_name).strip()

    user = db.query(models.User).filter(models.User.id == id).first()

    user.first_name = item.first_name
    user.last_name = item.last_name
    user.shortName = short_name
    user.gender = item.gender
    user.dob = item.dob
    user.birth_time = item.birth_time
    user.birth_place = item.birth_place
    user.profile_image = item.profile_image

    db.commit()
    db.refresh(user)
    return user


class RoutePermission:
    """use when you want to manage permissions by table and managed by UI.
    incase you want static role-based-permission use `RoleChecker` class
    """

    def __init__(
        self,
        route_name: str = "",
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user),
        request: starlette.requests.Request = None,
    ):

        self.route_name = route_name

    def __call__(
        self,
        route_name: str = "",
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user),
        request: starlette.requests.Request = None,
    ):
        # return request.method

        # return request.path_params
        if current_user.role_id != 1:
            routeAccess = (
                db.query(models.RouteAccess)
                .filter(models.RouteAccess.route_name == self.route_name)
                .filter(models.RouteAccess.role_id == current_user.role_id)
                .filter(models.RouteAccess.route_method == request.method)
                .first()
            )
            if not routeAccess:
                raise HTTPException(
                    status_code=403, detail="Permission denied for this route"
                )

        return current_user


class RoleChecker:
    """use you want static role-based-permission.
    incase you want to manage permissions by table and managed by UI use `RoutePermission`.
    """

    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user=Depends(get_current_user)):
        if (
            current_user.role.name != "admin"
            and current_user.role.name not in self.allowed_roles
        ):
            logger.debug(
                f"User with role {current_user.role.name} not in {self.allowed_roles}"
            )
            raise HTTPException(
                status_code=403, detail="Permission denied for this operation"
            )

        return current_user
