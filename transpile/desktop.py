import xml.etree.ElementTree as ET
import utils

import translator
from dataclasses import dataclass
from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, Field, validator, ValidationError


class Desktops(BaseModel):
    number: int
    names: list[str]
    firstdesk: int
    popUpTime: Optional[int] = 100

    @validator("popUpTime", pre=True, always=True)
    def check_popup(cls, v):
        if v:
            assert v >= 100, "Must be at least 100 milliseconds"
        return v or 100

    @validator("number")
    def check_valid_number(cls, v):
        limit = 12
        message = """A lot of desktops isvery difficult to manage! Constrained
        to{}""".format(
            limit
        )

        assert v <= limit, message
        return v or 6


DKD = {
    "number": 1,
    "names": ["sda"],
    "firstdesk": 1,
}
res = translator.CreateSchema(Desktops, DKD).call("OK")

print("RSl", ET.tostring(res))
