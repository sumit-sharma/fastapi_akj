from fastapi import APIRouter

from api.api_v1.endpoints import auth, user, category, misc, transaction, testimonial, blog, horoscope, notifications

api_router = APIRouter()

api_router.include_router(auth.router, tags=['auth'])

api_router.include_router(user.router, tags=["users"])

api_router.include_router(category.router, tags=["users"])

api_router.include_router(misc.router, tags=["misc"])

api_router.include_router(transaction.router, tags=["transactions"])

api_router.include_router(testimonial.router, tags=["testimonials"])

api_router.include_router(blog.router, tags=["news"])

api_router.include_router(horoscope.router, tags=["horoscope"])

api_router.include_router(notifications.router, tags=["notifications"])

