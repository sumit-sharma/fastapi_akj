from pydantic import BaseModel


class AuthModel(BaseModel):
    country_code: str
    mobile: str 
    
    class Config:
        orm_mode = True


class LoginModel(AuthModel):
    otp: str
    
    
    
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