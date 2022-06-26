import datetime
from enum import Enum
import uuid
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


def get_customer_id(user_id, db):
    return db.query(models.PaymentCustomer).filter(user_id == user_id).first()


@router.post("/create-customer")
def create_customer(user=Depends(allowed_roles), db: Session = Depends(get_db)):
    """create customerID for payment gateways(razorpay)

    Args:
        user (_type_, optional): _description_. Defaults to Depends(allowed_roles).
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Returns:
        JSON: _description_
    """
    try:
        customer = (
            db.query(models.PaymentCustomer)
            .filter(models.PaymentCustomer.user_id == user.id)
            .first()
        )
        if customer:
            cust_id = customer.cust_id
        else:
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
                cust_id = res["id"]
                row = models.PaymentCustomer(cust_id=res["id"], user_id=user.id)
                db.add(row)
                db.commit()
                db.refresh(row)
        if cust_id:
            return JSONResponse(
                status_code=200, content={"detail": "cutsomer Id: " + cust_id}
            )
        return JSONResponse(
            status_code=400, content={"detail": "some error occurred, please try later"}
        )
    except Exception as ex:
        msg = getattr(ex, "message", str(ex))
        print(msg)
        return JSONResponse(status_code=422, content={"detail": msg})


@router.post("/create-order")
def create_order(
    item: CreateOrderModel,
    current_user=Depends(allowed_roles),
    db: Session = Depends(get_db),
):
    try:
        # return get_customer_id(current_user.id, db)
        
        # print(type(uuid.uuid4()))
        
        client = razorpay.Client(auth=(razor_key, razor_secret))
        res = client.order.create(
            {
                "amount": item.amount,
                "currency": "INR",
                "receipt": str(uuid.uuid4()),
                "notes": {
                    "customer_id": get_customer_id(current_user.id, db).cust_id,
                }
            }
        )

        # return res

        if res:
            # amount = Column(FLOAT)
            # currency = Column(String(255), default="INR")
            # receipt = Column(String(255), comment="transaction_uid on transaction")
            # notes = Column(JSON)
            # attempts = Column(Integer, default=0)
            # status = Column(String(255), default="init")

            row = models.PaymentOrder(
                user_id = current_user.id,
                entity_id=res["id"],
                amount = res["amount"],
                currency=res["currency"],
                receipt = res["receipt"],
                offer_id = res["offer_id"],
                notes = res["notes"],
                attempts = res["attempts"], 
                status = res["status"]
                )
            db.add(row)
            db.commit()
            db.refresh(row)
            return JSONResponse(
                status_code=200, content={"detail": row}
            )
        return JSONResponse(
            status_code=400, content={"detail": "some error occurred, please try later"}
        )
    except Exception as ex:
        msg = getattr(ex, "message", str(ex))
        print(msg)
        return JSONResponse(status_code=422, content={"detail": msg})
