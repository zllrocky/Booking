from fastapi import FastAPI

from app.users.router import router as users_router
from app.auth.router import router as auth_router
from app.hotels.router import router as hotels_router
from app.rooms.router import router as rooms_router
from app.booking.router import router as bookings_router
from app.partnerships.router import router as partnerships_router

app = FastAPI(title="Booking")


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(bookings_router)
app.include_router(partnerships_router)