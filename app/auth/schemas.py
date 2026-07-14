from pydantic import BaseModel
from pydantic import EmailStr


class SToken(BaseModel):
    access_token: str
    token_type: str


class STokenData(BaseModel):
    email: EmailStr | None = None

