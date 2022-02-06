import xml.etree.ElementTree as ET
# defining clear structure
from dataclasses import dataclass, asdict
from utils import *
from typing import Optional
from services import *
from enum import Enum, auto


class Maximise(Enum):
    VERTICAL = auto(),
    HORIZONTAL = auto(),
    BOTH = auto(),
    NONE = auto()


class Layer(Enum):
    NORMAL = auto(),
    ABOVE = auto(),
    BELOW = auto(),


@dataclass
class Style:
    decore: bool
    shade: bool
    focus: bool
    size: list


@dataclass
class Position:
    force: bool
    x: int
    y: int


@dataclass
class Skippable:
    pager: bool
    taskbar: bool


@dataclass
class Identifier:
    classname: Optional[str]
    #could use either class or name
    type: str
    name: Optional[str]


@dataclass
class AppSetting:
    id: Identifier
    layer: Layer
    desktop: int
    style: Style
    position: Optional[Position]
    skip: Optional[Skippable]


# must contain cfgkeys(keys recieve from the jsonparser)
# service_cfg map of cfgkeys to its corresponding service
def load_service(cfgkeys, service_cfg) -> None:
    print(cfgkeys)
    #bruh service
    for key in list(cfgkeys):
        # check if has subservice
        service = service_cfg.get(key)
        if service is not None:
            print(service.call)
            service.call()
        else:
            continue

    return


# using dependency injection significantly reduce class methods
# and bloat !!!


class AppConfigParser():

    def __init__(self, output):
        o = CreateXmlAccessService(root="applications",
                                   outputTarget=output).call()

        self.configElement = o["rootElement"]
        self.targetFd = o["targetFd"]
        self.appxmlroot = None

    def create_service_cf(self, config):
        xmlsetter = CreateElementFactory(self.appxmlroot)
        svcfg = {
            "style":
                CreateStyleProcessorService(config.get("style"), xmlsetter),
            "id":
                CreateIdParserService({"name", "type", "group"},
                                      self.appxmlroot, config["id"]),
            "position":
                CreatePositionService(config.get("position"), xmlsetter)
        }
        return svcfg

    def parse(self, conf: AppSetting):
        config = asdict(conf)
        root = self.configElement
        app = ET.SubElement(root, "application")
        self.appxmlroot = app
        load_service(config.keys(), self.create_service_cf(config))

    def writeToFile(self):
        CreateDataService(self.targetFd, self.configElement).call()


appxmlparser = AppConfigParser("application")


class ConfigExtractor():

    def __init__(self, configs: dict, lookup_keys: list, parser):
        self.appconfigs = configs
        self.lookup_keys = lookup_keys
        self.parser = parser

    def extract_id(self, classname, appconfig):

        id = appconfig.get("id")
        t = id.get("type") or "Normal"

        name = id.get("name")
        if name is not None:
            idt = Identifier(classname, t, name)
        else:
            idt = Identifier(classname, t, None)
        return idt

    def call(self):
        for classname in self.appconfigs:
            config = self.appconfigs[classname]

            args = []
            args.append(self.extract_id(classname, config))
            print(args)

            # def arg_parser(key):
            #     map = {"position": Position}
            #     if key
            def parse_pos(posconfig):
                p = posconfig
                return Position(config["force"], p[0], p[1])

            argmapper = {"position": parse_pos}
            mapkeys = argmapper.keys()

            def arg_parser(k):
                l = list(filter(lambda mapkey: mapkey == k, list(mapkeys)))
                if len(l) > 0:
                    firstl = l[0]
                    return argmapper[firstl](config[k])
                else:
                    return config[k]

            #arg_parser(key)

            args.extend(map(arg_parser, self.lookup_keys))
            settings = AppSetting(*args, None)
            self.parser.parse(settings)


appconf = readJsonConfig("../../test.json")

ConfigExtractor(appconf["applications"],
                ["layer", "desktop", "style", "position"], appxmlparser).call()
# extract_json_config()
appxmlparser.writeToFile()
