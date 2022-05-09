import logging
from typing import Any, Optional
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


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2),
) -> Any:
    # return token
    result = decodeJWT(token)
    user = db.query(models.User).filter(models.User.id == result["user_id"]).first()
    return user


class RoutePermission:
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
