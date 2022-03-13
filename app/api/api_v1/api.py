from fastapi import APIRouter

from api.api_v1.endpoints import auth, user, category, misc

api_router = APIRouter()

api_router.include_router(auth.router, tags=['auth'])

api_router.include_router(user.router, tags=["users"])

api_router.include_router(category.router, tags=["users"])

api_router.include_router(misc.router, tags=["misc"])

