from .var import Validation
import sys

sys.path.append("../utils")
from utils.mutation_tools import replace, delete_none

from pydantic import (
    validate_arguments,
    root_validator,
)


def value_list_validation(field, val, valid_values):
    spot_invalid = set(val).difference(valid_values)
    if len(spot_invalid) > 0:
        raise ValueError(
            "Invalid {} items at {}".format(field, spot_invalid)
        )


def extract_overlap(primary_dict: dict, overlap_keys):
    prone = set(list(primary_dict.keys())).intersection(overlap_keys)
    print("PRONE", prone, primary_dict)
    return {k: primary_dict[k] for k in prone}


@validate_arguments
def check_field_is_valid_obs_value(
    field_name: list[str],
) -> classmethod:
    def _field_checker(_, values) -> str:
        selected = extract_overlap(values, field_name)

        for field, val in selected.items():
            target = field
            mapto = field.split(":", 1)
            if len(mapto) > 1:
                target = field[1]

            valid_values = Validation.get(target.strip())
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


def remove_empty() -> classmethod:
    def delete_all_none(_, values):
        delete_none(values)
        return values

    return root_validator(
        allow_reuse=True,
    )(delete_all_none)


import inspect


def convert_field_to_attr(fields: list[str]) -> classmethod:
    def _converter(_cls, values):
        selected = extract_overlap(values, fields)
        for select in selected:
            replace(values, select, "@" + select)

        return values

    return root_validator(
        allow_reuse=True,
    )(_converter)


def check_allow_value(val, allow):
    s = val.strip()
    if s not in allow:
        print(
            "{name} {} is not in valid {name} list {}".format(
                val, repr(allow), name="bruh"
            )
        )
        raise ValueError


Count = 0


def rename(f, Count):
    f.__name__ = "{}-{}".format(f.__name__, Count)
    Count += 1
    return f


def set_default_values(new_values: dict) -> classmethod:
    def _set_default(_, values):
        selected = extract_overlap(values, new_values.keys())
        for select in selected:
            if values[select] is None:
                values[select] = new_values[select]

        return values

    return root_validator(allow_reuse=True)(_set_default)


def replace_field_name(new_field_names: dict):
    def _replace_field(_, values):
        selected = extract_overlap(values, new_field_names.keys())
        for select in selected:
            replace(values, select, new_field_names[select])
        return values

    return root_validator(allow_reuse=True)(_replace_field)


def ctacha(new_vals: dict):
    def _replace_field32(_, values):
        selected = extract_overlap(values, new_vals.keys())
        print("SEL SEL", selected)
        # for select in selected:
        #     replace(values, select, new_values[select])
        # return values

    print(_replace_field32(0, new_vals))

    return root_validator()(_replace_field32)
