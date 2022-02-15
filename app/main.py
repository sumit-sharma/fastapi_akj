from typing import Optional

from fastapi import FastAPI

from fastapi.routing import APIRouter

# from api.api_v1.api import api_router

from fastapi_pagination import Page, add_pagination, paginate

from fastapi.testclient import TestClient

from mangum import Mangum

app = FastAPI()




# app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def read_root():
    return {"message": "Hello World"}


@app.get("/test")
def test():
    return {"message": "Hello World"}
    

add_pagination(app)

handler = Mangum(app=app)