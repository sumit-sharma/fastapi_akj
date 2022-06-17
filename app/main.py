from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.routing import APIRouter

from api.api_v1.api import api_router

from admin import admin_routes


from fastapi_pagination import Page, add_pagination, paginate

from fastapi.testclient import TestClient

from mangum import Mangum

app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://api.aapkajyotish.com",
    "https://aapkajyotish.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],   
)

app.include_router(api_router, prefix="/api/v1")

app.include_router(admin_routes.router, prefix="/admin", tags=['admin'])


@app.get("/")
async def read_root():
    return {"message": "Hello World"}


@app.get("/test")
def test():
    return {"message": "Hello World"}
    

add_pagination(app)

handler = Mangum(app=app)