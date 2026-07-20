from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from app.partnerships.models import RequestStatus
from datetime import datetime

class SPartnershipsRequestCreate(BaseModel):
    company_name: str
    tax_id: str
    contact_phone: PhoneNumber
    contact_email: EmailStr


class SPartnershipsRequestResponse(SPartnershipsRequestCreate):
    id : int
    status: RequestStatus
    created_at: datetime