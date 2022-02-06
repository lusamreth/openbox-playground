import xml.etree.ElementTree as ET
import json
from os.path import exists

from copy import deepcopy


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
            print("iasd", k, mapper)
            raise Exception("bruh")
        if pine:
            continue

        EP = ET.Element(k, {})
    return EP


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


def makeAction(action, inneraction, cmd):
    inner = ET.SubElement(action, inneraction)
    inner.text = cmd


def combine_kv(keys, values):
    def not_list(a):
        return type(a) is not list

    if not_list(keys) and not_list(values):
        keys = [keys]
        values = [values]

    # default behavoir: leftover keys will be ignored!
    if len(keys) < len(values):
        raise Exception("Not enough keys to combine with value")

    res = {}
    for i, val in enumerate(values):
        res[keys[i]] = val
        # res[val] = keys[i]
    return res


class CreateDataService(object):
    def __init__(self, fd, root):
        self.fd = fd
        self.root = root

    def call(self):
        self.fd.write(ET.tostring(self.root))
        self.fd.close()

    # need to create Omit mechanism


cached = []


class CreateElementFactory:
    def __init__(self, xmlroot):
        self.mainroot = xmlroot
        self.cached = cached

    def call(self, branch, elements):
        if self.mainroot is None:
            raise Exception("app is not yet instantiate!")
        if branch is None:
            element = self.mainroot
        else:
            element = ET.SubElement(self.mainroot, branch)
        print("INPUT ELEMENTs", elements)

        #         def call_stack(e):
        #             # innerElement.text = str(e[key])
        #             for k, v in e.items():
        #                 scrub = None
        #                 if isinstance(v, dict):
        #                     cached.append(ET.SubElement(element, k))
        #                     call_stack(v)
        #                 else:

        #                     def extract():
        #                         z = None
        #                         if len(cached) > 0:

        #                             scrub = cached.pop()
        #                             z = ET.SubElement(scrub, k)
        #                             z.text = v

        #                             extract()

        #                     extract()

        #         call_stack(elements)

        return element


def validate_field(Field, dataInput):
    res = {}
    for field in Field.__dataclass_fields__:
        res[field] = dataInput.get(field)

    return res


def readJsonConfig(file):
    mb = open(file, "r")
    print("MB rad", mb)
    return json.load(mb)


def test_combine_kv():
    expected = {"key1": "val1", "key2": "val2"}
    res = combine_kv(["key1", "key2"], ["val1", "val2"])
    assert res == expected, "Incorrect!!"


class MutationService:
    def __init__(self, replacement, skips) -> None:

        self.skips = skips or []
        # self.skips = ["button"]
        self.replacement = replacement

    def replace(self, k):
        if bool(not self.replacement):
            return k
        print("replla,", self.replacement)

        has = self.replacement.get(k)

        if has is not None:
            return has
        else:
            return k

    def skip(self, k):
        return self.skips.count(k) > 0


class SplitElementService(MutationService):
    def __init__(self, payload) -> None:

        self.payload = payload
        self.upper = []
        self.lower = []

    def handlelist(self, key, item):
        res = []
        # e = map(lambda x: ET.SubElement(m, x), item)
        for i in item:
            m = ET.Element(key, {})
            m.text = i
            res.append(m)

        self.lower.extend(list(res))

    def traverse(self, orikey, item):
        if orikey == "chain":
            print("TARGET!", orikey, item)
            self.lower.append(ET.Element("Bruh"))
            return

        if self.skip(orikey):
            return

        key = self.replace(orikey)

        if isinstance(item, dict):
            print("kee", key)
            self.upper.append(ET.Element(key, {}))
            self.CreateNewElementFact(item)
        elif isinstance(item, list):
            self.handlelist(key, item)
        else:
            c = ET.Element(key, {})
            c.text = item
            self.lower.append(c)
        # print(type(item))

    def CreateNewElementFact(self, payload):
        for key, item in payload.items():
            self.traverse(key, item)

    def call(self, replacement, skip):
        super().__init__(replacement, skip)
        self.CreateNewElementFact(self.payload)
        print(self.upper)
        return {"lower": self.lower, "upper": self.upper}


class ScissorService:
    def __init__(self) -> None:
        self.skip_element = {}
        self.replacement = {}

    def replace(self, input):
        self.replacement = input
        return self

    def skip(self, skip):
        self.skip_element = skip
        return self


class CreateNewElFact(ScissorService):
    def __init__(self, payload) -> None:
        # self.root = root
        self.splitter = SplitElementService(payload)
        self.halt = False
        self.prev = None
        self.res = None
        super().__init__()

    def handle_xml_chain(self, current, lower):
        if self.prev is not None:
            current.insert(0, self.prev)
            self.prev = current
            # print("UP", ET.tostring(self.prev))

        else:
            self.prev = current
            current.insert(0, lower.pop())

    def call(self):
        print("replacement", self.replacement, self.skip_element)
        res = self.splitter.call(self.replacement, self.skip_element)

        upper = res["upper"]
        lower = res["lower"]

        while not self.halt:
            # if len(upper) == 0:
            #     return lower.pop()

            up = upper.pop()
            if isinstance(up, dict):
                print("woah")
                # { ptr:int(index), val:<Element> }

            self.handle_xml_chain(up, lower)

            if len(lower) > 0:
                # self.prev.insert(0, lower.pop())
                for lower_element in lower:
                    self.prev.insert(0, lower_element)
                lower = []

            self.res = up

            if len(upper) == 0 and len(lower) == 0:
                self.halt = True

        return self.res


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


def test_create_element():
    print("running create element test!")
    make = CreateXmlAccessService(
        outputTarget="test-output", root="test-root"
    )

    test_payload = {
        "mousebind": {
            "button": "f",
            "triggerAction": "Press",
            "actions": ["1", "2"],
            "chain": {"actions": ["bruh"]}
            # "chain": ["bruh", "bruh", "bruh"],
        }
    }

    # test_payload = {"root": {"apple": "1", "spp": "23"}}  #
    # test_payload = {"root": "1"}  #
    # test_payload = {"root": {"lv2": ["3", "bru", "32"]}}
    # test_payload = {"bruh": {"bruh1": {"bruh2": {"bruh3": {"bruh4": "text"}}}}}
    # test_payload = {"contexts": {"bruh": {"bru": "text"}}}
    # only work after nested level
    res = (
        CreateNewElFact(test_payload)
        # .skip("button")
        .replace({"button": "ok"}).call()
    )
    print(ET.tostring(res))


if __name__ == "__main__":
    test_combine_kv()
    test_create_element()
    print("Everything passed")
