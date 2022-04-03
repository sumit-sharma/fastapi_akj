from typing import Optional, List
from pydantic import BaseModel


class PageModel(BaseModel):
    id: int
    name: str
    slug: str
    content: str
    title : str
    meta: str
    class Config:
        orm_mode = True


class EditPageModel(BaseModel):
    content: str
    title : str
    meta: str

    class Config:
        orm_mode = True

class LanguageModel(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class CreateLanguageModel(BaseModel):
    name: str

    class Config:
        orm_mode = True

