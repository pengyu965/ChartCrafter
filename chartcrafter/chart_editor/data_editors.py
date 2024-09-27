import random
from typing import Tuple, List

import numpy as np

from chartcrafter.data_processor import Data, VisualAttribute


def apply_range_filter(data: Data) -> Tuple[Data, List[str]]:
    # Get the x-axis labels
    chart_data = data.data_table.copy(deep=True)
    xlabels = chart_data.iloc[:, 0].tolist()

    # Get the start and end x-axis values
    start_x = random.choice(xlabels[:len(xlabels) // 2])
    end_x = random.choice(xlabels[xlabels.index(start_x) + 1:])

    # Filter the data by the desired range
    start_index = chart_data.iloc[:, 0].tolist().index(start_x)
    end_index = chart_data.iloc[:, 0].tolist().index(end_x)
    edited_chart_data = chart_data.iloc[start_index:end_index + 1, :]

    # Generate the prompt
    if start_x is not None and end_x is not None:
        prompt = f"Show only data from '{start_x}' to '{end_x}'"
    else:
        raise ValueError("Error: 'xlabel_start' or 'xlabel_end' not provided.")

    return Data(edited_chart_data, data.chart_title, data.x_axis_title, data.y_axis_title), [prompt]


def apply_series_filter(data: Data, visual_attrs: VisualAttribute) -> Tuple[Data, VisualAttribute, List[str]]:
    # Get the data series indices
    data_ = data.copy()
    visual_attrs_ = visual_attrs.copy()

    chart_data = data_.data_table
    num_data_series = len(chart_data.columns) - 1
    if num_data_series < 2:
        raise ValueError("Cannot filter if there is only one data series")

    data_series_indices = range(0, num_data_series)

    # Get the desired number of data series
    filtered_num_series = random.choice(range(1, num_data_series))

    # Get the desired data series
    filtered_series_indices = random.sample(data_series_indices, filtered_num_series)
    for key in visual_attrs_.specific_attrs:
        visual_attrs_.specific_attrs[key] = [visual_attrs_.specific_attrs[key][i] for i in filtered_series_indices]

    # Filter the data by the desired data series
    # i+1 because the first column is the x-axis
    columns_to_keep = [chart_data.columns[0]] + [chart_data.columns[i + 1] for i in filtered_series_indices]
    edited_chart_data = chart_data.loc[:, chart_data.columns.isin(columns_to_keep)][columns_to_keep]

    data_.data_table = edited_chart_data
    # Generate the prompt
    data_series_names = edited_chart_data.columns[1:].astype("str").tolist()  # skip the x-axis column
    filtered_data_series_names = ', '.join(data_series_names)
    prompt = f"Show only data for '{filtered_data_series_names}'"

    return (
        data_,
        visual_attrs_,
        [prompt]
    )


def add_data_point(data: Data, visual_attrs: VisualAttribute, data_point_name: str | None = None,
                   data_point_values: str | None = None,
                   mutate=False) -> Tuple[Data, List[str]]:
    if (data_point_name is None or data_point_values is None) and not mutate:
        raise ValueError('Must specify either data_point_name and data_point_values or mutate should be True')
    else:
        data_ = data.copy()
        if mutate:
            data_removed, _, data_point_name, data_point_values = remove_data_point(data, visual_attrs)
            data.data_table = data_removed.data_table
        else:
            raise NotImplementedError("Add data series currently works only with mutate=False")

    prompt = f"Add data point '{data_point_name}' with values '{data_point_values}'"

    return data_, [prompt]


def remove_data_point(data: Data, visual_attrs: VisualAttribute, data_point_index: int | None = None) -> Tuple[
    Data, List[str], str, str]:
    data_ = data.copy()
    chart_data = data_.data_table
    # Make a copy of the chart data
    edited_chart_data = chart_data
    if chart_data.shape[0] < 2:
        raise ValueError("Can not remove data points if data points less than 2.")
    if data_point_index is None:
        data_point_index = -1
    # Get the name of the last data point (x-label)
    data_point_name = chart_data.iloc[data_point_index, 0]
    # Get the values of the last data point
    data_values = chart_data.iloc[data_point_index, 1:].values.tolist()

    # Remove the selected data point from the chart data
    edited_chart_data = edited_chart_data.drop(index=len(edited_chart_data) - 1)
    data_.data_table = edited_chart_data
    # Generate the prompt
    prompt = f"Remove data point '{data_point_name}'"

    return (data_,
            [prompt], str(data_point_name), str(data_values))


def add_data_series(data: Data, visual_attrs: VisualAttribute, series_name: str | None = None,
                    series_values: str | None = None, mutate=False):
    if (series_name is None or series_values is None) and not mutate:
        raise ValueError('Must specify either series_name and series_values or mutate should be True')
    else:
        data_ = data.copy()
        visual_attrs_ = visual_attrs.copy()
        if mutate:
            data_removed, visual_attrs_removed, _, series_name, series_values = remove_data_series(data, visual_attrs)
            data.data_table = data_removed.data_table
            visual_attrs.specific_attrs = visual_attrs_removed.specific_attrs
        else:
            raise NotImplementedError("Add data series currently works only with mutate=False")

    prompt = f"Add data series '{series_name}' to the chart with values '{series_values}'"

    return data_, visual_attrs_, [prompt]


def remove_data_series(data: Data, visual_attrs: VisualAttribute, data_series_index: int | None = None) -> Tuple[
    Data, VisualAttribute, List[str], str, str]:
    # remove the last data-series
    data_ = data.copy()
    visual_attrs_ = visual_attrs.copy()
    chart_data = data_.data_table

    chart_props = visual_attrs_.specific_attrs
    # Make a copy of the chart data
    edited_chart_data = chart_data

    # Get the number of existing data series
    num_data_series = len(chart_data.columns) - 1
    if num_data_series < 2:
        raise ValueError("cannot remove if there is only one data series")

    # Select the last data series to remove
    if data_series_index is None:
        data_series_index = num_data_series - 1
    data_series_name = edited_chart_data.columns[data_series_index + 1]
    data_series_values = edited_chart_data.iloc[:, data_series_index + 1].values.tolist()

    # Remove the selected data series from the chart data
    edited_chart_data = edited_chart_data.drop(data_series_name, axis=1)
    data_.data_table = edited_chart_data
    for key in chart_props:
        # remove data_series_index from the list
        # remove element from list using index
        chart_props[key].pop(data_series_index)

    # Generate the prompt
    prompt = f"Remove '{data_series_name}'"

    return (data_,
            visual_attrs_,
            [prompt],
            str(data_series_name),
            str(data_series_values))


def update_data_point(chart_data, chart_props):
    # Make a copy of the chart data
    edited_chart_data = chart_data

    # Get the number of existing data points
    num_data_points = chart_data.shape[0]

    # Select a random data point to update
    data_point_index = random.randint(0, num_data_points - 1)

    # Get the x-axis value of the selected data point
    x_value = chart_data.iloc[data_point_index, 0]

    # Generate random data for the updated data point
    min_value = np.min(chart_data.iloc[:, 1:].values)
    max_value = np.max(chart_data.iloc[:, 1:].values)
    if isinstance(min_value, int) and isinstance(max_value, int):
        updated_data_point = random.randint(min_value, max_value)
    else:
        updated_data_point = round(np.random.uniform(min_value, max_value), 2)

    # Get the index of the data series to update
    data_series_idx = random.randint(1, chart_data.shape[1] - 1)
    data_series_name = chart_data.columns[data_series_idx]

    # Update the selected data point in the chart data
    edited_chart_data.iloc[data_point_index, data_series_idx] = updated_data_point

    # Generate the prompt
    if data_series_name is None or data_series_name.strip() == "":
        prompt = f"Update the data point at '{x_value}' to '{updated_data_point}'"
    else:
        prompt = f"Update the data point for '{data_series_name}' at '{x_value}' to '{updated_data_point}'"

    return edited_chart_data, chart_props, prompt, 'update_data_point'
