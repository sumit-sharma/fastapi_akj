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
class UserModel(BaseModel):
    id: int
    name: str
    country: str
    email: str
    phone: str = None
    role_id:int   = None
    role: RoleModel
    class Config:
        orm_mode = True

