import json
from typing import Tuple

import pandas as pd

from chartcrafter.data_processor.data_utils import (get_specific_attrs_key,
                                                                           pre_process_chart_data,
                                                                           pre_process_unified_data
                                                                           )
from chartcrafter.data_processor.unified_attrs_generator import \
    populate_values_missing_attrs_unified_json_dict
from chartcrafter.data_processor.unified_data import Data, VisualAttribute
from chartcrafter.data_processor.validators import pmc_json_validator


@pmc_json_validator
def get_data_from_pmc_json(pmc_json: dict) -> Tuple[Data, str]:
    text_blocks = pd.DataFrame(pmc_json["task6"]["input"]["task2_output"]["text_blocks"])
    text_roles = pd.DataFrame(pmc_json["task6"]["input"]["task3_output"]["text_roles"])
    chart_type = pmc_json["task1"].get("output", {}).get("chart_type", "")

    labels = text_blocks.merge(text_roles, how="outer", on="id")

    axes_titles = labels[labels["role"] == "axis_title"]["text"].values

    x_axis_title = ""
    y_axis_title = ""

    if axes_titles.shape[0] == 2:
        x_axis_title, y_axis_title = axes_titles
    elif axes_titles.shape[0] == 1:
        x_axis_title = axes_titles[0]

    chart_title = labels[labels["role"] == "chart_title"]
    if chart_title.empty:
        chart_title = ""
    else:
        chart_title = labels[labels["role"] == "chart_title"]["text"].values[0]

    data_frame = (
        pd.concat(
            [
                pd.DataFrame(d["data"])
                .rename(columns={"y": d["name"]}).set_index("x")
                for d in pmc_json["task6"]["output"]["data series"]
            ],
            axis=1)
        .reset_index()
        .rename(columns={"x": axes_titles[0]})
    )
    data_frame = pre_process_chart_data(data_frame)

    return Data(data_frame, chart_title, x_axis_title, y_axis_title), chart_type


def read_unified_attrs(unified_attrs_dict,
                       unified_json_path="",
                       auto_fill_missing_attrs=True) -> Tuple[Data, VisualAttribute]:
    if not unified_attrs_dict:
        with open(unified_json_path, "r") as unified_json_file:
            unified_attrs_dict = json.load(unified_json_file)

    underlying_data = pre_process_unified_data(unified_attrs_dict.pop("underlying_data"))
    chart_title = unified_attrs_dict.pop("chart_title")
    x_label = unified_attrs_dict.pop("x_axis_title")
    y_label = unified_attrs_dict.pop("y_axis_title")

    data = Data(underlying_data, chart_title, x_label, y_label)

    specific_attrs_key = get_specific_attrs_key(unified_attrs_dict["global_properties"])

    if auto_fill_missing_attrs:
        # Proceed with populating random values for the missing attributes if autofill flag is True
        legend_count = len(data.legend_labels)
        unified_attrs_dict = populate_values_missing_attrs_unified_json_dict(unified_attrs_dict, legend_count)

    visual_attrs = VisualAttribute(unified_attrs_dict["global_properties"], unified_attrs_dict[specific_attrs_key],
                                   specific_attrs_key)

    return data, visual_attrs
