import xml.etree.ElementTree as ET
import json

# from domain.schema import AppSetting
# from domain.schema import *

import domain
import mutations
from mutations.translator import TranslateSchema

Appo = {"id": {"classname": "bruh"}, "layer": "1", "style": {}}

group_app = {"application": [Appo]}

p = domain.AppSetting(**Appo)

pi = mutations.id_conversion(p.dict())
res = (
    TranslateSchema(domain.Applications, group_app)
    .inject_mutations([mutations.group_process])
    .call("applications")
)

print(ET.tostring(res))
font1 = {"name": "nani", "size": 10, "slant": "bruh"}
test_theme = {
    "name": "hell",
    "fonts": [font1],
}

# print("CREATING THEMNE")
# res_theme = TranslateSchema(domain.Theme, test_theme).call("theme")

Gen32 = {
    "resistance": {"strength": 10, "screen_edge_strength": 10},
    "focus": None,
}


# fix the none problem
def replacer(_dict, target, val):
    for k, v in _dict.items():
        if isinstance(v, dict):
            replacer(v, target, val)
        else:
            if k == target:
                _dict[k] = val

    return _dict


re = replacer(
    {"a": {"b": {"c": None}}, "bruh": {"bru": 1}},
    target="c",
    val="ok",
)

with open("first_test.json") as f:
    p = json.load(f)

    root = TranslateSchema(
        domain.RootSetting, p["RootSetting"]
    ).call("openbox")

    archetypes = {
        "keyboard": domain.Keyboard,
        "mouse": domain.Mouse,
        "theme": domain.Theme,
        "applications": domain.Applications,
        "desktops": domain.Desktops,
    }

    res = mutations.BuildResolver(archetypes, mutations.Resolver, p)
    for r in res.values():
        root.insert(0, r)

    print(ET.tostring(root))
