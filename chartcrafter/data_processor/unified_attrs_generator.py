import random
from copy import deepcopy

from chartcrafter.chart_plotter.constants import ChartType
from chartcrafter.chart_plotter.constants import (FONTS, TITLE_FONT_SIZE, TICK_FONT_SIZE,
                                                                         GRID_LINE_STYLE,
                                                                         LINE_STYLES, MARKER_OPTIONS, COLOR_OPTIONS,
                                                                         HATCH_OPTIONS, LEGEND_POSITIONS,
                                                                         LEGEND_N_COLUMNS)
from chartcrafter.data_processor.unified_data import Data, VisualAttribute
from chartcrafter.data_processor.data_utils import slice_or_repeat_list, get_specific_attrs_key


def generate_random_unified_attrs(data: Data, chart_type: str):
    chart_type = chart_type.lower()
    if chart_type == ChartType.LINE.value:
        chart_specific_attrs = generate_line_chart_attrs(len(data.legend_labels))
    elif chart_type in (
            ChartType.STACKED_VERTICAL_BAR.value, ChartType.GROUPED_VERTICAL_BAR.value,
            ChartType.STACKED_HORIZONTAL_BAR.value,
            ChartType.GROUPED_HORIZONTAL_BAR.value):
        if chart_type in (ChartType.STACKED_VERTICAL_BAR.value, ChartType.STACKED_HORIZONTAL_BAR.value):
            legend_count = data.data_table.shape[1] - 1
        else:
            legend_count = len(data.legend_labels)
        chart_specific_attrs = generate_bar_chart_attrs(legend_count)
    else:
        raise NotImplementedError('Unknown chart type {}'.format(chart_type))

    global_attrs = generate_global_attrs(chart_type)
    specific_attrs_key = get_specific_attrs_key(chart_type)

    return VisualAttribute(global_attrs, chart_specific_attrs, specific_attrs_key)


def generate_global_attrs(chart_type):
    global_props = {
        "chart_type": chart_type,
        "chart_title_params": {
            "fontname": random.choice(FONTS),
            "fontsize": random.choice(TITLE_FONT_SIZE),
            "rotation": 0
        },
        "x_label_params": {
            'fontname': random.choice(FONTS),
            'fontsize': random.choice(TITLE_FONT_SIZE),
        },
        "x_tick_params": {
            'axis': 'x',
            'which': 'major',
            'rotation': random.choice([0, 45]),
            'labelsize': random.choice(TICK_FONT_SIZE),
            'labelfontfamily': 'sans-serif'
        },
        "legend_params": {
            'loc': random.choice(LEGEND_POSITIONS),
            'ncol': random.choice(LEGEND_N_COLUMNS)}
    }

    grid_params = {'visible': random.choice([True, False])}
    if grid_params["visible"]:
        grid_params.update(axis=random.choice(['both', 'x', 'y']), linestyle=random.choice(GRID_LINE_STYLE))

    global_props["grid_params"] = grid_params

    global_props["y_label_params"] = deepcopy(global_props["x_label_params"])
    global_props["y_tick_params"] = deepcopy(global_props["x_tick_params"])
    global_props["y_tick_params"]["axis"] = "y"
    global_props["y_tick_params"]["rotation"] = random.choice([0])

    return global_props


def generate_line_chart_attrs(legend_count, colors=None):
    linestyles = deepcopy(LINE_STYLES)
    markers = deepcopy(MARKER_OPTIONS)

    random.shuffle(linestyles)
    random.shuffle(markers)

    colors_passed = bool(colors)
    if not colors_passed:
        colors = deepcopy(COLOR_OPTIONS)
        random.shuffle(colors)

    if legend_count:
        linestyles = slice_or_repeat_list(linestyles, legend_count)
        markers = slice_or_repeat_list(markers, legend_count)
        if not colors_passed:
            colors = slice_or_repeat_list(colors, legend_count)

    return {
        "linestyles": linestyles,
        "markers": markers,
        "colors": colors
    }


def generate_bar_chart_attrs(legend_count, colors=None):
    hatches = deepcopy(HATCH_OPTIONS)
    random.shuffle(hatches)
    colors_passed = bool(colors)
    if not colors_passed:
        colors = deepcopy(COLOR_OPTIONS)
        random.shuffle(colors)

    if legend_count:
        hatches = slice_or_repeat_list(hatches, legend_count)
        if not colors_passed:
            colors = slice_or_repeat_list(colors, legend_count)

    return {
        "hatches": hatches,
        "colors": colors
    }


def populate_values_missing_attrs_unified_json_dict(unified_attrs_dict, legend_count):
    chart_type = unified_attrs_dict["global_properties"].get("chart_type")

    default_properties = get_default_properties(legend_count, chart_type)

    sanitized_params = replace_dict_recursively(default_properties, unified_attrs_dict)

    return sanitized_params


def replace_dict_recursively(src: dict, target: dict) -> dict:
    res = {}
    for key, value in src.items():
        target_val = target.get(key)
        if not target_val:
            target_val = value
        elif isinstance(target_val, dict):
            target_val = replace_dict_recursively(value, target_val)
        elif isinstance(target_val, list):
            target_val = target_val[:len(value)]

        res[key] = target_val
    return res


def get_default_properties(legend_counts, chart_type=ChartType.LINE.value) -> dict:
    default_properties = {
        "chart_title": "# Missing Chart Title",
        "x_axis_title": "# Missing x axis title",
        "y_axis_title": "# Missing y axis title",
        "global_properties": {
            "chart_type": "bar",
            "x_label_params": {
                "fontname": "Arial Black",
                "fontsize": "medium"
            },
            "y_label_params": {
                "fontname": "Arial Black",
                "fontsize": "medium"
            },
            "legend_params": {
                "loc": 1,
                "ncol": 3
            },
            "chart_title_params": {
                "fontname": "Arial Black",
                "fontsize": "large",
                "rotation": 0
            },
            "x_tick_params": {
                "axis": "x",
                "which": "major",
                "rotation": 45,
                "labelsize": "small",
                "labelfontfamily": "Arial Black"
            },
            "y_tick_params": {
                "axis": "y",
                "which": "major",
                "rotation": 0,
                "labelsize": "small",
                "labelfontfamily": "Arial Black"
            },
            "grid_params": {
                "visible": False
            }
        }}

    colors = repeat_to_length(COLOR_OPTIONS, legend_counts)
    if chart_type == "line":
        markers = repeat_to_length(MARKER_OPTIONS, legend_counts)
        line_styles = repeat_to_length(LINE_STYLES, legend_counts)
        default_properties.update(
            **{f"{chart_type}_properties": {"linestyles": line_styles,
                                            "markers": markers,
                                            "colors": colors
                                            }}
        )
    else:
        hatches = repeat_to_length(HATCH_OPTIONS, legend_counts)
        default_properties.update(
            **{f"{chart_type}_properties": {"hatches": hatches,
                                            "colors": colors}}
        )

    return default_properties


def repeat_to_length(lst: list, length: int) -> list:
    if length <= 0:
        return []
    repeated_list = [lst[i % len(lst)] for i in range(length)]
    return repeated_list
