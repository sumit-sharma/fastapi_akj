
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import Optional
from sqlalchemy.orm import Session
from core.auth.auth_bearer import JWTBearer, RoleChecker, signJWT, decodeJWT
import database, models
from schema.auth import AuthModel, LoginModel
from fastapi.responses import JSONResponse
from schema.user import UserModel
import requests

router = APIRouter()

get_db = database.get_db


# function to generate OTP
def generateOTP() :
 
    # Declare a digits variable 
    # which stores all digits
    digits = "0123456789"
    OTP = ""
 
   # length of password can be changed
   # by changing value in range
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
 
    return OTP

def sendsms(country_code, mobile):
    
	# api-endpoint
	# URL = "http://164.52.195.161/API/SendMsg.aspx"
	URL =  "http://164.52.195.161/API/BalAlert.aspx"
	# location given here
	
	  
	# defining a params dict for the parameters to be sent to the API
	# PARAMS = {'dest': mobile, 'msg': "Dear%20Customer,%0A%0AOTP%20for%20verify%20your%20mobile%20number%20on%20%20test%20is%20test.%0AKANNDS"}
	PARAMS = {'uname': 20220081, 'pass': "G99x9GJX", 'send': "KANNDS"}
	  
	# sending get request and saving the response as response object
	r = requests.get(url = URL, params = PARAMS)
	  
	# extracting data in json format
	data = r.json()
	
	return data

def check_user(country_code, mobile, db: Session = Depends(get_db)):
    status = False
    user = db.query(models.User).filter(models.User.country_code == country_code, models.User.mobile_no == mobile).first()
    if(user):
        status = user
    
    return status


@router.post("/send_otp")
def send_otp(item: AuthModel, db: Session = Depends(get_db)):
    return sendsms(item.country_code, item.mobile)
    
    # user = check_user(item.country_code, item.mobile, db)
    # if(user):
    #     otp =  models.AccountOtp(type="mobile", otp=generateOTP(), user_id = user.id, reference= "login")
    #     db.add(otp)
    #     db.commit()
    #     db.refresh(otp)
    #     return otp
    # else:
    #     return JSONResponse(status_code=404, content={"message": "user not found"})




@router.post("/login")
def login_access_token(item: LoginModel, db: Session = Depends(get_db)):
    user = check_user(item.country_code, item.mobile, db)
    
    return {"token": signJWT(user.id), "detail": user}


@router.get("/user", response_model=UserModel)
def user_profile(token: str = Depends(JWTBearer()), db: Session = Depends(get_db)):
    result =  decodeJWT(token)
    user =  db.query(models.User).filter(models.User.id == result['user_id']).first()
    return user    




