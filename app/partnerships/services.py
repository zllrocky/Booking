from uuid import UUID
from fastapi import HTTPException

from app.partnerships.models import RequestStatus
from app.partnerships.schemas import SPartnershipsRequestCreate, SPartnershipsRequestResponse
from app.partnerships.dao import PartnershipsDAO


async def create_partnership_request(partnership_data: SPartnershipsRequestCreate,
                                     user_id: UUID) -> SPartnershipsRequestResponse:
    existing_request = await PartnershipsDAO.find_one_or_none(
        user_id=user_id, status=RequestStatus.PENDING)

    if existing_request:
        raise HTTPException(status_code=400,
            detail='You already have a request under review.')

    data_to_insert = partnership_data.model_dump()
    data_to_insert['user_id'] = user_id
    new_request = await PartnershipsDAO.add(**data_to_insert)
    return new_request


async def check_status_partnership(user_id: UUID):
    return await PartnershipsDAO.find_all(user_id=user_id)
