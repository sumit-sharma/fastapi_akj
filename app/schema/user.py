from datetime import date, datetime
import json
from typing import Any, Optional, List

from pydantic import BaseModel, Field


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

class BasicUserModel(BaseModel):
    first_name: str
    last_name: Optional[str]
    shortName: Optional[str]
    profile_image: Optional[str]
    
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

class AstrologerModel(BaseModel):
    id: Optional[int] = Field(..., alias='astrologer_id')
    visibilty: str
    experience: Optional[str]
    about: Optional[str]
    rating: Optional[float] = None
    rating_count: Optional[int] = None
    price: Optional[str]
    total_call_mins: Optional[int]
    category: List[CategoriesModel]
    class Config:
        orm_mode = True
        allow_population_by_field_name = True



class AstroModel(BaseModel):
    User: UserModel
    Astrologer: AstrologerModel

    class Config:
        orm_mode = True

class RateStatics(BaseModel):
    star_1: int
    star_2: int
    star_3: int
    star_4: int
    star_5: int

class AstroModelWithRateStatics(AstroModel):
    rate_statics: RateStatics
    class Config:
        orm_mode = True
     


class RatingInModel(BaseModel):
    user_id: int
    rate: int
    remark: Optional[str]


class RatingOutModel(BaseModel):
    # user_id: int
    rate: int
    remark: Optional[str]
    created_at: Any
    creator: BasicUserModel
    
    class Config:
        orm_mode = True



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
    helptext: Optional[str]
    # receipt: str
    # notes: dict
    attempts: int = 0

    class Config:
        orm_mode = True


class TestimonialModel(BaseModel):
    id: Optional[int]
    name: str
    designation: str
    content: str
    image_url: str
    class Config:
        orm_mode = True


class InputTestimonialModel(BaseModel):
    name: str
    designation: str
    content: str
    image_url: str
    class Config:
        orm_mode = True


class InputBlogModel(BaseModel):
    name: str
    image_url: Optional[str]
    content: Optional[str]
    category_id: Optional[str]
    class Config:
        orm_mode = True
    
class BlogModel(InputBlogModel):
    id: Optional[int]
    slug: str
    popularity = str
    trending = str

class InputSunsignModel(BaseModel):
    name: str
    image_url: Optional[str]
    category_id: int
    help_text: Optional[str]
    status: bool
    class Config:
        orm_mode = True

class SunsignModel(InputSunsignModel):
    id: Optional[int]
    slug: str
    category: CategoriesModel

class InputDailyHoroscopeModel(BaseModel):
    sunsign_id: int
    category_id: int
    content: str
    language_id: int
    published_date: date
    class Config:
        orm_mode = True

class DailyHoroscopeModel(InputDailyHoroscopeModel):
    id: Optional[int]
    # category: CategoriesModel
    language: LanguageModel
    sunsign: SunsignModel

class DeviceTokenModel(BaseModel):
    token_type: int
    device_type: int
    token: str

class NotificationModel(BaseModel):
    receiver_id: int
    content: str
    entity_type: Optional[str]
    entity_id: Optional[int]
    show_sender: bool
    class Config:
        orm_mode = True

class InputNotificationModel(NotificationModel):
    pass

class OutputNotificationModel(NotificationModel):
    id: int
    is_read: bool = False
    sender_id: int
    created_at: datetime
    sender: BasicUserModel
    
    