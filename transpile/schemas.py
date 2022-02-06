from dataclasses import dataclass
import utils
from typing import Generic, TypeVar, Optional
import xml.etree.ElementTree as ET
from pydantic import (
    BaseModel,
    validator,
    ValidationError,
)

from pydantic.generics import GenericModel


@dataclass
class Desktops:
    number: int
    names: list[str]
    firstdesk: int
    popUpTime: int


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

    @validator("event")
    def validate_btn(cls, val):
        print("VAL", val)
        validbtn = [
            "Press",
            "Click",
            "DoubleClick",
            "Release",
            "Drag",
        ]
        check_allow_value(val, validbtn)

        return val


class Context(BaseModel):
    name: str
    mousebinds: list[Mousebind]

    @validator("name")
    def validate_ctx(cls, val):
        valid_contexts = [
            "Frame",
            "Client",
            "Desktop",
            "Root",
            "Titlebar",
            # "Top, Bottom, Left, Right",
            # "TLCorner, TRCorner, BLCorner, BRCorner",
            "Icon",
            "Iconify",
            "Maximize",
            "Close",
            "AllDesktops",
            "Shade",
            "MoveResize",
        ]

        check_allow_value(val, valid_contexts)
        return val


class Mouse(BaseModel):
    contexts: list[Context]
    configs: Optional[MouseConfigs]


T = TypeVar("T")


class Keybind(GenericModel, Generic[T]):
    action: str
    key: str
    chain: Optional[T]
    chroot: bool


class Keyboard(BaseModel):
    keybinds: list[Keybind]
    configs: Optional[dict]
    chainQuitKey: str


Form = {"mouse": Mouse, "desktop": Desktops, "keyboard": Keyboard}


def process_chain_key(root, chain):
    passed = utils.validate_field(Keybind, chain)


import translator

# button: str
# triggerAction: str
# actions: list[str]

mouscfg = {
    "contexts": [
        {
            "name": "Frame",
            "mousebinds": [
                {
                    "button": "Press",
                    "event": "Press",
                    "actions": ["shad", "bruh"],
                },
                {
                    "button": "Li",
                    "event": "DoubleClick",
                    "actions": ["osa", "s"],
                },
            ],
        },
        {
            "name": "Frame",
            "mousebinds": [
                {
                    "button": "Press",
                    "event": "Press",
                    "actions": ["shad", "bruh"],
                },
                {
                    "button": "Li",
                    "event": "DoubleClick",
                    "actions": ["osa", "s"],
                },
            ],
        },
    ],
}


def context_attrib_replacement(data):
    data_ctx = data["contexts"]

    def replace(dt, old, new):
        dt[new] = dt.pop(old)

    replace(data, "contexts", "context")
    for ctx in data_ctx:
        mbu = ctx["mousebinds"]
        replace(ctx, "name", "@name")
        replace(ctx, "mousebinds", "mousebind")

        for m in mbu:
            replace(m, "event", "@action")
            replace(m, "button", "@button")

    return data


def mousebind_injector(context_data):

    # print("Po", p)
    # return flatten(kbind, ["chain"])
    res = []
    for action_obj in context_data["mousebind"]:
        for action in action_obj["actions"]:
            xml_output = ET.Element("action", {"name": action})
            loca = "contexts/mousebinds[@action='{}']".format(
                action_obj["@action"]
            )

            res.append({"location": loca, "data": xml_output})

            print("Pine", xml_output)
        action_obj.pop("actions")
    print("res", res)

    return res


def walker(data):
    res = []
    for dt in data["context"]:
        res.append(mousebind_injector(dt))

    return res[0]
    # print(ET.tostring(res[0]))
    # mbs = p["contexts"]["mousebinds"]
    # for mb in mbs:
    #     print(mb)
    # data["contexts"]["name"]


b = (
    translator.CreateSchema(Mouse, mouscfg)
    .inject_mutations([context_attrib_replacement])
    .hook([walker])
    .call("Mouse")
)
print(ET.tostring(b))

import dicto


def a(dc):
    return dicto.flatten(dc, ["configs"])


res = (
    translator.CreateSchema(
        Keyboard,
        dicto.kbconf["Keyboard"],
    )
    .inject_mutations([a])
    .hook([dicto.convertKeybind])
    .call("keyboard")
)

print(ET.tostring(res))
