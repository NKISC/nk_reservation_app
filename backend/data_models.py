from pydantic import BaseModel
from typing import *


class BasePostQuery(BaseModel):
    cond: dict[str, Any]


class PermissionCheckQuery(BaseModel):
    permissions: list[str]
    classrooms: list[str]
