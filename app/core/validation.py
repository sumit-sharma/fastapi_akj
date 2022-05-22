import database, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Security, status, Request, Path

from api.deps import check_email, check_user


get_db = database.get_db


def unique_user_validation(country_code, mobile, email, db: Session = Depends(get_db)):
    user = check_user(country_code, mobile, db)
    if user:
        raise HTTPException(status_code=422, detail="Phone number already in exists")
    user = check_email(email, db)
    if user:
        raise HTTPException(status_code=422, detail="Email already in exists")
    return True
