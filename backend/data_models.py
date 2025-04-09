from pydantic import BaseModel
from typing import *


class BasePostQuery(BaseModel):
    cond: dict[str, Any]


class PermissionCheckQuery(BaseModel):
    permissions: list[str]
    classrooms: list[str]


class AdditionModel(BaseModel):
    classrooms: str
    noon: bool
    applicant_id: str
    time_stamp: int
