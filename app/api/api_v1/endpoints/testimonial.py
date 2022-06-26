from fastapi.responses import JSONResponse
from typing import Optional, List
from fastapi import APIRouter, Depends, Header, Path
from api.deps import RoleChecker, RoutePermission
from core.auth.auth_bearer import JWTBearer
from schema.user import InputTestimonialModel, TestimonialModel
from sqlalchemy.orm import Session
import database, models
from fastapi_pagination import Page, paginate
from schema.user import TestimonialModel


router = APIRouter()

get_db = database.get_db


@router.get("/testimonials", response_model=Page[TestimonialModel])
def fetch_testimonial(db: Session = Depends(get_db)):
    return paginate(db.query(models.Testimonial).all())


allowed_roles = RoleChecker(["admin"])


@router.post("/testimonial", response_model=TestimonialModel)
def create_testimonial(
    item: InputTestimonialModel,
    db: Session = Depends(get_db),
    current_user=Depends(allowed_roles),
):
    testimonial = models.Testimonial(
        name=item.name,
        designation=item.designation,
        content=item.content,
        image_url=item.image_url,
        status=True,
    )
    db.add(testimonial)
    db.commit()
    db.refresh(testimonial)
    return testimonial


@router.put("/testimonial/{testimonial_id}", response_model=TestimonialModel)
def edit_testimonial(
    testimonial_id: int,
    item: InputTestimonialModel,
    db: Session = Depends(get_db),
    current_user=Depends(allowed_roles),
):
    testimonial = (
        db.query(models.Testimonial)
        .filter(models.Testimonial.id == testimonial_id)
        .first()
    )
    if testimonial:
        testimonial.name=item.name
        testimonial.designation=item.designation
        testimonial.content=item.content
        testimonial.image_url=item.image_url    
        db.commit()
        db.refresh(testimonial)
        return testimonial
    else:
     return JSONResponse(status_code=404, content={"detail": "testimonal not found."})   

@router.delete("/testimonial/{testimonial_id}")
def delete_testimonial(
    testimonial_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(allowed_roles),
):
    testimonial = (
        db.query(models.Testimonial)
        .filter(models.Testimonial.id == testimonial_id)
        .first()
    )
    if testimonial:
        db.delete(testimonial)
        db.commit()
        return JSONResponse(status_code=200, content={"detail": "testimonal has been deleted."})
    else:
     return JSONResponse(status_code=404, content={"detail": "testimonal not found."})   
 
 
 