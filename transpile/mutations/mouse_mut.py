import xml.etree.ElementTree as ET
from . import translator


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

    # print("Po", p)
    # return flatten(kbind, ["chain"])
    res = []
    for action_obj in context_data["mousebind"]:
        for action in action_obj["actions"]:
            xml_output = ET.Element("action", {"name": action})
            loca = "context/mousebind[@action='{}']".format(
                action_obj["@action"]
            )

            res.append({"location": loca, "data": xml_output})

            print("Pine", xml_output)
        action_obj.pop("actions")
    print("res", res)

    return res


def walker(data):
    res = []
    for dt in data["context"]:
        res.append(mousebind_injector(dt))

    return res[0]


def DefaultMouseMutation(MouseSchema, config):
    return (
        translator.TranslateSchema(MouseSchema, config)
        .inject_mutations([context_attrib_replacement])
        .hook([walker])
        .call("Mouse")
    )
