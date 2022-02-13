from pydantic import BaseModel


class AuthModel(BaseModel):
    country_code: str
    mobile: str 
    
    class Config:
        orm_mode = True


class LoginModel(AuthModel):
    otp: str