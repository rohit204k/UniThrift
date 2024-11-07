from typing import Optional

from pydantic import constr

from app.server.models.custom_types import EmailStr
from app.server.models.generic import BaseModel
from app.server.static.enums import Role, UserStatus


class UserCreateRequest(BaseModel):
    first_name: constr(min_length=1, max_length=150, strip_whitespace=True)
    last_name: constr(min_length=1, max_length=150, strip_whitespace=True)
    email: EmailStr
    university_id: constr(min_length=1, max_length=15, strip_whitespace=True)
    phone: Optional[constr(min_length=1, max_length=30, strip_whitespace=True)] = ''
    address: Optional[constr(min_length=1, max_length=150, strip_whitespace=True)] = ''
    password: constr(min_length=1, max_length=150, strip_whitespace=True)


class UserUpdateRequest(BaseModel):
    email: EmailStr
    first_name: Optional[constr(min_length=1, max_length=150, strip_whitespace=True)]
    last_name: Optional[constr(min_length=1, max_length=150, strip_whitespace=True)]
    phone: Optional[constr(min_length=1, max_length=30, strip_whitespace=True)]
    address: Optional[constr(min_length=1, max_length=150, strip_whitespace=True)]


class UserCreateDB(BaseModel):
    first_name: str
    last_name: str
    email: str
    university_id: str
    phone: str
    address: Optional[str] = ''
    user_type: Role
    user_status: UserStatus = UserStatus.ACTIVE
    is_verified: bool = False


class UserUpdateDB(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    user_status: Optional[UserStatus]
    is_verified: Optional[bool]
