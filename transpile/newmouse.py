import utils
from dataclasses import dataclass


@dataclass
class Mousebind:
    button: str
    triggerAction: str
    actions: list[str]


@dataclass
class Contexts:
    name: str
    contexts: list[Mousebind]


# +dragThreshold How many pixels you need to drag for it to be
# recognized as a drag operation.

# +doubleClickTime Time (in milliseconds) allowed between two separate clicks
# to register as a DoubleClick.

# +screenEdgeWarpTime Time (in milliseconds) to pause between two consecutive
# desktop switches done by holding the cursor next to the screen edge.
# Set to 0 to disable this feature.


@dataclass
class MouseConfigs:
    dragThreshold: str
    doubleClickTime: str
    screenEdgeWarpTime: str


@dataclass
class Mouse:
    contexts: Contexts
    configs: MouseConfigs


class CreateMouseBind:
    def __init__(self, output) -> None:
        make = utils.CreateXmlAccessService(outputTarget=output, root="mouse")
        o = make.call()
        self.configElement = o["rootElement"]
        self.targetFd = o["targetFd"]
        self.mouseroot = o["rootElement"]
