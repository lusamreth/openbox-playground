from copy import deepcopy
from dict2xml import dict2xml
import xml.etree.ElementTree as ET
import dicttoxml
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


# b = flatten(a, ["configs", "keybinds"])
