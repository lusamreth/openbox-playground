import xml.etree.ElementTree as ET
import json
from os.path import exists

from copy import deepcopy


def replace(dt, old, new):
    dt[new] = dt.pop(old)


def flatten(dictionary, skips, strict=False):
    newobj = deepcopy(dictionary)
    assert isinstance(dictionary, dict)

    # if dictionary.get("convertible") is None:
    #     return dictionary

    for skip in skips:
        pi = dictionary.get(skip)
        if pi and not strict:
            print("PI", pi)
            newobj.update(pi)
            newobj.pop(skip)
        elif strict:
            raise ValueError(
                "Stict enabled! dict must contain the target skip value"
            )

    # newobj.pop("convertible")

    return newobj


def delete_none(_dict):
    """Delete None values recursively from all of
    the dictionaries, tuples, lists, sets"""

    if isinstance(_dict, dict):
        for key, value in list(_dict.items()):
            if isinstance(value, (list, dict, tuple, set)):
                _dict[key] = delete_none(value)
            elif value == {} or value is None or key is None:
                del _dict[key]

    elif isinstance(_dict, (list, set, tuple)):
        _dict = type(_dict)(
            delete_none(item) for item in _dict if item is not None
        )

    return _dict


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


def convert_each_action(inner):
    if isinstance(inner, dict):

        if inner.get("name") is not None:
            n = "name"
        else:
            n = "@name"

        name = {"@name": inner.pop(n)}
        inner = inner | name
        cop = {"action": inner}

        return cop

    return {"action": {"@name": inner}}


def action_list_converter(action_list):
    res = []
    for action in action_list:
        act = action.get("action")
        assert act is not None
        res.append(act)
    return {"action": res}


def flatten_misc(action_obj):
    action_obj = flatten(action_obj, ["misc"])

    for k, item in action_obj.items():

        if k != "@name":
            if isinstance(item, list):

                mama = list(map(convert_each_action, list(item)))

                print("FLAT INNER", mama)
                action_obj[k] = action_list_converter(mama)
                # action_obj[k] = list(mama)

    return action_obj


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
