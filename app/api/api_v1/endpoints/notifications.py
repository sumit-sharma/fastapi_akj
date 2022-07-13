import datetime
from fastapi.responses import JSONResponse
from typing import Optional, List
from fastapi import APIRouter, Depends, Header, Path
from sqlalchemy import update
from api.deps import RoleChecker, RoutePermission
from core.curd import check_item, upsert
from core.auth.auth_bearer import JWTBearer
from sqlalchemy.orm import Session
import database, models
from fastapi_pagination import Page, paginate
from schema.user import (
    DeviceTokenModel,
    OutputNotificationModel,
    InputNotificationModel,
)


router = APIRouter()

get_db = database.get_db

allowed_roles = RoleChecker(["admin", "astrologer", "user"])


@router.post("/store-device-token")
def store_device_token(
    item: DeviceTokenModel,
    db: Session = Depends(get_db),
    current_user=Depends(allowed_roles),
):
    return upsert(
        models.DeviceToken,
        dict(user_id=current_user.id, device_type=item.device_type),
        dict(token_type=item.token_type, token=item.token, updated_at= datetime.datetime.now()),
        db
    )


# @router.get("/fetch-notifications", response_model=Page[OutputNotificationModel])
@router.get("/fetch-notifications")
def fetch_notifications(
    db: Session = Depends(get_db),
    current_user=Depends(allowed_roles),
):
    return paginate(
        db.query(models.Notification)
        .filter(models.Notification.receiver_id == current_user.id)
        .all()
    )


@router.post("/create-notification", response_model=OutputNotificationModel)
def create_notification(
    item: InputNotificationModel,
    current_user=Depends(allowed_roles),
    db: Session = Depends(get_db),
):
    notification = models.Notification(
        receiver_id=item.receiver_id,
        content=item.content,
        entity_type=item.entity_type,
        entity_id=item.entity_id,
        show_sender=item.show_sender,
        sender_id=current_user.id,
        is_read=False,
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


@router.put("/mark-read/{notification_id}", response_model=OutputNotificationModel)
def mark_read(
    notification_id: int,
    current_user=Depends(allowed_roles),
    db: Session = Depends(get_db),
):
    notification = check_item(notification_id, models.Notification, "Notification", db)
    if notification and notification.receiver_id == current_user.id:
        notification.is_read = True
        db.commit()
        db.refresh(notification)
        return notification
    else:
        return JSONResponse(status_code=403, content={"detail": "not authourised."})


@router.put("/mark-all-read", response_model=Page[OutputNotificationModel])
def mark_all_read(
    current_user=Depends(allowed_roles),
    db: Session = Depends(get_db),
):
    notifications = db.query(models.Notification).filter(
        models.Notification.receiver_id == current_user.id
    )
    notifications.update({"is_read": True})
    db.commit()
    return paginate(notifications.all())
