import xml.etree.ElementTree as ET
import json
from os.path import exists

from copy import deepcopy


def flatten(dictionary, skips):
    newobj = deepcopy(dictionary)
    assert isinstance(dictionary, dict)

    # if dictionary.get("convertible") is None:
    #     return dictionary

    for skip in skips:
        pi = dictionary.get(skip)
        if pi:
            newobj.update(pi)

    # newobj.pop("convertible")

    return newobj


def create_action(mapper, action_obj):
    EP = None

    def adder(k, itm):
        sube = ET.SubElement(EP, k[1:])
        sube.set("name", itm)

    def chain(_, itm):
        assert EP is not None
        poi = create_action(mapper, itm)
        EP.insert(0, poi)

    SkipVar = {"@": adder, "?": chain}

    for k, map in mapper.items():

        itm = action_obj.get(map)
        pine = list(filter(lambda a: a == k[0], SkipVar))

        if k[0] in SkipVar and itm is not None:
            SkipVar[k[0]](k, itm)

        if k[0] != "?" and itm is None:
            print("iasd", k, mapper)
            raise Exception("bruh")
        if pine:
            continue

        EP = ET.Element(k, {})
    return EP


def xml_format(tar):
    return "{}.xml".format(tar)


class CreateXmlAccessService(object):
    def __init__(self, outputTarget, root, mode="wb"):
        self.target = outputTarget
        self.root = root

        fullFormat = xml_format(outputTarget)
        if not exists(fullFormat):
            self.mode = "x"
        else:
            self.mode = mode
        self.name = fullFormat

    def call(self):
        rootElement = ET.Element(self.root)
        targetFd = open(self.name, self.mode)
        return {"targetFd": targetFd, "rootElement": rootElement}


def makeAction(action, inneraction, cmd):
    inner = ET.SubElement(action, inneraction)
    inner.text = cmd


def combine_kv(keys, values):
    def not_list(a):
        return type(a) is not list

    if not_list(keys) and not_list(values):
        keys = [keys]
        values = [values]

    # default behavoir: leftover keys will be ignored!
    if len(keys) < len(values):
        raise Exception("Not enough keys to combine with value")

    res = {}
    for i, val in enumerate(values):
        res[keys[i]] = val
        # res[val] = keys[i]
    return res


class CreateDataService(object):
    def __init__(self, fd, root):
        self.fd = fd
        self.root = root

    def call(self):
        self.fd.write(ET.tostring(self.root))
        self.fd.close()

    # need to create Omit mechanism


def readJsonConfig(file):
    mb = open(file, "r")
    print("MB rad", mb)
    return json.load(mb)


def test_combine_kv():
    expected = {"key1": "val1", "key2": "val2"}
    res = combine_kv(["key1", "key2"], ["val1", "val2"])
    assert res == expected, "Incorrect!!"


# come up with a way to skip element and add attribute
# to each individual tag!!
# +Input: {
#   skips : ["configs","configs:threshold"]
#   Schemas :{
#     ** CONFIG NEED TO BE HIDDEN
#     configs: { <- only skip the first one!!
#         configs : [...]
#         threshold : 200,
#         chain : [...]
#     }
#   # schemas["configs"]
# }
# +Output : -> <configs>...</configs>, <threshold>200</threshold>,
# <chain>...</chain>
# }


if __name__ == "__main__":
    print("Everything passed")
