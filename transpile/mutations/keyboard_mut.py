from copy import deepcopy
import xml.etree.ElementTree as ET


import sys

sys.path.append("../utils")
from utils.mutation_tools import flatten, replace

from .translator import TranslateSchema


def flatten(dictionary, skips):
    newobj = deepcopy(dictionary)
    assert isinstance(dictionary, dict)

    # if dictionary.get("convertible") is None:
    #     return dictionary

    for skip in skips:
        newobj.pop(skip)
        pi = dictionary.get(skip)
        if pi:
            newobj.update(pi)

    # newobj.pop("convertible")

    return newobj


def create_action(mapper, action_obj):
    EP = None

    # SkipVar = {"@": adder, "?": chain}
    def flatten_misc(action_obj):
        action_obj["action"] = flatten(
            action_obj["action"], ["misc"]
        )

    for _, map in mapper.items():
        p = action_obj.get(map)
        if map == "chain":
            act_name = action_obj.get("action")
            # print("chain", k, map, p, act_name, action_obj["@key"])
            loca = "keybind[@key='{}']/action[@name='{}']".format(
                action_obj["@key"], act_name["@name"]
            )

            kb = ET.Element("keybind", {"key": p["key"]})
            ET.SubElement(kb, "action", {"name": p["action"]})
            EP = {"location": loca, "data": kb}

            flatten_misc(action_obj)
            # action_obj = pi
            del action_obj[map]
    return EP


def convertKeybind(input_dict):
    dictionary = input_dict
    # mapper = {"@key": "key", "action": "action", "?chain": "chain"}
    mapper = {"@action": "action", "?chain": "chain", "@key": "@key"}
    # return flatten(kbind, ["chain"])
    res = []
    for action_obj in dictionary["keybind"]:

        r = create_action(mapper, action_obj)
        if r:
            print("RR", r)
            res.append(r)

    return res


def cfg_currying(dc):
    if dc.get("configs"):
        return flatten(dc, ["configs"])
    else:
        return dc
