from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String, Table, DateTime, Text, Float
from sqlalchemy.orm import relationship
from database import Base, engine
import datetime
from sqlalchemy.dialects.mysql import BIGINT, SMALLINT

# group = Table('users_groups', Base.metadata,
#     # id = Column(Integer, primary_key=True, index=True)
#     Column('user_id', Integer, ForeignKey('users.id')),
#     Column('group_id', Integer, ForeignKey('auth_group.id'))
# )

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    slug = Column(String)
    image_url = Column(String)
    description = Column(String)


class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    # username = Column(String)
    password = Column(String)
    name = Column(String)
    # last_name = Column(String)
    email = Column(String)
    country = Column(String)
    phone = Column(String)
    profile_image = Column(String)
    role_id = Column(Integer, ForeignKey('roles.id'))    
      # Relationships
    role = relationship("Role", foreign_keys=[role_id])

    languages = relationship("Language", secondary="language_user", backref="users")



    # def __repr__(self):
    #     return "<User %r>" % self.role



class AccountOtp(Base):
    __tablename__ = "accounts_otp"

    id = Column(Integer, primary_key=True, autoincrement=True)
    otp = Column(String(20))
    user_id = Column(BIGINT(unsigned=True), ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now())
    user = relationship("User", foreign_keys=[user_id])
    


class Page(Base):
    __tablename__ = "pages"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(225))
    slug = Column(String(225))
    title = Column(String(225))
    meta = Column(String(225))
    # user_id = Column(ForeignKey('users.id')),
     
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now())


class Language(Base):
    __tablename__ = "languages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(225))
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now())

class LanguageUser(Base):
    __tablename__ = "language_user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    language_id = Column(Integer, ForeignKey('languages.id'))    
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now())

    # Relationships
    # language = relationship("Language", foreign_keys=[language_id])
    language = relationship("Language", foreign_keys=[language_id])
    user = relationship("User", foreign_keys=[user_id])


class AstrologerCategory(Base):
    __tablename__ = "astrologer_category"
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    astrologer_id = Column(Integer, ForeignKey('astrologers.id'))    
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now())
    # Relationships
    category = relationship("Category", foreign_keys=[category_id])
    astrologer = relationship("Astrologer", foreign_keys=[astrologer_id])

class Astrologer(Base):
    __tablename__ = "astrologers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    experience = Column(String(500))
    about = Column(Text)
    rating = Column(Float)
    rating_count = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now())
    # relationship
    # user = relationship("User", foreign_keys="user_id")
    # role = relationship("Role", foreign_keys=[role_id])
    user = relationship("User",  backref="users", uselist=False)

    category = relationship("Category", secondary="astrologer_category", backref="astrologers")


class Rating(Base):
    __tablename__ = 'ratings'
    id = Column(Integer, primary_key=True,autoincrement=True)
    user_id = Column(BIGINT(unsigned=True), ForeignKey('users.id'), comment="user who be rated")
    created_by = Column(BIGINT(unsigned=True), ForeignKey('users.id'))
    rate = Column(SMALLINT(unsigned=True))
    remark = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now())    
    user = relationship("User", foreign_keys=[user_id])

    
Base.metadata.create_all(bind=engine)
    