from datetime import date
from typing import Optional
from pydantic import BaseModel


class AuthModel(BaseModel):
    country_code: str
    mobile: str

    class Config:
        orm_mode = True


class LoginModel(AuthModel):
    otp: str


class RegisterModel(AuthModel):
    first_name: str
    last_name: str
    email: str
    dob: Optional[date]


class AdminLoginModel(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True


class CreateCategoryModel(BaseModel):
    name: str
    description: str
    image_url: str

    class Config:
        orm_mode = True


class CreateAstrologerModel(RegisterModel):
    experience: Optional[str]
    description: Optional[str]
    about: Optional[str]

    class Config:
        orm_mode = True
