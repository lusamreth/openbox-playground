from .app_mut import group_process, id_conversion
from .translator import TranslateSchema
from .mouse_mut import context_attrib_replacement, walker
from .keyboard_mut import cfg_currying, convertKeybind


Resolver = {
    "keyboard": {
        "Mutations": [cfg_currying],
        "hook": [convertKeybind],
        # "Mutations": [],
        # "hook": [],
    },
    "mouse": {
        "Mutations": [context_attrib_replacement],
        "hook": [walker],
    },
    "applications": {
        "Mutations": [group_process],
    },
    "theme": {},
    "desktops": {},
}


def BuildResolver(schemas: dict, resolvers: dict, data: dict):
    args = ("Mutations", "hook")
    res = {}
    for name, resolver in resolvers.items():
        if data.get(name) is None or data[name] == {}:
            continue

        print(resolver)
        mut = resolver.get(args[0]) or []
        hk = resolver.get(args[1]) or []
        xml_format = (
            TranslateSchema(schema=schemas[name], data=data[name])
            .inject_mutations(mut)
            .hook(hk)
            .call(name)
        )

        res[name] = xml_format
    print("RE", res)
    return res


def DefaultMouseMutation(MouseSchema, config):
    return (
        TranslateSchema(MouseSchema, config)
        .inject_mutations([context_attrib_replacement])
        .hook([walker])
        .call("Mouse")
    )
