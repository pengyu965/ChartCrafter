import os
from typing import List


def get_file_path(directory: str, name: str, extension: str) -> str:
    return os.path.join(directory, f"{name}.{extension}")


def create_dirs(*paths):
    for path in paths:
        os.makedirs(path, exist_ok=True)


def update_edits_dict(edits_required: dict, keys: list):
    dict_ = edits_required
    outer_keys = keys[:-1]
    for key in keys[:-1]:
        dict_ = dict_[key]
    innermost_key = keys[-1]
    dict_[innermost_key] -= 1
    if dict_[innermost_key] == 0:
        dict_.pop(innermost_key)
        remove_dict_items_recursively(edits_required, outer_keys)


def remove_dict_items_recursively(d: dict, keys: list):
    outer_keys = keys[:-1]
    dict_ = d
    for key in outer_keys:
        dict_ = dict_[key]
    if not keys:
        return
    if not dict_[innermost_key := keys[-1]]:
        dict_.pop(innermost_key)
        remove_dict_items_recursively(d, outer_keys)


def limit_edits(edits_required: dict,
                included_chart_types: List[str] | None = None,
                included_edits: List[str] | None = None) -> None:
    if included_chart_types is not None:
        for key in list(edits_required.keys()):
            if key not in included_chart_types:
                edits_required.pop(key, None)
    if included_edits:
        for chart_type, edits in edits_required.items():
            for key in list(edits.keys()):
                if key not in included_edits:
                    edits.pop(key, None)


def get_counts_from_edits_json(edits_required: dict) -> dict:
    return {
        outer_key: {
            inner_key: sum_nested_dict(inner_value)
            for inner_key, inner_value in outer_value.items()
        }
        for outer_key, outer_value in edits_required.items()
    }


def sum_nested_dict(nested_dict: dict) -> int:
    to_return = {}
    for key, value in nested_dict.items():
        if isinstance(value, dict):
            to_return[key] = sum_nested_dict(value)
        else:
            to_return[key] = value
    return sum(to_return.values())
