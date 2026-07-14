from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal


class SRooms(BaseModel):
    room_id: UUID
    hotel_id: int
    name: str
    price: Decimal
    quantity: int
    facilities: list[str]


class SRoomsAdd(BaseModel):
    name: str
    price: Decimal
    quantity: int
    facilities: list[str]


class SRoomsUpdate(BaseModel):
    name: str | None = None
    price: Decimal | None = None
    quantity: int | None = None
    facilities: list[str] | None = None