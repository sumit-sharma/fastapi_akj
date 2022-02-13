from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
import datetime


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    slug = Column(String)
    image_url = Column(String)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    country_code = Column(String)
    mobile_no = Column(String)
    


class AccountOtp(Base):
    __tablename__ = "accounts_otp"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    otp = Column(String)
    reference = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now())
    # user = relationship("User", back_populates="accounts_otp")
    