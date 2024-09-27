import json
import random
from io import StringIO

import pandas as pd

from chartcrafter.chart_plotter.constants import ChartType


def get_specific_attrs_key(chart_type: str) -> str:
    if chart_type.lower() == ChartType.LINE.value:
        prefix = "line"
    elif chart_type.lower() in (
            ChartType.GROUPED_VERTICAL_BAR.value, ChartType.STACKED_VERTICAL_BAR.value,
            ChartType.GROUPED_HORIZONTAL_BAR.value,
            ChartType.STACKED_HORIZONTAL_BAR.value):
        prefix = "bar"
    else:
        raise NotImplementedError('Unknown chart type {}'.format(chart_type))

    return f"{prefix}_properties"


def pre_process_chart_data(df: pd.DataFrame) -> pd.DataFrame:
    # Convert the column name and values to numeric if applicable
    columns = []
    for col in df:
        try:
            df[col] = pd.to_numeric(df[col], downcast="float")
        except ValueError:
            # The value can not be converted to numeric
            pass
        try:
            converted_col_name = float(col)
            if converted_col_name.is_integer():
                converted_col_name = int(converted_col_name)
        except ValueError:
            # The value can not be converted to numeric
            converted_col_name = col
            pass

        if pd.api.types.is_numeric_dtype(type(converted_col_name)):
            converted_col_name = round(converted_col_name, 2)
        columns.append(converted_col_name)

    df = df.round(2)

    try:
        # Sort values in the first column if the column values are numeric
        # if pd.api.types.is_numeric_dtype(df[columns[0]]):
        df.sort_values(df.columns[0], inplace=True)
        sorted_cols = sorted(columns[1:])
        columns = [columns[0]] + sorted_cols
    except TypeError:
        # Skip if error
        pass

    df.columns = columns

    return df.reset_index(drop=True)


def pre_process_unified_data(data_string: str) -> pd.DataFrame:
    df = pd.read_csv(StringIO(data_string.replace(" <0x0A> ", "\n")), sep=r"\s*|\s*")
    processed_df = pre_process_chart_data(df)

    return processed_df


def slice_or_repeat_list(input_list, len_needed):
    inp_list = input_list[:]
    final_list = []

    while len(final_list) < len_needed:
        final_list.extend(inp_list)
        random.shuffle(inp_list)

    return final_list[:len_needed]


def write_unified_json(file_path: str, data, visual_attrs):
    with open(file_path, "w") as output_file:
        json.dump(data.to_unified_data() | visual_attrs.to_unified_data(), output_file, indent=2)
