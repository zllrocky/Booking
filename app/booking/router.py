from uuid import UUID

from fastapi import APIRouter, Depends

from app.auth.auth import get_current_active_user
from app.booking.schemas import SBooking, SAddBooking, SUpdateBooking
from app.booking.services import (get_all_user_bookings, add_bookings, delete_bookings,
                                  get_bookings_for_id, patch_booking)
from app.users.models import Users

router = APIRouter(prefix='/bookings', tags=['Bookings'])

@router.get('/{booking_id}', summary='Get booking',
            description='Returns the details of a specific booking by its ID')
async def get_booking(booking_id: UUID, user: Users = Depends(get_current_active_user)) -> SBooking:
    return await get_bookings_for_id(booking_id=booking_id, user_id=user.id)


@router.get('', summary='Get all bookings',
            description='Returns a list of all bookings made by an authorised user')
async def get_booking_info(user: Users = Depends(get_current_active_user)) -> list[SBooking]:
    return await get_all_user_bookings(user_id=user.id)


@router.post('', status_code=201, summary='Add a booking',
             description='Creates a new booking. Checks whether a room is available for the selected dates')
async def add_new_booking(booking_data: SAddBooking,
                          user: Users = Depends(get_current_active_user)) -> SBooking:
    return await add_bookings(booking_data=booking_data, user_id=user.id)


@router.patch('/{booking_id}', summary='Update booking dates',
              description='Changes the check-in and check-out dates. Checks for overlaps with other bookings')
async def update_booking(booking_id, booking_data: SUpdateBooking,
                         user: Users = Depends(get_current_active_user)) -> SBooking:
    return await patch_booking(booking_id=booking_id, user_id=user.id,
                               booking_data=booking_data)


@router.delete('/{booking_id}', status_code=204, summary='Cancel booking',
               description='Permanently deletes a user’s booking')
async def del_booking(booking_id: UUID, user: Users = Depends(get_current_active_user)) -> None:
    await delete_bookings(booking_id=booking_id, user_id=user.id)