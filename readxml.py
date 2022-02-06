import xml.etree.ElementTree as ET

tree = ET.parse("../custom-rc.xml")
root = tree.getroot()

prefix = "{http://openbox.org/3.4/rc}"
obe = lambda target: prefix + target
stripElement = lambda e: e.split("}", 1)[1]


def checkIfIter(it):
    try:
        ia = iter(it)
        nx = ia.__next__()
        return nx is not None and not isinstance(nx, str)
    except Exception:
        return False


def traverseNestedAction(child, result):
    cv = child
    while checkIfIter(cv):
        ctag = stripElement(cv.tag)

        def fetch(c):
            a = c.attrib
            if "name" in a:
                return a.get("name")
            return a

        nest = list(map(fetch, cv))
        result.append({ctag: nest})
        # result.append(nest)

        cv = iter(child).__next__()


# limitation can only see through 3 level
def getKeybinds():
    keyboard = root.find(obe("keyboard"))
    if keyboard is None:
        return {}
    keybinds = keyboard.findall(obe("keybind"))
    keys = list(map(lambda e: e.attrib, keybinds))

    pairsbind = dict()

    for i, keybind in enumerate(keybinds):
        getAction = keybind.find(obe("action"))

        if getAction is not None:

            innerAction = list()

            for child in getAction:
                tag = stripElement(child.tag)
                if checkIfIter(child):
                    traverseNestedAction(child, result=innerAction)
                    child = iter(child).__next__()
                    continue

                if child.text is not None:
                    txt = child.text.strip()
                    if child.text == "none":
                        txt = False
                    elif len(txt) == 0:
                        innerAction.append(tag)
                        continue
                    innerAction.append({tag: txt})
                else:
                    innerAction.append(tag)

            mainAction = getAction.attrib.get("name")
            pair = {mainAction: innerAction}

            k = keys[i].get("key")

            if len(innerAction) > 0:
                pairsbind[k] = pair
            else:
                pairsbind[k] = mainAction

    return pairsbind


def getMouseBinding():
    res = dict()
    mouse = root.find(obe("mouse"))
    if mouse is None:
        return
    mouseContext = mouse.findall(obe("context"))
    for _, element in enumerate(mouseContext):
        mousebinds = element.findall(obe("mousebind"))

        def deserializeMb(mousebind):
            mbObj = dict()
            getAction = mousebind.findall(obe("action"))
            attr = mousebind.attrib

            fetchName = lambda action: action.get("name")
            actions = list(map(fetchName, getAction))

            mbObj["button"] = attr["button"]
            mbObj["event"] = attr["action"]
            mbObj["actions"] = actions
            return mbObj

        mbs = list(map(deserializeMb, mousebinds))
        res[element.get("name")] = mbs
    return res


# transpile back to json
# read from the main rc
import json

with open("../mousebind.json", "w") as f:
    kb = getMouseBinding()
    ctx = {"contexts": kb}
    kb = {"mouse": ctx}
    json.dump(kb, f)
