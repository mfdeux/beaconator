import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class GACodeCreate(BaseModel):
    name: str
    code: str
    active: bool = True

    class Config:
        extra = "forbid"


class GACodeUpdate(BaseModel):
    name: Optional[str]
    code: Optional[str]
    active: Optional[str]

    class Config:
        extra = "forbid"


class GACode(BaseModel):
    id: int
    name: str
    code: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    active: bool

    class Config:
        orm_mode = True


class PropertyImageKind(str, Enum):
    pixel = "pixel"
    gif = "gif"
    flat = "flat"
    flat_gif = "flat-gif"
    other = "other"


class PropertyCreate(BaseModel):
    name: str
    image: PropertyImageKind
    ga_code_id: int
    extra_params: Optional[str] = None
    active: bool = True

    class Config:
        extra = "forbid"


class PropertyUpdate(BaseModel):
    name: Optional[str]
    image: Optional[PropertyImageKind]
    ga_code_id: Optional[int]
    extra_params: Optional[str]
    active: Optional[bool]

    class Config:
        extra = "forbid"


class Property(BaseModel):
    id: int
    name: str
    image: PropertyImageKind
    created_at: datetime.datetime
    updated_at: datetime.datetime
    code: str
    ga_code: GACode
    ga_code_id: int
    active: bool
    extra_params: Optional[str]

    class Config:
        orm_mode = True


class Login(BaseModel):
    password: str


class AuthToken(BaseModel):
    token: str
