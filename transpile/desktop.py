import xml.etree.ElementTree as ET
from dataclasses import dataclass
import utils
from typing import Generic, TypeVar, Optional


@dataclass
class Desktops:
    number: int
    names: list[str]
    firstdesk: int
    popUpTime: int
