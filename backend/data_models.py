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

class CyclicalRecordAdditionModel(BaseModel):
    classroom: str
    noon: bool
    applicant_id: str
    beginning_time_stamp: int
    ending_time_stamp: int
    days: list[bool]

class UserAdditionModel(BaseModel):
    display_name: str
    permissions: str


class LoginModel(BaseModel):
    code: str


class UserAlterModel(BaseModel):
    uid: str
    display: str
    permission: list[str]


class RecordAlterModel(BaseModel):
    record_id: int
    noon: bool
    time_stamp: int
