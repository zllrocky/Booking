from fastapi import HTTPException

from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SHotelAdd, SHotelUpdate, SHotel


async def get_all_info_hotels(location: str | None = None,
                              name: str | None = None) -> list[SHotel]:
    return await HotelsDAO.find_all(location=location, name=name)


async def get_hotel_info(hotel_id: int) -> SHotel:
    current_hotel = await HotelsDAO.find_one_or_none(hotel_id=hotel_id)
    if not current_hotel:
        raise HTTPException(status_code=404, detail='Hotel not found')
    return current_hotel


async def add_hotel(hotel_data: SHotelAdd):
    hotel_dict = hotel_data.model_dump()
    new_hotel = await HotelsDAO.add(**hotel_dict)
    if not new_hotel:
        raise HTTPException(status_code=500, detail='Internal Server Error')
    return new_hotel


async def update_hotel_info(hotel_id: int, hotel_data: SHotelUpdate):
    current_hotel = await HotelsDAO.find_one_or_none(hotel_id=hotel_id)
    if not current_hotel:
        raise HTTPException(status_code=404, detail='Hotel not found')
    hotel_dict = hotel_data.model_dump(exclude_unset=True)
    update_hotel = await HotelsDAO.update(filter_by={'hotel_id': hotel_id}, data=hotel_dict)
    return update_hotel


async def delete_hotel(hotel_id: int):
    result = await HotelsDAO.delete(hotel_id=hotel_id)
    if not result:
        raise HTTPException(status_code=404, detail='Not found')

