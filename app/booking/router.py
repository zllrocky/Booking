from uuid import UUID
from fastapi import APIRouter

from app.booking.schemas import SBooking, SAddBooking, SUpdateBooking
from app.booking.services import (get_all_user_bookings, add_bookings, delete_bookings,
                                  get_bookings_for_id, patch_booking)
from app.dependencies import DependsAdminOrUser


router = APIRouter(prefix='/bookings', tags=['Bookings'])


@router.get('/{booking_id}', summary='[ADMIN / USER] Get booking',
            description='**Access:** Authorized users and Administrators.\n'
                        'Returns the details of a specific booking by its ID.')
async def get_booking(booking_id: UUID, user: DependsAdminOrUser) -> SBooking:
    return await get_bookings_for_id(booking_id=booking_id, user_id=user.id)


@router.get('', summary='[ADMIN / USER] Get all bookings',
            description='**Access:** Authorized users and Administrators.\n'
                        'Returns a list of all bookings made by the authorized user.')
async def get_booking_info(user: DependsAdminOrUser) -> list[SBooking]:
    return await get_all_user_bookings(user_id=user.id)


@router.post('', status_code=201, summary='[ADMIN / USER] Add a booking',
             description='**Access:** Authorized users and Administrators.\n'
                         'Creates a new booking. Automatically checks whether the room '
                         'is available for the selected dates.')
async def add_new_booking(booking_data: SAddBooking,
                          user: DependsAdminOrUser) -> SBooking:
    return await add_bookings(booking_data=booking_data, user_id=user.id)


@router.patch('/{booking_id}', summary='[ADMIN / USER] Update booking dates',
              description='**Access:** Authorized users and Administrators.\n'
                          'Changes the check-in and check-out dates. '
                          'Checks for overlaps with other bookings.')
async def update_booking(booking_id: UUID, booking_data: SUpdateBooking,
                         user: DependsAdminOrUser) -> SBooking:
    return await patch_booking(booking_id=booking_id, user_id=user.id,
                               booking_data=booking_data)


@router.delete('/{booking_id}', status_code=204, summary='[ADMIN / USER] Cancel booking',
               description='**Access:** Authorized users and Administrators.\n'
                           'Permanently deletes a specific booking.')
async def del_booking(booking_id: UUID, user: DependsAdminOrUser) -> None:
    await delete_bookings(booking_id=booking_id, user_id=user.id)