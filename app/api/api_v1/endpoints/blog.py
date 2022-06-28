from fastapi.responses import JSONResponse
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Header, Path
from slugify import slugify
from api.deps import RoleChecker, RoutePermission
from core.auth.auth_bearer import JWTBearer
from schema.user import InputBlogModel, BlogModel
from sqlalchemy.orm import Session
import database, models
from fastapi_pagination import Page, paginate
from schema.user import TestimonialModel


router = APIRouter()

get_db = database.get_db


def check_blog(blog_id: int, db):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if blog:
        return blog
    raise HTTPException(status_code=404, detail="blog not found")


def auth_blog(blog_id: int, current_user, db):
    blog = check_blog(blog_id, db)
    if blog.created_by == current_user.id or current_user.role_id == 1:
        return blog
    raise HTTPException(
        status_code=403, detail="You are not authorised for this operation"
    )


@router.get("/blog", response_model=Page[BlogModel])
def fetch_blogs(db: Session = Depends(get_db)):
    return paginate(db.query(models.Blog).all())


@router.get("/blog/{blog_id}", response_model=BlogModel)
def fetch_blog(blog_id: int, db: Session = Depends(get_db)):
    return check_blog(blog_id, db)


allowed_roles = RoleChecker(["admin", "astrologer"])


@router.post("/blog", response_model=InputBlogModel)
def create_blog(
    item: InputBlogModel,
    db: Session = Depends(get_db),
    current_user=Depends(allowed_roles),
):

    blog = models.Blog(
        name=item.name,
        slug=slugify(item.name),
        content=item.content,
        image_url=item.image_url,
        created_by=current_user.id,
    )
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog


@router.put("/blog/{blog_id}", response_model=BlogModel)
def edit_testimonial(
    blog_id: int,
    item: InputBlogModel,
    db: Session = Depends(get_db),
    current_user=Depends(allowed_roles),
):

    blog = auth_blog(blog_id, current_user, db)
    blog.name = item.name
    blog.slug = slugify(item.name)
    blog.content = item.content
    blog.image_url = item.image_url
    db.commit()
    db.refresh(blog)
    return blog


@router.delete("/blog/{blog_id}")
def delete_blog(
    blog_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(allowed_roles),
):
    blog = auth_blog(blog_id, current_user, db)
    db.delete(blog)
    db.commit()
    return JSONResponse(status_code=200, content={"detail": "blog has been deleted."})
