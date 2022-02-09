from dataclasses import dataclass
from typing import Generic, List, TypeVar, Optional, List, Annotated
from pydantic.class_validators import root_validator

from pydantic.generics import GenericModel
from pydantic import BaseModel, validator
from pydantic.types import OptionalInt


from .validators import (
    check_field_is_valid_obs_value,
    convert_field_to_attr,
    set_default_values,
    remove_empty,
    replace_field_name,
)


class Desktops(BaseModel):
    number: int
    names: Optional[list[str]]
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

    _no_empty = remove_empty()


# +dragThreshold How many pixels you need to drag for it to be
# recognized as a drag operation.

# +doubleClickTime Time (in milliseconds) allowed between two separate clicks
# to register as a DoubleClick.

# +screenEdgeWarpTime Time (in milliseconds) to pause between two consecutive
# desktop switches done by holding the cursor next to the screen edge.
# Set to 0 to disable this feature.


class MouseConfigs(BaseModel):
    dragThreshold: str
    doubleClickTime: str
    screenEdgeWarpTime: str


def check_allow_value(val, allow):
    s = val.strip()
    if s not in allow:
        print(
            "{name} {} is not in valid {name} list {}".format(
                val, repr(allow), name="bruh"
            )
        )
        raise ValueError


class Mousebind(BaseModel):
    button: str
    event: str
    actions: list[str]

    _validate_valid_values = check_field_is_valid_obs_value(
        ["event", "actions"]
    )


class Context(BaseModel):
    name: str
    mousebinds: list[Mousebind]

    _validate_valid_values = check_field_is_valid_obs_value(
        ["name:context"]
    )


class Mouse(BaseModel):
    contexts: list[Context]
    configs: Optional[MouseConfigs]
    _no_empty = remove_empty()


T = TypeVar("T")


class Action(BaseModel):
    name: str
    misc: Optional[dict]

    _check_allow = check_field_is_valid_obs_value(["name:actions"])
    _no_empty = remove_empty()
    _attr = convert_field_to_attr(["name"])


class Keybind(GenericModel, Generic[T]):
    action: Action
    key: str
    chain: Optional[T]
    chroot: Optional[bool]

    @validator("action", pre=True, always=True)
    def make_action(value):
        if isinstance(value, str):
            return Action(name=value, misc=None)
        elif isinstance(value, dict):
            name = value["name"]
            del value["name"]
            return Action(name=name, misc=value)
        return value

    _attr = convert_field_to_attr(["key"])
    _no_empty = remove_empty()


class Keyboard(BaseModel):
    keybinds: list[Keybind]
    configs: Optional[dict]
    chainQuitKey: str

    _no_empty = remove_empty()
    _replacement = replace_field_name({"keybinds": "keybind"})


# class Maximise(Enum):
#     VERTICAL = auto(),
#     HORIZONTAL = auto(),
#     BOTH = auto(),
#     NONE = auto()

# class Layer(Enum):
#     NORMAL = auto(),
#     ABOVE = auto(),
#     BELOW = auto(),


class Style(BaseModel):
    decore: Optional[bool]
    shade: Optional[bool]
    focus: Optional[bool]

    _no_none = remove_empty()


class Position(BaseModel):
    force: bool
    x: int
    y: int

    _attr = convert_field_to_attr(["force"])


class Skippable(BaseModel):
    pager: bool
    taskbar: bool


class Identifier(BaseModel):
    classname: str
    # could use either class or name
    type: Optional[str]
    name: Optional[str]

    _replace = replace_field_name({"classname": "class"})
    # after replacing the field_name the next validators
    # must comply with new field instead of old one!!
    _no_empty = remove_empty()
    _attr = convert_field_to_attr(["class", "type", "name"])


class AppSetting(BaseModel):
    id: Identifier
    layer: Optional[str]
    # Optional stuff
    desktop: OptionalInt
    style: Optional[Style]
    position: Optional[Position]
    iconify: Optional[bool]
    maximise: Optional[bool]
    skip: Optional[Skippable]
    size: Optional[list]

    _no_empty = remove_empty()


class Applications(BaseModel):
    application: list[AppSetting]
    _no_empty = remove_empty()


