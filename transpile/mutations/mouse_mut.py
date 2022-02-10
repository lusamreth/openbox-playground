from copy import deepcopy
import xml.etree.ElementTree as ET
from . import translator

import sys

import xmltodict

sys.path.append("../utils")
from utils.mutation_tools import flatten, flatten_misc


def context_attrib_replacement(data):
    data_ctx = data["contexts"]

    def replace(dt, old, new):
        dt[new] = dt.pop(old)

    replace(data, "contexts", "context")
    for ctx in data_ctx:
        mbu = ctx["mousebinds"]
        replace(ctx, "name", "@name")
        replace(ctx, "mousebinds", "mousebind")

        for m in mbu:
            replace(m, "event", "@action")
            replace(m, "button", "@button")

    return data


def mousebind_injector(context_data):

    res = []
    ctx_name = context_data["@name"]

    for action_obj in context_data["mousebind"]:
        event = action_obj["@action"]
        for action in action_obj["actions"]:
            # create_action({"name","action"},action)
            # name = action.get("@name")

            # xml_output = ET.Element("action", {"name": name})
            flat = flatten_misc(action)
            # prone = xmltodict.unparse(flat)
            action_branch = xmltodict.unparse({"action": flat})
            assert action_branch is not None
            xml_output = ET.fromstring(action_branch)
            # xml_output.insert(0, ET.fromstring(action_branch))
            print("FLAT", ET.tostring(xml_output))

            loca = (
                "context[@name='{}']/mousebind[@action='{}']".format(
                    ctx_name, event
                )
            )

            res.append({"location": loca, "data": xml_output})

            print("Pine", xml_output)
        action_obj.pop("actions")

    return res


def walker(data):
    res = []
    for dt in data["context"]:
        # mutator(deepcopy(dt))
        res.append(mousebind_injector(dt))

    return res[0]


def DefaultMouseMutation(MouseSchema, config):
    return (
        translator.TranslateSchema(MouseSchema, config)
        .inject_mutations([context_attrib_replacement])
        .hook([walker])
        .call("Mouse")
    )
