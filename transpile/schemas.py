from dataclasses import dataclass
import utils
from typing import Generic, TypeVar, Optional
import xml.etree.ElementTree as ET


@dataclass
class Desktops:
    number: int
    names: list[str]
    firstdesk: int
    popUpTime: int


@dataclass
class Mousebind:
    button: str
    triggerAction: str
    actions: list[str]


@dataclass
class Contexts:
    name: str
    mousebind: list[Mousebind]


# +dragThreshold How many pixels you need to drag for it to be
# recognized as a drag operation.

# +doubleClickTime Time (in milliseconds) allowed between two separate clicks
# to register as a DoubleClick.

# +screenEdgeWarpTime Time (in milliseconds) to pause between two consecutive
# desktop switches done by holding the cursor next to the screen edge.
# Set to 0 to disable this feature.


@dataclass
class MouseConfigs:
    dragThreshold: str
    doubleClickTime: str
    screenEdgeWarpTime: str


@dataclass
class Mouse:
    contexts: Contexts
    configs: MouseConfigs


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
    configs: str
    chainQuitKey: str


Form = {"mouse": Mouse, "desktop": Desktops, "keyboard": Keyboard}


def process_chain_key(root, chain):
    passed = utils.validate_field(Keybind, chain)


import translator

# button: str
# triggerAction: str
# actions: list[str]

mouscfg = {
    "name": "bruh",
    "contexts": {
        "name": "bruh",
        "mousebinds": [
            {
                "button": "D",
                "triggerAction": "bru",
                "actions": ["shad", "bruh"],
            },
            {
                "button": "E",
                "triggerAction": "heheh",
                "actions": ["osa", "s"],
            },
        ],
    },
    "ps": "10",
}


def context_attrib_replacement(data):
    data_ctx = data["contexts"]
    mb = data_ctx["mousebinds"]

    def replace(dt, old, new):
        dt[new] = dt.pop(old)

    replace(data_ctx, "name", "@name")
    # data_ctx["@name"] = data_ctx.pop("name")

    for m in mb:
        replace(m, "triggerAction", "@action")
        replace(m, "button", "@button")

    return data


def mousebind_injector(data):

    p = utils.flatten(data, ["contexts"])

    # return flatten(kbind, ["chain"])
    res = []
    for action_obj in p["mousebinds"]:
        for action in action_obj["actions"]:
            xml_output = ET.Element("action", {"name": action})
            loca = "contexts/mousebinds[@action='{}']".format(
                action_obj["@action"]
            )

            res.append({"location": loca, "data": xml_output})

            print("Pine", xml_output)
        action_obj.pop("actions")

    return res

    # print(ET.tostring(res[0]))
    # mbs = p["contexts"]["mousebinds"]
    # for mb in mbs:
    #     print(mb)
    # data["contexts"]["name"]


b = (
    translator.CreateSchema(Mouse, mouscfg)
    .permuate([context_attrib_replacement])
    .hook([mousebind_injector])
    .call("Mouse")
)
print(ET.tostring(b))


# Global actions
# Execute
# 1 Startup notification
# ShowMenu
# NextWindow
# PreviousWindow
# DirectionalCycleWindows
# DirectionalTargetWindow
# GoToDesktop
# AddDesktop
# RemoveDesktop
#  ToggleShowDesktop
#  ToggleDockAutohide
#  Reconfigure
#  Restart
#  Exit
#  SessionLogout
#  Debug
# ndow actions
# Focus
# Raise
# Lower
# RaiseLower
# Unfocus
# FocusToBottom
# Iconify
# Close
# ToggleShade
#  Shade
#  Unshade
#  ToggleOmnipresent
#  ToggleMaximize
#  Maximize
#  Unmaximize
#  ToggleFullscreen
#  ToggleDecorations
#  Decorate
#  Undecorate
#  SendToDesktop
#  Move
#  Resize
#  MoveResizeTo
#  MoveRelative
#  ResizeRelative
#  MoveToEdge
#  GrowToEdge
#  GrowToFill
#  ShrinkToEdge
#  If
#  ForEach
#  Stop
#  ToggleAlwaysOnTop
#  ToggleAlwaysOnBottom
#  SendToLayer
