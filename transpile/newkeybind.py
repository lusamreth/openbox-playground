import xml.etree.ElementTree as ET

# defining clear structure
from dataclasses import dataclass, asdict
from utils import *

import json


@dataclass
class Action:
    name: str
    options: dict


# support emacs keychain
@dataclass
class KeybindObj:
    key: str
    action: Action


class Keyboard:
    def __init__(self, output):
        o = buildXmlAccess(root="keyboard", outputTarget=output)
        self.keyboardElement = o["rootElement"]
        self.targetFd = o["targetFd"]

    # bind function use on each element!
    def bind(self, keyObj: KeybindObj, parent=None):
        obj = asdict(keyObj)
        if parent is None:
            parent = self.keyboardElement

        rootkb = ET.SubElement(parent, "keybind")
        rootkb.set("keybind", obj["key"])

        action = ET.SubElement(rootkb, "action")
        action.set("name", obj["action"]["name"])
        return rootkb

    def writeToFile(self):
        f = self.targetFd
        f.write(ET.tostring(self.keyboardElement))


# bruh
mb = open("../../keybinds.json", "r")
j = json.load(mb)
k = Keyboard("keybinds")


def makeAction(keybind):
    action = keybind["action"]
    return Action(action["name"], action.get("options") or {})


def read_config():
    configs = j["configs"]
    quitstr = "chainQuitKey"
    qk = configs.get(quitstr)
    print(qk)

    if qk is not None:
        obj = KeybindObj(qk, makeAction({"action": {"name": "quitstr"}}))
        k.bind(obj)

    return {"chroot": configs.get("chroot")}


def read_key_config():
    keybinds = j["keybinds"]
    configs = read_config()

    for key, value in keybinds.items():

        keybind = keybinds[key]
        chained = value.get("chains")

        obj = KeybindObj(key, makeAction(keybind))

        kbind = k.bind(obj)

        if chained is not None:
            if configs.get("chroot"):
                kbind.set("chroot", "true")

            for chainkey in chained:
                inner = chained[chainkey]
                makeAction(inner)
                chainObj = KeybindObj(chainkey, makeAction(inner))
                k.bind(chainObj, parent=kbind)


read_key_config()
k.writeToFile()
