from fastapi import APIRouter

from app.hotels.schemas import SHotel, SHotelAdd, SHotelUpdate
from app.hotels.services import get_all_info_hotels, get_hotel_info, add_hotel, \
    update_hotel_info, delete_hotel
from app.dependencies import DependsAdminOrOwner

router = APIRouter(prefix='/hotels', tags=['Hotels'])


@router.get('', summary='[PUBLIC] Get all hotels',
            description='**Access:** Public (no authorization required).\n\n'
                        'Returns a list of hotels. Can be optionally filtered by location '
                        'or name. Returns the full catalog if no filters are provided.')
async def get_all_hotels(location: str | None = None, name: str | None = None) -> list[SHotel]:
    return await get_all_info_hotels(location=location, name=name)


@router.get('/{hotel_id}', summary='[PUBLIC] Get hotel by ID',
            description='**Access:** Public (no authorization required).\n\n'
                        'Returns detailed information about a specific hotel by its '
                        'unique ID. Returns 404 Not Found if the hotel does not exist.')
async def get_hotel(hotel_id: int) -> SHotel:
    return await get_hotel_info(hotel_id=hotel_id)


@router.post('', status_code=201, summary='[ADMIN / OWNER] Add new hotel',
             description='**Access:** Administrators and Owners only.\n'
                         'Creates a new hotel. The ID is generated automatically.')
async def post_hotel(hotel_data: SHotelAdd, _: DependsAdminOrOwner) -> SHotel:
    return await add_hotel(hotel_data)


@router.patch('/{hotel_id}', summary='[ADMIN / OWNER] Update hotel info',
              description='**Access:** Administrators and Owners only.\n\n'
                          'Partial update of hotel information. You can provide '
                          'any combination of fields to update.')
async def update_hotel(hotel_id: int, hotel_data: SHotelUpdate,
                       _: DependsAdminOrOwner) -> SHotel:
    return await update_hotel_info(hotel_id, hotel_data)


@router.delete('/{hotel_id}', status_code=204, summary='[ADMIN / OWNER] Delete hotel',
               description='**Access:** Administrators and Owners only.\n\n'
                           'Permanently deletes a hotel from the database. '
                           'The hotel will be removed from all listings and search results.\n\n'
                           '**Warning:** This action cannot be undone.')
async def remove_hotel(hotel_id: int, _: DependsAdminOrOwner) -> None:
    await delete_hotel(hotel_id=hotel_id)