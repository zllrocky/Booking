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


async def check_status_partnership(user_id: UUID) -> list[SPartnershipsRequestResponse]:
    return await PartnershipsDAO.find_all(user_id=user_id)


async def get_all_status_partnership(status: RequestStatus | None = None
                                     ) -> list[SPartnershipsRequestResponse]:
    return await PartnershipsDAO.find_all(status=status)


async def get_partnership_for_id(partnership_id: int) -> SPartnershipsRequestResponse:
    current_partnership = await PartnershipsDAO.find_one_or_none(id=partnership_id)
    if not current_partnership:
         raise HTTPException(status_code=404, detail='Not found')
    return current_partnership


async def update_status_partnership(partnership_id: int,
                                    status: RequestStatus
                                    ) -> SPartnershipsRequestResponse:
    current_id = await PartnershipsDAO.find_one_or_none(id=partnership_id)
    if not current_id:
        raise HTTPException(status_code=404, detail='Not found')
    update_status = await PartnershipsDAO.update(filter_by={'id': partnership_id},
                                                 data={'status': status})
    return update_status


async def delete_partnership_status(partnership_id: int) -> None:
    result = await PartnershipsDAO.delete(id=partnership_id)
    if not result:
        raise HTTPException(status_code=404, detail='Not found')