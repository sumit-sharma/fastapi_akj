from typing import Optional

from pydantic import BaseModel


class CategoriesModel(BaseModel):
    id: int
    name: str
    slug: str
    image_url: str

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    id: int
    first_name: str
    last_name: str
    # image_url: str
    country_code: str
    email: str
    username: str
    mobile_no: str

    class Config:
        orm_mode = True
