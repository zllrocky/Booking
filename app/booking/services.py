from uuid import UUID

from fastapi import HTTPException

from app.booking.dao import BookingDAO
from app.booking.schemas import SAddBooking, SBooking, SUpdateBooking
from app.rooms.dao import RoomsDAO


async def get_bookings_for_id(booking_id: UUID, user_id: UUID) -> SBooking:
    result = await BookingDAO.find_one_or_none(booking_id=booking_id, user_id=user_id)
    if not result:
        raise HTTPException(status_code=404, detail='Not found')
    return result


async def get_all_user_bookings(user_id: UUID) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user_id)


async def add_bookings(user_id: UUID, booking_data: SAddBooking) -> SBooking:
    booking_dict = booking_data.model_dump()
    total_days = (booking_data.date_to - booking_data.date_from).days
    room = await RoomsDAO.find_one_or_none(room_id=booking_data.room_id)
    if not room:
        raise HTTPException(status_code=404, detail='Not found')

    existing_booking = await BookingDAO.check_overbooking(
        room_id=booking_data.room_id,
        date_from=booking_data.date_from,
        date_to=booking_data.date_to
    )
    if existing_booking:
        raise HTTPException(status_code=409, detail='The room is already booked for these dates')

    total_cost = total_days * room.price
    return await BookingDAO.add(user_id=user_id, **booking_dict,price=room.price,
                                total_days=total_days,  total_cost=total_cost)


async def patch_booking(booking_id: UUID, user_id: UUID, booking_data: SUpdateBooking) -> SBooking:
    existing_booking = await BookingDAO.find_one_or_none(booking_id=booking_id, user_id=user_id)
    if not existing_booking:
        raise HTTPException(status_code=404, detail='Booking not found')

    overbooking = await BookingDAO.check_overbooking(
        room_id=existing_booking.room_id,
        date_from=booking_data.date_from,
        date_to=booking_data.date_to,
        booking_id=booking_id
    )
    if overbooking:
        raise HTTPException(status_code=409,
                            detail='Room is already booked for these dates')

    booking_dict = booking_data.model_dump(exclude_unset=True)
    update_booking = await BookingDAO.update(filter_by={'booking_id': booking_id, 'user_id': user_id},
                                        data=booking_dict)
    return update_booking


async def delete_bookings(booking_id: UUID, user_id: UUID) -> None:
    result = await BookingDAO.delete(booking_id=booking_id, user_id=user_id)
    if not result:
        raise HTTPException(status_code=404, detail='Booking not found')