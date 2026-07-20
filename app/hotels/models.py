from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base
from app.rooms.models import Rooms


class Hotels(Base):
    __tablename__ = 'hotels'

    hotel_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    location: Mapped[str]
    latitude: Mapped[float]
    longitude: Mapped[float]
    rooms_quantity: Mapped[int]
    image_id: Mapped[int]
    services: Mapped[list[str]] = mapped_column(JSONB, nullable=True)

    rooms: Mapped[list["Rooms"]] = relationship(back_populates="hotel")