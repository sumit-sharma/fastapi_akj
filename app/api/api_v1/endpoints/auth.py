import math
import random
from typing import Any, Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from api.deps import RoleChecker
from core.auth.auth_bearer import JWTBearer, signJWT, decodeJWT
import database, models
from schema.auth import AuthModel, LoginModel
from fastapi.responses import JSONResponse
from schema.user import UserModel
import requests
from settings import otp_exp_min
from datetime import datetime
from api.deps import RoutePermission


router = APIRouter()

get_db = database.get_db


# function to generate OTP
def generateOTP(num: int = 4):

    # Declare a digits variable
    # which stores all digits
    digits = "0123456789"
    OTP = ""

    # length of password can be changed
    # by changing value in range
    for i in range(num):
        OTP += digits[math.floor(random.random() * 10)]

    return OTP


def sendsms(country_code, mobile):
    return 1234
    # URL =  "http://164.52.195.161/API/BalAlert.aspx"
    # PARAMS = {'uname': 20220081, 'pass': "G99x9GJX", 'send': "KANNDS"}
    otp = generateOTP(4)

    TXTSMS = "http://164.52.195.161/API/SendMsg.aspx?uname=20220081&pass=G99x9GJX&send=KANNDS&dest=#mobile&msg=Dear%20Customer,%0A%0AOTP%20for%20verify%20your%20mobile%20number%20on%20%20AKJ%20is%20#otp.%0AKANNDS"
    TXTSMS = TXTSMS.replace("#mobile", mobile)
    TXTSMS = TXTSMS.replace("#otp", otp)
    # r = requests.get(url = URL, params = PARAMS)
    r = requests.get(TXTSMS)
    # extracting data in json format
    # data = r.json()

    return otp


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


def otp_user(user_id: int, otp: int, db: Session = Depends(get_db)):
    user = (
        db.query(models.AccountOtp)
        .filter(models.AccountOtp.user_id == user_id, models.AccountOtp.otp == otp)
        .order_by(desc(models.AccountOtp.id))
        .first()
    )
    if user:
        return True  # TODO: delete later
        minutes = round((datetime.now() - user.created_at).total_seconds() / 60)
        if minutes <= int(otp_exp_min):
            return True
    return False


@router.post("/send_otp")
def send_otp(item: AuthModel, db: Session = Depends(get_db)):
    otp = sendsms(item.country_code, item.mobile)
    user = check_user(item.country_code, item.mobile, db)
    if user:
        row = models.AccountOtp(otp=otp, user_id=user.id)
        db.add(row)
        db.commit()
        db.refresh(row)
        return JSONResponse(
            status_code=200, content={"message": "otp has been send to your mobile"}
        )
    else:
        return JSONResponse(status_code=404, content={"message": "user not found"})


@router.post("/verify_otp")
def login_access_token(item: LoginModel, db: Session = Depends(get_db)):
    user = check_user(item.country_code, item.mobile, db)
    if otp_user(user.id, item.otp, db):
        return {"token": signJWT(user.id), "detail": user}
    else:
        return JSONResponse(
            status_code=403, content={"message": "Invalid otp or it has been expired"}
        )


@router.post("/register")
def login_access_token(item: LoginModel, db: Session = Depends(get_db)):
    user = check_user(item.country_code, item.mobile, db)
    if otp_user(user.id, item.otp, db):
        return {"token": signJWT(user.id), "detail": user}
    else:
        return JSONResponse(
            status_code=403, content={"message": "Invalid otp or it has been expired"}
        )


# @router.get("/user", response_model=UserModel)
# def user_profile(token: str = Depends(JWTBearer()), db: Session = Depends(get_db)):
#     result =  decodeJWT(token)
#     user =  db.query(models.User).filter(models.User.id == result['user_id']).first()
#     return user

# @router.get("/user", name="myprofile", response_model=UserModel)

allowed_roles = RoleChecker(["user"])


@router.get("/user/me", name="myprofile", response_model=UserModel)
def user_profile(
    db: Session = Depends(get_db), current_user=Depends(allowed_roles)
) -> Any:
    # result =  decodeJWT(token)
    return current_user
    # return current_user
    # result =  decodeJWT(token)
    # user =  db.query(models.User).filter(models.User.id == result['user_id']).first()
    # return user
