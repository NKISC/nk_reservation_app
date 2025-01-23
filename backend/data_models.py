from pydantic import BaseModel
from typing import *


class ClassroomQuery(BaseModel):
    cond: dict[str, Any]
