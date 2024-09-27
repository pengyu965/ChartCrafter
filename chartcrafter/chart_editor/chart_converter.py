import random
from copy import deepcopy
from typing import Optional, Literal, Tuple, List

from chartcrafter.chart_editor import prompt_templates
from chartcrafter.chart_plotter.constants import ChartType
from chartcrafter.data_processor import Data, VisualAttribute
from chartcrafter.data_processor.data_utils import get_specific_attrs_key
from chartcrafter.data_processor.unified_attrs_generator import (generate_bar_chart_attrs,
                                                                                        generate_line_chart_attrs)


def convert_line_to_bar(data: Data, visual_attrs: VisualAttribute,
                        new_chart_type: Optional[
                            Literal[
                                "grouped vertical bar",
                                "stacked vertical bar", "grouped horizontal bar", "stacked horizontal bar",]] = None
                        ) -> Tuple[Data, VisualAttribute, List[str]]:
    if new_chart_type is None:
        new_chart_type = random.choice([ChartType.GROUPED_VERTICAL_BAR.value, ChartType.STACKED_VERTICAL_BAR.value,
                                        ChartType.GROUPED_HORIZONTAL_BAR.value, ChartType.STACKED_HORIZONTAL_BAR.value])
    else:
        new_chart_type = new_chart_type.lower()

    global_attrs, specific_attrs = deepcopy(visual_attrs.global_attrs), deepcopy(visual_attrs.specific_attrs)
    global_attrs["chart_type"] = new_chart_type
    specific_attrs_key = get_specific_attrs_key(new_chart_type)

    specific_attrs = generate_bar_chart_attrs(len(data.legend_labels), specific_attrs["colors"])

    return (Data(deepcopy(data.data_table),
                 data.chart_title,
                 data.y_axis_title,
                 data.y_axis_title),
            VisualAttribute(global_attrs, specific_attrs, specific_attrs_key),
            [prompt.format(old_chart_type="Line Chart", new_chart_type=new_chart_type) for prompt in
             prompt_templates.chart_conversion])


def convert_bar_to_line(data: Data, visual_attrs: VisualAttribute) -> Tuple[Data, VisualAttribute, List[str]]:
    old_chart_type = visual_attrs.global_attrs["chart_type"]
    new_chart_type = ChartType.LINE.value
    global_attrs, specific_attrs = deepcopy(visual_attrs.global_attrs), deepcopy(visual_attrs.specific_attrs)
    global_attrs["chart_type"] = new_chart_type

    specific_attrs_key = get_specific_attrs_key(new_chart_type)
    specific_attrs = generate_line_chart_attrs(len(data.legend_labels), specific_attrs["colors"])

    return (Data(deepcopy(data.data_table),
                 data.chart_title,
                 data.y_axis_title,
                 data.y_axis_title),
            VisualAttribute(global_attrs, specific_attrs, specific_attrs_key),
            [prompt.format(old_chart_type=old_chart_type, new_chart_type=new_chart_type) for prompt in
             prompt_templates.chart_conversion])


def convert_vertical_bar_type(data: Data, visual_attrs: VisualAttribute, new_chart_type: Optional[Literal[
    "grouped vertical bar", "stacked vertical bar", "grouped horizontal bar", "stacked horizontal bar",]] = None) -> \
        Tuple[Data, VisualAttribute, List[str]]:
    old_chart_type = visual_attrs.global_attrs["chart_type"]

    if new_chart_type is None:
        random.choice([chart_type for chart_type in
                       [ChartType.GROUPED_VERTICAL_BAR.value, ChartType.STACKED_VERTICAL_BAR.value,
                        ChartType.GROUPED_HORIZONTAL_BAR.value, ChartType.STACKED_HORIZONTAL_BAR]
                       if chart_type != old_chart_type
                       ]
                      )
    global_attrs = deepcopy(visual_attrs.global_attrs)
    global_attrs["chart_type"] = new_chart_type
    # Todo: The colors and hatches might be different for grouped bars versus stacked bars because legends may differ
    return (Data(deepcopy(data.data_table), data.chart_title, data.x_axis_title, data.y_axis_title),
            VisualAttribute(global_attrs, deepcopy(visual_attrs.specific_attrs), visual_attrs.specific_attrs_key),
            [prompt.format(old_chart_type=old_chart_type, new_chart_type=new_chart_type) for prompt in
             prompt_templates.chart_conversion])
