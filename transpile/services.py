from utils import combine_kv


class CreateStyleProcessorService():

    def grab(self, k):
        val = self.style.get(k)
        return val

    def __init__(self, style, writer):
        self.style = style
        self.winsize = self.grab("size")
        self.general = style
        self.writer = writer

    def size_handler(self):
        if self.winsize:
            sizearr = str.split(self.style["size"], "x")
            sizekeys = ["width", "height"]
            # bingus
            kp = combine_kv(sizekeys, sizearr)
            self.writer.call("size", elements=kp)

    def call(self):
        if self.style is None:
            return

        checkIfyes = lambda val: "yes" if val else "no"
        values = list(map(lambda key: checkIfyes(key), self.general))
        keys = self.general.keys()

        self.size_handler()
        self.writer.call(None, elements=combine_kv(list(keys), values))


class CreateIdParserService(object):

    def __init__(self, keys, reciever, id):
        self.id_keys = keys
        self.reciever = reciever
        self.id = id

    def call(self):
        id_keys = self.id_keys
        for idkey in id_keys:
            val = self.id.get(idkey)
            if val is not None:
                self.reciever.set(idkey, val)


class CreatePositionService(object):

    def __init__(self, position, write):
        self.position = position
        self.writer = write

    def call(self):
        p = self.position
        if p is None:
            return

        str_pos = map(lambda key: str(key), [p["y"], p["y"]])
        e = self.writer.call("position", combine_kv(["x", "y"], list(str_pos)))
        force = p.get("force")

        if force:
            e.set("force", str(force))
