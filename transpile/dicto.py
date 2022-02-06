from copy import deepcopy
import dicttoxml
from dict2xml import dict2xml
import xml.etree.ElementTree as ET
import translator
import xmltodict

nested = {
    "bruh1": "11",
    # "bruh2": {"sada": 1},
    "DOTAC2": {"SDu": {"sda": "sda"}, "bru": {"SDA": "1"}},
    "hell": {
        "id": "1",
        "okabil": "100",
        "okabil11": "100",
        "okabil2": "100",
        "pp01": {
            "lkee-2": {"pico": {"pp": "100"}},
            # "bruh": "100",
            "lkee-1": {"bruha": "100"},
            "lkee-3": {"bruh": "100"},
        },
        "ppp04": {"pbg": "010", "pbx": "012"},
        "ppp03": {"pbg": "010", "pbx": "012"},
        "ppp02": {"pbo": {"lkee": "100"}, "1pbo": {"lkee": "100"}},
        "pda": "100",
    },
    "DOTAC": {"SD": {"dsad": "bru"}, "Sad": "sad"},
    "pita2": {
        "pb": {"lkee": "100"},
        "DOTAC32": {"SDx": {"sda": "sda"}},
    },
    "DONDA": "100",
    # problem after entering root it neglect the upper element
    "pita": {
        "certic32": {"bruh1": {"sdas": "10"}},
        "aa": [{"bruh1": {"sdas": "10"}}, {"bruh": 10}],
    },
    "bruh": "11",
}


kbconf = {
    "Keyboard": {
        "configs": {"Threshold": "100"},
        "keybinds": [
            {
                "action": "bruh",  # name
                "key": "D",
                "chroot": False,
                "chain": {"action": "bruhchain", "key": "D"},
            },
            {
                "action": "bruh2",  # name
                "key": "D",
                "chroot": False,
                "chain": {"action": "bruhchane", "key": "D"},
            },
        ],
        "chainQuitKey": "haa",
    }
}


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


# def create_action(mapper, action_obj):
#     kbind = {}
#     for k, map in mapper.items():
#         itm = action_obj.get(map)
#         if k[0] != "?" and itm is None:
#             raise Exception("bruh")

#         if k[0] == "?":
#             k = k[1:]
#         if k == "chain" and itm is not None:
#             pois = create_action(mapper, itm)
#             kbind["keybind"] = pois
#             continue

#         # print("LPko", kbind)
#         kbind[k] = itm
#     # new_keybind.append({})
#     return kbind


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
            print("hayi diom")
            raise Exception("bruh")
        if pine:
            continue

        EP = ET.Element(k, {})
    return EP


def convertKeybind(input_dict):
    dictionary = input_dict
    # mapper = {"@key": "key", "action": "action", "?chain": "chain"}
    mapper = {
        "keybind": "key",
        "@action": "action",
        "?chain": "chain",
    }
    # return flatten(kbind, ["chain"])
    res = []
    for action_obj in dictionary["keybinds"]:
        res.append(create_action(mapper, action_obj))

    input_dict.pop("keybinds")
    print("CONVIEI", input_dict)
    return res


# b = flatten(a, ["configs", "keybinds"])
