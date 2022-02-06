from readxml import checkIfIter, traverseNestedAction

from transpile.utils import MutationService
import xml.etree.ElementTree as ET

tree = ET.parse("../custom-rc.xml")
root = tree.getroot()


prefix = "{http://openbox.org/3.4/rc}"
obe = lambda target: prefix + target


def pois(item):
    try:
        ix = iter(item)

        def leveling():
            qub = ix.__next__()
            while qub:
                o = iter(qub).__next__()
                qub = iter(o).__next__()

        lis = list()
        leveling()
        print("leveling", lis)
        return pois(iter(ix.__next__()))
    except:
        return


def test1():
    keyboard = root.find(obe("keyboard"))

    for kb in iter(keybinds):
        print("pois", pois(kb))
    keys = list(map(lambda e: e.attrib, keybinds))


class SplitElementServiceExp(MutationService):
    def __init__(self, payload) -> None:

        self.payload = payload
        self.upper = []
        self.lower = []
        self.loclist = []

    def handlelist(self, key, item):
        res = []
        # e = map(lambda x: ET.SubElement(m, x), item)
        for i in item:
            m = ET.Element(key, {})
            m.text = i
            res.append(m)

        self.lower.extend(list(res))

    def traverse(self, orikey, item, inherit_buffer=[]):

        if self.skip(orikey):
            return

        key = self.replace(orikey)
        if isinstance(item, dict):
            self.upper.append(
                {"value": ET.Element(key, {}), "ptr": 0}
            )
            self.CreateNewElementFact(item, self.loclist)
        elif isinstance(item, list):
            self.handlelist(key, item)
        else:
            c = ET.Element(key, {})
            c.text = item

            self.loclist.append(c)
            print(inherit_buffer)
            self.lower.append(c)
        # print(type(item))

    def CreateNewElementFact(self, payload, buffer=[]):
        for key, item in payload.items():
            self.traverse(key, item, buffer)

    def call(self, replacement, skip):
        super().__init__(replacement, skip)
        self.CreateNewElementFact(self.payload)
        return {"lower": self.lower, "upper": self.upper}


# res = SplitElementServiceExp(nested).call({}, {})
# print(res["upper"])
