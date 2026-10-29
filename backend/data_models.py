from pydantic import BaseModel
from typing import *


class BasePostQuery(BaseModel):
    cond: dict[str, Any]

class ClassroomQueryModel(BaseModel):
    cond: dict[str, Any] = {}
    available_only: bool = False

class ClassroomManagementModel(BaseModel):
    code: str
    id: str
    display: str
    place: str
    pic_url: str = ""
    func_tag: str = ""
    available: bool = True


class ClassroomDeletionModel(BaseModel):
    code: str
    id: str


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


class GrantAccessModel(BaseModel):
    uid: str
    display: str
    password: str


class UserAlterModel(BaseModel):
    uid: str
    display: str
    permission: list[str]


class RecordAlterModel(BaseModel):
    record_id: int
    noon: bool
    time_stamp: int


class CyclicalDeletionModel(BaseModel):
    initiator: str
