from typing import Optional

from pydantic import conint, constr

from app.server.models.generic import BaseModel
from app.server.static.enums import ListingStatus


class ListingCreateRequest(BaseModel):
    item_id: constr(min_length=1, max_length=150, strip_whitespace=True)
    description: constr(min_length=1, max_length=450, strip_whitespace=True)
    price: conint(ge=0)


class ListingCreateDB(BaseModel):
    item_name: str
    description: str
    price: int
    status: ListingStatus
    seller_id: str


class ListingUpdateRequest(BaseModel):
    description: Optional[constr(min_length=1, max_length=450, strip_whitespace=True)]
    price: Optional[conint(ge=0)]
    status: Optional[ListingStatus]


class ListingUpdateDB(BaseModel):
    description: Optional[str]
    price: Optional[int]
    status: Optional[ListingStatus]
