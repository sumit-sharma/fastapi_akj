from sqlalchemy import (
    FLOAT,
    JSON,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    Table,
    DateTime,
    Text,
    Float,
    Date,
)
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
    name = Column(String(225))
    slug = Column(String(225))
    image_url = Column(String(225))
    description = Column(String(225))


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(225))


class OauthAccessToken(Base):
    __tablename__ = "oauth_access_tokens"
    id = Column(String(100), primary_key=True)
    user_id = Column(BIGINT(unsigned=True), ForeignKey("users.id"))
    name = Column(String(255))
    scopes = Column(Text)
    revoked = Column(Boolean)
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now())
    expires_at = Column(DateTime)

    # Relationships
    user = relationship("User", foreign_keys=[user_id])


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    # username = Column(String(225))
    password = Column(String(225))
    first_name = Column(String(225))
    last_name = Column(String(225))
    shortName = Column(String(225))
    gender = Column(String(225))
    dob = Column(Date)
    birth_time = Column(String(225))
    birth_place = Column(String(225))
    email = Column(String(225))
    country = Column(String(225))
    phone = Column(String(225))
    profile_image = Column(String(225))
    role_id = Column(Integer, ForeignKey("roles.id"))
    is_blocked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now())

    # Relationships
    role = relationship("Role", foreign_keys=[role_id])

    languages = relationship("Language", secondary="language_user", backref="users")

    # def __repr__(self):
    #     return "<User %r>" % self.role


class AccountOtp(Base):
    __tablename__ = "accounts_otp"

    id = Column(Integer, primary_key=True, autoincrement=True)
    otp = Column(String(20))
    user_id = Column(BIGINT(unsigned=True), ForeignKey("users.id"))
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
    language_id = Column(Integer, ForeignKey("languages.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now())

    # Relationships
    # language = relationship("Language", foreign_keys=[language_id])
    language = relationship("Language", foreign_keys=[language_id])
    user = relationship("User", foreign_keys=[user_id])


class AstrologerCategory(Base):
    __tablename__ = "astrologer_category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    astrologer_id = Column(Integer, ForeignKey("astrologers.id"))
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now())
    # Relationships
    category = relationship("Category", foreign_keys=[category_id])
    astrologer = relationship("Astrologer", foreign_keys=[astrologer_id])


class Astrologer(Base):
    __tablename__ = "astrologers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    experience = Column(String(500))
    about = Column(Text)
    rating = Column(Float)
    rating_count = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now())
    status = Column(SmallInteger)
    # relationship
    # user = relationship("User", foreign_keys="user_id")
    # role = relationship("Role", foreign_keys=[role_id])
    user = relationship("User", backref="users", uselist=False)

    category = relationship(
        "Category", secondary="astrologer_category", backref="astrologers"
    )


class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        BIGINT(unsigned=True), ForeignKey("users.id"), comment="user who be rated"
    )
    created_by = Column(BIGINT(unsigned=True), ForeignKey("users.id"))
    rate = Column(SMALLINT(unsigned=True))
    remark = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now())
    user = relationship("User", foreign_keys=[user_id])


class RouteAccess(Base):
    __tablename__ = "route_access"
    id = Column(Integer, primary_key=True, autoincrement=True)
    route_name = Column(String(225))
    route_method = Column(String(20))
    role_id = Column(BIGINT(unsigned=True), ForeignKey("roles.id"))
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now())
    role = relationship("Role", foreign_keys=[role_id])


# razor pay customer
class PaymentCustomer(Base):
    __tablename__ = "payment_customers"
    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    user_id = Column(BIGINT(unsigned=True), ForeignKey("users.id"))
    cust_id = Column(String(225))
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now())
    user = relationship("User", foreign_keys=[user_id])


class PaymentOrder(Base):
    __tablename__ = "orders"
    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    user_id = Column(BIGINT(unsigned=True), ForeignKey("users.id"))
    entity_id = Column(
        String(255), comment="order ID after creation, src: razorpay response"
    )
    amount = Column(FLOAT)
    currency = Column(String(255), default="INR")
    receipt = Column(String(255), comment="transaction_uid on transaction")
    offer_id = Column(String(255))
    notes = Column(JSON)
    attempts = Column(Integer, default=0)
    status = Column(String(255), default="init")
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now())

    user = relationship("User", foreign_keys=[user_id])


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    transaction_uid = Column(String(225))
    customer_id = Column(BIGINT(unsigned=True), ForeignKey("payment_customers.id"))
    order_id = Column(BIGINT(unsigned=True), ForeignKey("orders.id"))
    amount = Column(FLOAT)
    currency = Column(String(255), default="INR")
    response = Column(JSON)
    status = Column(String(255), default="init")
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now())

    customer = relationship("PaymentCustomer", foreign_keys=[customer_id])
    order = relationship("PaymentOrder", foreign_keys=[order_id])


class Testimonial(Base):
    __tablename__ = "testimonials"
    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    name = Column(String(225))
    designation = Column(String(225))
    content = Column(Text)
    image_url = Column(String(225))
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now())


Base.metadata.create_all(bind=engine)
