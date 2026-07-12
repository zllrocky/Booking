from fastapi import FastAPI

from app.users.router import router as users_router
from app.auth.router import router as auth_router
from app.hotels.router import router as hotels_router


app = FastAPI(title="Booking")


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(hotels_router)