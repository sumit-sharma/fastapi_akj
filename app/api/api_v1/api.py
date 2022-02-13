from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, user

api_router = APIRouter()

api_router.include_router(auth.router, tags=['auth'])

api_router.include_router(user.router, tags=["users"])