class Font(BaseModel):
    name: str
    size: int
    weight: Optional[str]
    slant: Optional[str]
    # attr
    place: Optional[str]

    _defaults = set_default_values(
        {"weight": "normal", "slant": "normal"}
    )
    _no_empty = remove_empty()
    _convert_attributes = convert_field_to_attr(["place"])


class Theme(BaseModel):
    name: str
    fonts: List[Font]
    titleLayout: str

    _no_empty = remove_empty()


Pair = Annotated[List[int], 2]
Quad = Annotated[List[int], 4]


class Resize(BaseModel):
    popupFixedPosition: Optional[Pair]
    drawContents: bool
    popupShow: str
    popupPosition: str


class Margin(BaseModel):
    value: Quad


class Resistance(BaseModel):
    strength: int
    screen_edge_strength: int


class Focus(BaseModel):
    focusNew: bool
    focusLast: bool
    raiseOnFocus: bool
    focusDelay: int
    followMouse: bool


class Placement(BaseModel):
    primaryMonitor: int
    policy: str
    monitor: str


DefaultSetting = {
    "focus": {
        "focusNew": True,
        "focusLast": True,
        "focusDelay": "50",
        "followMouse": True,
        "raiseOnFocus": True,
    },
    "placement": {
        "primaryMonitor": 1,
        "policy": "smart",
        "monitor": "Primary",
    },
    "resize": {
        "popupPosition": "center",
        "drawContents": True,
        "popupShow": "Nonpixel",
    },
    "margins": [0, 0, 0, 0],
}


class RootSetting(BaseModel):
    resistance: Resistance
    focus: Optional[Focus]
    placement: Optional[Placement]
    resize: Optional[Resize]
    margins: Optional[Quad]
    # xmlns = "http://openbox.org/3.4/rc"

    @root_validator(pre=True)
    def focus_default(cls, values):
        RootVar = ("focus", "placement", "resize", "margins")
        for var in RootVar:
            inner_val = values.get(var)
            default = DefaultSetting[var]
            if inner_val is None:
                values[var] = DefaultSetting[var]
            else:
                if isinstance(default, dict):
                    default.update(values[var])
                    values[var] = default
                elif isinstance(default, list):
                    b = len(values[var])
                    d = len(default)
                    z = default[b:d]
                    values[var].extend(z)

        return values

    @validator("margins", always=True)
    def margin_set(value):
        slot = ["top", "bottom", "left", "right"]
        marg = {}
        for i, v in enumerate(value):
            marg[slot[i]] = v
        return marg

    _no_empty = remove_empty()


# <menu>
#   <hideDelay>250</hideDelay>
#   <middle>no</middle>
#   <submenuShowDelay>100</submenuShowDelay>
#   <submenuHideDelay>400</submenuHideDelay>
#   <applicationIcons>yes</applicationIcons>
#   <manageDesktops>yes</manageDesktops>
#   <file>menu.xml</file>
# </menu>


class Menu(BaseModel):
    hideDelay: int
    middle: bool
    submenuShowDelay: int
    submenuHideDelay: int
    applicationIcons: bool
    file: "str"


# _replace = replace_field_name({"focus": "xd"})


# _no_empty = remove_empty()

# xmlns="http://openbox.org/3.4/rc" xmlns:xi="http://www.w3.org/2001/XInclude"

# <resize>
# <drawContents>yes</drawContents>
# <popupShow>Nonpixel</popupShow>
# <!--  'Always', 'Never', or 'Nonpixel' (xterms and such)  -->
# <popupPosition>Center</popupPosition>
# <!--  'Center', 'Top', or 'Fixed'  -->
# <popupFixedPosition>
# <!--  these are used if popupPosition is set to 'Fixed'  -->
# <x>10</x>
# <!--  positive number for distance from left edge, negative number for
#          distance from right edge, or 'Center'  -->
# <y>10</y>
# <!--  positive number for distance from top edge, negative number for
#          distance from bottom edge, or 'Center'  -->
# </popupFixedPosition>
# </resize>
# <!--  You can reserve a portion of your screen where windows will not cover when
#      they are maximized, or when they are initially placed.
#      Many programs reserve space automatically, but you can use this in other
#      cases.  -->
# <margins>
# <top>0</top>
# <bottom>0</bottom>
# <left>0</left>
# <right>0</right>
# </margins>
