from fastapi import FastAPI
from app.users.router import router as auth_router


app = FastAPI(title="Booking")


app.include_router(auth_router)