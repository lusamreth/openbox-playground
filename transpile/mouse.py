import xml.etree.ElementTree as ET
from utils import *

# defining clear structure
from dataclasses import dataclass, asdict


@dataclass
class MousebindObj:
    button: str
    event: str
    actions: list


def buildcreateMousebind(context):
    mbind = ET.SubElement(context, "mousebind")

    def mb(button, actionNode: dict):
        mbind.set("button", button)
        actionElement = ET.SubElement(mbind, "action")
        for action in actionNode:
            # print("actionss => m",action)
            actionElement.set("name", action)

            if hasattr(actionNode, "__iter__"):
                for key in actionNode[action]:
                    makeAction(actionElement, key, actionNode[action][key])
            actionNode[action]
        return mbind

    return mb


class Mouse:
    def __init__(self, outputTarget):
        o = buildXmlAccess(root="mouse", outputTarget=outputTarget)
        self.mouseElement = o["rootElement"]
        self.targetFd = o["targetFd"]

    def createContext(self, name):
        mouse = self.mouseElement
        context = ET.SubElement(mouse, "context")
        context.set("name", name)
        return context

    def bind(self, mbobj: MousebindObj, ctx):
        mousebindElement = ET.SubElement(ctx, "mousebind")
        obj = asdict(mbobj)
        btn = obj["button"]
        action = obj["event"]

        mousebindElement.set("button", btn)
        mousebindElement.set("action", action)

        actions = obj["actions"]
        # processing actions Node [arr]:
        for action in actions:
            actionElement = ET.SubElement(mousebindElement, "action")
            if isinstance(action, dict):
                for key in action:
                    actionElement.set("name", key)
            else:
                actionElement.set("name", action)

    def writeTofile(self):
        print("WRITING TO FILE!")
        f = self.targetFd
        f.write(ET.tostring(self.mouseElement))


def processMousebindObj(mouseObj, mbObj_arr, context):
    toMbObj = lambda mbDict: MousebindObj(
        mbDict["button"], mbDict["event"], mbDict["actions"]
    )

    for mbDict in mbObj_arr:
        mouseObj.bind(toMbObj(mbDict), context)


def deserializeMouseJson(jsonDict, outputTo, config={"root": True}):
    r = jsonDict
    if config["root"]:
        r = jsonDict["mouse"]

    mouseCtx = r["contexts"]
    print("outputTo", outputTo)
    mouseObj = Mouse(outputTo)
    for ctx in mouseCtx:
        context = mouseObj.createContext(ctx)
        mbObj_arr = mouseCtx[ctx]
        processMousebindObj(mouseObj, mbObj_arr, context)
    mouseObj.writeTofile()


# in mouse root contains multiple contexts
# available contexts : Frame,Client,Desktop,Root,Titlebar,Icon
# Top,Bottom,Left,Right,Iconify,Shade,MoveResize,Maximize,Close
# TLCorner, TRCorner, BLCorner, BRCorner
# Moreinfo in openbox docs:
# http://openbox.org/wiki/Help:Bindings#Context

# each context contain indivdual bind
# mouse bind object contains :
# button,event,actions
# Additional config for deseralization:
# require-root mean in json should start with :
# {mouse : {contexts...}} ; default : true
# else {
# contexts : [ binds... ]
# }
# ignore-contexts-prefix : after iterate root context level
# could be skipped; ie {mouse:{contexts:{....}}};default : false

# convert to json
import json

mb = open(
    "../../mouse.json",
)
j = json.load(mb)

deserializeMouseJson(jsonDict=j, outputTo="mouse")
# mbj = MousebindObj("w-a","click",["bruh"])
