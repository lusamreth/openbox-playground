from copy import deepcopy
import xml.etree.ElementTree as ET

import sys

sys.path.append("../utils")
from utils.mutation_tools import flatten, flatten_misc

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


def create_action(mapper, action_obj, loca_finder):
    EP = None

    # SkipVar = {"@": adder, "?": chain}
    #     def flatten_misc(action_obj):

    #         action_obj["action"] = flatten(
    #             action_obj["action"], ["misc"]
    #         )
    #         print("MAGG", action_obj["action"])

    #         for k, item in action_obj["action"].items():
    #             if k != "@name":
    #                 if isinstance(item, list):

    #                     def convert_each_action(inner):
    #                         if isinstance(inner, dict):
    #                             print("MAGG INNER", inner)
    #                             n = "@name"
    #                             if inner.get("name") is not None:
    #                                 n = "name"

    #                             name = {"@name": inner.pop(n)}
    #                             inner = inner | name
    #                             cop = {"action": inner}

    #                             return cop

    #                         return {"action": {"@name": inner}}

    #                     mama = map(convert_each_action, list(item))
    #                     action_obj["action"][k] = list(mama)

    for map_item in mapper:
        p = action_obj.get(map_item)
        if map_item == "chain":
            # print("chain", k, map, p, act_name, action_obj["@key"])
            loca = loca_finder(action_obj)
            kb = ET.Element("keybind", {"key": p["key"]})
            ET.SubElement(kb, "action", {"name": p["action"]})
            EP = {"location": loca, "data": kb}
            action_obj["action"] = flatten_misc(action_obj["action"])
            # action_obj = pi
            del action_obj[map_item]
    return EP


def convertKeybind(input_dict):
    dictionary = input_dict
    # mapper = {"@key": "key", "action": "action", "?chain": "chain"}
    mapper = {"action", "chain", "@key"}
    # return flatten(kbind, ["chain"])
    res = []

    def lc_finder(action_obj):
        act_name = action_obj.get("action")
        return "keybind[@key='{}']".format(
            action_obj["@key"], act_name["@name"]
        )

    for action_obj in dictionary["keybind"]:

        r = create_action(mapper, action_obj, lc_finder)
        if r:
            print("RR", r)
            res.append(r)

    return res


def cfg_currying(dc):
    if dc.get("configs"):
        return flatten(dc, ["configs"])
    else:
        return dc
