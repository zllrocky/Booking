from uuid import UUID
from fastapi import HTTPException

from app.rooms.dao import RoomsDAO
from app.rooms.schemas import SRooms, SRoomsAdd, SRoomsUpdate


async def get_all_rooms(hotel_id: int) -> list[SRooms]:
    return await RoomsDAO.find_all(hotel_id=hotel_id)


async def get_room_for_id(room_id: UUID) -> SRooms:
    result =  await RoomsDAO.find_one_or_none(room_id=room_id)
    if not result:
        raise HTTPException(status_code=404, detail='Not found')
    return result


async def add_rooms(hotel_id: int, rooms_data: SRoomsAdd) ->SRooms:
    rooms_dict = rooms_data.model_dump()
    rooms_dict['hotel_id'] = hotel_id
    new_rooms = await RoomsDAO.add(**rooms_dict)
    if not new_rooms:
        raise HTTPException(status_code=500, detail='Internal Server Error')
    return new_rooms


async def update_rooms_info_for_id(room_id: UUID, rooms_data: SRoomsUpdate) -> SRooms:
    current_room = await RoomsDAO.find_one_or_none(room_id=room_id)
    if not current_room:
        raise HTTPException(status_code=404, detail='Room not found')
    room_dict = rooms_data.model_dump(exclude_unset=True)
    update_room = await RoomsDAO.update(filter_by={'room_id': room_id},
                                          data=room_dict)
    return update_room


async def delete_room_for_id(room_id: UUID) ->None:
    result = await RoomsDAO.delete(room_id=room_id)
    if not result:
        raise HTTPException(status_code=404, detail='Room not found')