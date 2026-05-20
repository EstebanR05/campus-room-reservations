from typing import Optional

from pydantic import BaseModel


class MessageResponse(BaseModel):
    message: str


class PaginationQuery(BaseModel):
    limit: int = 50
    skip: int = 0


class UserActionHeader(BaseModel):
    x_user_id: Optional[str] = None
