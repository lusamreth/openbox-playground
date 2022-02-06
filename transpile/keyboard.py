from dataclasses import dataclass
import utils
import translator
import dicto
from typing import Generic, TypeVar, Optional

T = TypeVar("T")


@dataclass
class Keybind(Generic[T]):
    action: str
    key: str
    chain: Optional[T]
    chroot: bool


@dataclass
class Keyboard:
    keybinds: list[Keybind]
    configs: Optional[dict]
    chainQuitKey: str


# b = xmltodict.unparse({"keyboard": res}, pretty=True)
# print("res", b)
