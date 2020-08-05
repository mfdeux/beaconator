import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class GACodeBase(BaseModel):
    name: Optional[str] = None
    code: str
    active: bool


class GACodeChange(GACodeBase):
    pass


class GACode(GACodeBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


class PropertyImageKind(str, Enum):
    pixel = "pixel"
    gif = "gif"
    flat = "flat"
    flat_gif = "flat-gif"
    other = "other"


class PropertyBase(BaseModel):
    name: str
    image: PropertyImageKind
    ga_code_id: str
    extra_params: Optional[str] = None
    active: bool


class PropertyChange(PropertyBase):
    pass


class Property(PropertyBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    code: str
    ga_code: GACode

    class Config:
        orm_mode = True


class Login(BaseModel):
    password: str


class AuthToken(BaseModel):
    token: str
