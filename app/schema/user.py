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


class UserModel(BaseModel):
    id: int
    first_name: str
    last_name: str
    country: str
    email: str
    phone: str = None
    role_id: int = None
    profile_image: str = None
    role: RoleModel
    languages: List[LanguageModel]

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
