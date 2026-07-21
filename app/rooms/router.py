from uuid import UUID
from fastapi import APIRouter

from app.dependencies import DependsAdminOrOwner
from app.rooms.schemas import SRooms, SRoomsAdd, SRoomsUpdate
from app.rooms.services import get_all_rooms, get_room_for_id, add_rooms, \
    update_rooms_info_for_id, delete_room_for_id


router = APIRouter(tags=['Rooms'])


@router.get('/hotels/{hotel_id}/rooms', summary='[PUBLIC] Get all rooms for hotel',
            description='**Access**: Public (no authorization required).\n'
                        'Returns a list of all rooms for the specified hotel.')
async def get_all_rooms_for_hotel(hotel_id: int) -> list[SRooms]:
    return await get_all_rooms(hotel_id=hotel_id)


@router.get('/rooms/{room_id}', summary='[PUBLIC] Get room by ID',
            description='**Access**: Public (no authorization required).\n'
                        'Returns detailed information about a specific room by its UUID.')
async def get_room(room_id: UUID) -> SRooms:
    return await get_room_for_id(room_id=room_id)


@router.post('/hotels/{hotel_id}/rooms', status_code=201,
             summary='[ADMIN / OWNER] Add new room for hotel',
             description=('**Access**: Administrators and Owners only.\n'
                          'Creates a new room for the specified hotel.'))
async def add_rooms_for_hotel(hotel_id: int, rooms_data: SRoomsAdd,
                              _: DependsAdminOrOwner) -> SRooms:
    return await add_rooms(hotel_id=hotel_id, rooms_data=rooms_data)


@router.patch('/rooms/{room_id}', summary='[ADMIN / OWNER] Update room info',
              description=('**Access:** Administrators and Owners only.\nPartial update'
                           ' of room information. You can provide any combination of fields to update.'))
async def update_rooms_info(room_id: UUID, rooms_data: SRoomsUpdate,
                            _: DependsAdminOrOwner) ->SRooms:
    return await update_rooms_info_for_id(room_id=room_id, rooms_data=rooms_data)


@router.delete('/rooms/{room_id}', status_code=204,
               summary='[ADMIN / OWNER] Delete room',
               description='**Access:** Administrators and Owners only.'
                           '\nDeletes a specific room by its UUID.')
async def delete_room(room_id: UUID, _: DependsAdminOrOwner) -> None:
    await delete_room_for_id(room_id=room_id)
