import sys

sys.path.append("../utils")
from utils.mutation_tools import flatten, delete_none, replace


def id_conversion(each_app):
    print(each_app)
    id = each_app["id"]
    delete_none(each_app)
    id_keys = id.keys()
    print(id_keys, id.keys())

    for key in list(id_keys):
        replace(id, key, "@" + key)

    return each_app


def style_extract(data):
    return flatten(data, ["style"])


def group_process(group):
    apps = group["application"]

    for app in apps:
        style_extract(app)
        # style_extract(id_conversion(app))
    return group
