from uuid import UUID

from fastapi import APIRouter,Depends

from app.auth.auth import get_current_active_user
from app.rooms.schemas import SRooms, SRoomsAdd, SRoomsUpdate
from app.rooms.services import get_all_rooms, get_room_for_id, add_rooms, \
    update_rooms_info_for_id, delete_room_for_id

router = APIRouter(tags=['Rooms'])


@router.get('/hotels/{hotel_id}/rooms')
async def get_all_rooms_for_hotel(hotel_id: int) -> list[SRooms]:
    return await get_all_rooms(hotel_id=hotel_id)


@router.get('/rooms/{rooms_id}')
async def get_room(room_id: UUID) -> SRooms:
    return await get_room_for_id(room_id=room_id)


@router.post('/hotels/{hotel_id}/rooms', status_code=201)
async def add_rooms_for_hotel(hotel_id: int, rooms_data: SRoomsAdd,
                              _ = Depends(get_current_active_user)) -> SRooms:
    return await add_rooms(hotel_id=hotel_id, rooms_data=rooms_data)


@router.patch('/rooms/{room_id}')
async def update_rooms_info(room_id: UUID, rooms_data: SRoomsUpdate,
                            _ = Depends(get_current_active_user)) ->SRooms:
    return await update_rooms_info_for_id(room_id=room_id, rooms_data=rooms_data)


@router.delete('/rooms/{room_id}', status_code=204)
async def delete_room(room_id: UUID, _ = Depends(get_current_active_user)) -> None:
    await delete_room_for_id(room_id=room_id)
