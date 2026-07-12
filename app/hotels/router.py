from fastapi import APIRouter, Depends

from app.auth.auth import get_current_active_user
from app.hotels.schemas import SHotel, SHotelAdd, SHotelUpdate
from app.hotels.services import get_all_info_hotels, get_hotel_info, add_hotel, \
    update_hotel_info, delete_hotel

router = APIRouter(prefix='/hotels', tags=['Hotels'])


@router.get('', summary='Get all hotels',
            description='Returns a list of hotels.<br>Can be optionally filtered by location'
                        ' or name. Returns full catalog if no filters are provided.')
async def get_all_hotels(location: str | None = None, name: str | None = None):
    return await get_all_info_hotels(location=location, name=name)


@router.get('/{hotel_id}', summary='Get hotel by ID',
            description='Returns detailed information about a specific hotel by its'
                        ' unique ID.<br> Returns 404 Not Found if the hotel does not exist.')
async def get_hotel(hotel_id: int):
    return await get_hotel_info(hotel_id=hotel_id)


@router.post('', status_code=201, response_model=SHotel, summary='Add new hotel',
             description='Creates a new hotel. ID is generated automatically.')
async def post_hotel(hotel_data: SHotelAdd, _ = Depends(get_current_active_user)):
    return await add_hotel(hotel_data)


@router.patch('/{hotel_id}', summary='Update hotel info',
              description='Partial update of hotel information.<br>'
                          'You can provide any combination of fields to update:<br>'
                          '-name: name of the hotel<br>'
                          '-location: address or city<br>'
                          '-services: list of available services<br>'
                          '-rooms_quantity: total number of rooms<br>'
                          '-image_id: ID of the image file')
async def update_hotel(hotel_id: int, hotel_data: SHotelUpdate,
                       _ = Depends(get_current_active_user)):
    return await update_hotel_info(hotel_id, hotel_data)


@router.delete('/{hotel_id}', status_code=204, summary='Delete hotel',
               description='Permanently delete a hotel from the database.'
                           'Warning: This action cannot be undone.<br>'
                           'The hotel will be removed from all listings and search results.')
async def remove_hotel(hotel_id: int, _ = Depends(get_current_active_user)):
    await delete_hotel(hotel_id=hotel_id)