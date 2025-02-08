from pydantic import BaseModel
from typing import *


class BasePostQuery(BaseModel):
    cond: dict[str, Any]
