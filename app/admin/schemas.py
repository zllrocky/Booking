from pydantic import BaseModel

from app.users.models import Role


class SAdminUpdateStatus(BaseModel):
    role: Role


class SAdminUpdateIsActive(BaseModel):
    is_active: bool


