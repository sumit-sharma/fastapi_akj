import datetime
from enum import Enum
import api.api_v1.endpoints
from fastapi.responses import JSONResponse
from typing import Optional, List, Union
from fastapi import APIRouter, Depends, HTTPException, Query
from api.deps import RoleChecker
from core.auth.auth_bearer import JWTBearer, decodeJWT
from schema.user import CreateOrderModel
from sqlalchemy.orm import Session
from sqlalchemy.sql import text, func
import database, models
from fastapi_pagination import Page, paginate
import razorpay
from settings import razor_key, razor_secret

router = APIRouter()

get_db = database.get_db
allowed_roles = RoleChecker(["user", "admin"])


@router.post("/create-customer")
def create_customer(user=Depends(allowed_roles), db: Session = Depends(get_db)):
    try:
        client = razorpay.Client(auth=(razor_key, razor_secret))
        res = client.customer.create(
            {
                "name": (
                    user.first_name
                    + " "
                    + (user.last_name if not user.last_name is None else "")
                ).strip(),
                "contact": (user.country + user.phone).strip(),
                "email": user.email,
                "fail_existing": 1,
                "notes": {
                    "user_id": user.id,
                },
            }
        )

        if res:
            row = models.PaymentCustomer(cust_id=res["id"], user_id=user.id)
            db.add(row)
            db.commit()
            db.refresh(row)
            return JSONResponse(
                status_code=200, content={"detail": "cutsomer Id saved"}
            )
        return JSONResponse(
            status_code=400, content={"detail": "some error occurred, please try later"}
        )
    except Exception as ex:
        msg = getattr(ex, "message", str(ex))
        print(msg)
        return JSONResponse(status_code=422, content={"detail": msg})

@router.post("/create-order")
def create_order(item: CreateOrderModel, user=Depends(allowed_roles), db: Session = Depends(get_db)):
    try:
        client = razorpay.Client(auth=(razor_key, razor_secret))
        res = client.order.create({
            "amount": 50000,
            "currency": "INR",
            "receipt": "receipt#1",
            "notes": {
            "key1": "value3",
            "key2": "value2"
            }
        })


        if res:
            row = models.PaymentCustomer(cust_id=res["id"], user_id=user.id)
            db.add(row)
            db.commit()
            db.refresh(row)
            return JSONResponse(
                status_code=200, content={"detail": "cutsomer Id saved"}
            )
        return JSONResponse(
            status_code=400, content={"detail": "some error occurred, please try later"}
        )
    except Exception as ex:
        msg = getattr(ex, "message", str(ex))
        print(msg)
        return JSONResponse(status_code=422, content={"detail": msg})

