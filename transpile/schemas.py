from dataclasses import dataclass
import utils
from typing import Generic, TypeVar, Optional
import xml.etree.ElementTree as ET
import translator
import var
from pydantic.generics import GenericModel
from pydantic import (
    BaseModel,
    validator,
    validate_arguments,
    root_validator,
)


def value_list_validation(field, val, valid_values):
    spot_invalid = set(val).difference(valid_values)
    if len(spot_invalid) > 0:
        raise ValueError(
            "Invalid {} items at {}".format(field, spot_invalid)
        )


@validate_arguments
def check_field_is_valid_obs_value(
    field_name: list[str],
) -> classmethod:
    def _field_checker(_, values) -> str:
        prone = set(values.keys()).intersection(field_name)
        selected = {k: values[k] for k in prone}

        for field, val in selected.items():
            target = field
            mapto = field.split(":", 1)
            if len(mapto) > 1:
                target = field[1]

            valid_values = var.Validation.get(target.strip())
            if valid_values:
                if isinstance(val, list):
                    value_list_validation(field, val, valid_values)
                else:
                    check_allow_value(val, valid_values)
            else:
                raise Exception(
                    "Invalid field of validation!: <{}> ".format(
                        field
                    )
                )

        return values

    # val.__name__ = (
    #     check_field_is_valid_email.__name__ + "_" + field_name
    # )
    return root_validator(allow_reuse=True)(_field_checker)


@dataclass
class Desktops:
    number: int
    names: list[str]
    firstdesk: int
    popUpTime: int


# +dragThreshold How many pixels you need to drag for it to be
# recognized as a drag operation.

# +doubleClickTime Time (in milliseconds) allowed between two separate clicks
# to register as a DoubleClick.

# +screenEdgeWarpTime Time (in milliseconds) to pause between two consecutive
# desktop switches done by holding the cursor next to the screen edge.
# Set to 0 to disable this feature.


class MouseConfigs(BaseModel):
    dragThreshold: str
    doubleClickTime: str
    screenEdgeWarpTime: str


def check_allow_value(val, allow):
    s = val.strip()
    if s not in allow:
        print(
            "{name} {} is not in valid {name} list {}".format(
                val, repr(allow), name="bruh"
            )
        )
        raise ValueError


class Mousebind(BaseModel):
    button: str
    event: str
    actions: list[str]

    _validate_valid_values = check_field_is_valid_obs_value(
        ["event", "actions"]
    )


class Context(BaseModel):
    name: str
    mousebinds: list[Mousebind]

    _validate_valid_values = check_field_is_valid_obs_value(
        ["name:context"]
    )


class Mouse(BaseModel):
    contexts: list[Context]
    configs: Optional[MouseConfigs]


T = TypeVar("T")


class Keybind(GenericModel, Generic[T]):
    action: str
    key: str
    chain: Optional[T]
    chroot: bool


class Keyboard(BaseModel):
    keybinds: list[Keybind]
    configs: Optional[dict]
    chainQuitKey: str


Form = {"mouse": Mouse, "desktop": Desktops, "keyboard": Keyboard}


# button: str
# triggerAction: str
# actions: list[str]

mouscfg = {
    "contexts": [
        {
            "name": "Frame",
            "mousebinds": [
                {
                    "button": "Press",
                    "event": "Press",
                    "actions": ["Debug", "AddDesktop"],
                },
                {
                    "button": "Li",
                    "event": "DoubleClick",
                    "actions": ["NextWindow", "AddDesktop"],
                },
            ],
        },
        {
            "name": "Frame",
            "mousebinds": [
                {
                    "button": "Press",
                    "event": "Press",
                    "actions": ["NextWindow", "AddDesktop"],
                },
                {
                    "button": "Li",
                    "event": "DoubleClick",
                    "actions": ["NextWindow", "AddDesktop"],
                },
            ],
        },
    ],
}


import dicto


def a(dc):
    return dicto.flatten(dc, ["configs"])


res = (
    translator.CreateSchema(
        Keyboard,
        dicto.kbconf["Keyboard"],
    )
    .inject_mutations([a])
    .hook([dicto.convertKeybind])
    .call("keyboard")
)

print(ET.tostring(res))
