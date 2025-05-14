from pydantic import BaseModel
from typing import *


class BasePostQuery(BaseModel):
    cond: dict[str, Any]


class PermissionCheckQuery(BaseModel):
    permissions: list[str]
    classrooms: list[str]


class RecordAdditionModel(BaseModel):
    classroom: str
    noon: bool
    applicant_id: str
    time_stamp: int

class UserAdditionModel(BaseModel):
    display_name: str
    permissions: str