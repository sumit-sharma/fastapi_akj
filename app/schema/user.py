from datetime import date
import json
from typing import Optional, List

from pydantic import BaseModel


class CategoriesModel(BaseModel):
    id: int
    name: str
    slug: str
    description: str = None
    image_url: str = None

    class Config:
        orm_mode = True


class RoleModel(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class LanguageModel(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class UpdateProfileModel(BaseModel):
    first_name: str
    last_name: Optional[str]
    shortName: Optional[str]
    gender: Optional[str]
    dob: Optional[date]
    birth_time: Optional[str]
    birth_place: Optional[str]
    profile_image: Optional[str]
    
    class Config:
        orm_mode = True

    

class UserModel(UpdateProfileModel):
    id: int
    country: str
    phone: str = None
    email: str
    role_id: int = None
    role: RoleModel
    languages: List[LanguageModel]
    is_blocked: bool
    class Config:
        orm_mode = True


class AstrologerModel(BaseModel):
    experience: Optional[str]
    about: Optional[str]
    rating: Optional[float] = None
    rating_count: Optional[int] = None

    category: List[CategoriesModel]

    class Config:
        orm_mode = True


class AstroModel(BaseModel):
    User: UserModel
    Astrologer: AstrologerModel

    class Config:
        orm_mode = True


class RatingInModel(BaseModel):
    user_id: int
    rate: int
    remark: Optional[str]


class RouteInAccessModel(BaseModel):
    route_url: str
    role_id: int

    class Config:
        orm_mode = True


class RouteAccessModel(BaseModel):
    route_url: str
    role_id: int
    role: RoleModel

    class Config:
        orm_mode = True


class CreateOrderModel(BaseModel):
    amount: str
    currency: str = "INR"
    receipt: str
    notes: dict
    attempts: int = 0

    class Config:
        orm_mode = True


