from pydantic import BaseModel

class SHotel(BaseModel):
    hotel_id: int
    name: str
    location: str
    latitude: float
    longitude: float
    rooms_quantity: int
    image_id: int
    services: list[str]


class SHotelAdd(BaseModel):
    name: str
    location: str
    latitude: float
    longitude: float
    rooms_quantity: int
    image_id: int
    services: list[str]


class SHotelUpdate(BaseModel):
    name: str | None = None
    location: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    rooms_quantity: int | None = None
    image_id: int | None = None
    services: list[str] | None = None