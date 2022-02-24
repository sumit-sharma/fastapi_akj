
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import Optional
from sqlalchemy.orm import Session
from core.auth.auth_bearer import JWTBearer, RoleChecker, signJWT, decodeJWT
import database, models
from schema.auth import AuthModel, LoginModel
from fastapi.responses import JSONResponse
from schema.user import UserModel
router = APIRouter()

get_db = database.get_db


def sendsms(country_code, mobile):
    pass


def check_user(country_code, mobile, db: Session = Depends(get_db)):
    status = False
    user = db.query(models.User).filter(models.User.country_code == country_code, models.User.mobile_no == mobile).first()
    if(user):
        status = user
    
    return status


@router.post("/send_otp")
def send_otp(item: AuthModel, db: Session = Depends(get_db)):
    user = check_user(item.country_code, item.mobile, db)
    if(user):
        otp =  models.AccountOtp(type="mobile", otp="1234", user_id = user.id, reference= "login")
        db.add(otp)
        db.commit()
        db.refresh(otp)
        return otp
    else:
        return JSONResponse(status_code=404, content={"message": "user not found"})




@router.post("/login")
def login_access_token(item: LoginModel, db: Session = Depends(get_db)):
    user = check_user(item.country_code, item.mobile, db)
    
    return {"token": signJWT(user.id), "detail": user}


@router.get("/user", response_model=UserModel)
def user_profile(token: str = Depends(JWTBearer()), db: Session = Depends(get_db)):
    result =  decodeJWT(token)
    user =  db.query(models.User).filter(models.User.id == result['user_id']).first()
    return user    




