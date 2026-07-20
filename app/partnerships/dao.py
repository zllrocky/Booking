from app.dao.base import BaseDAO
from app.partnerships.models import PartnershipsRequests


class PartnershipsDAO(BaseDAO):
    model = PartnershipsRequests