from typing import Optional, List
from fastapi import APIRouter, Depends
from fastapi_pagination import paginate, Page
from sqlalchemy.orm import Session, selectinload
# from api.deps import get_current_active_user
from schema.user import RouteInAccessModel, RouteAccessModel
import database, models
from core.auth.auth_bearer import signJWT
from schema.auth import AdminLoginModel, CreateCategoryModel
from passlib.context import CryptContext

router = APIRouter()

get_db = database.get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)



def authuneticate_user(email, password, db: Session = Depends(get_db)):
    status = False
    user = db.query(models.User).filter(models.User.email == email).options(selectinload(models.User.role)).first()
    if(user):
        # if verify_password(password, user.password):
        status = user
    
    return status


# @router.post("/login", response_model=UserModel)
@router.post("/login")
def admin_login(item: AdminLoginModel, db: Session = Depends(get_db)):
    # return {"password" : item.password, "hashed_password": get_password_hash(item.password)}
    user = authuneticate_user(item.email, item.password, db)
    return {"detail": user, "token": signJWT(user.id)}

# @router.post("/list-routes", response_model=Page[RouteAccessModel])
# def list_routes(db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
#     return paginate(db.query(models.RouteAccess).all())

# @router.post("/add-routes", response_model=RouteAccessModel)
# def add_routes(item: RouteInAccessModel, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
#     row = db.query(models.RouteAccess).\
#             filter(models.RouteAccess.role_id == item.role_id, models.RouteAccess.route_url == item.route_url).\
#             first()
#     if(not row):
#         row = models.RouteAccess(role_id = item.role_id, route_url = item.route_url)
#         db.add(row)
#         db.commit()
#         db.refresh(row)
    
#     return row



