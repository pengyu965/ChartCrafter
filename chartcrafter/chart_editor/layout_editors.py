import random
from copy import deepcopy
from typing import Optional, Tuple, List

from chartcrafter.chart_editor import prompt_templates
from chartcrafter.chart_plotter.constants import GRID_LINE_STYLE, LEGEND_POSITIONS, \
    LEGEND_POSITION_MAP
from chartcrafter.data_processor import VisualAttribute


def toggle_grid(visual_attrs: VisualAttribute) -> Tuple[VisualAttribute, List[str]]:
    global_attrs = deepcopy(visual_attrs.global_attrs)
    if global_attrs["grid_params"]["visible"]:
        global_attrs["grid_params"] = {"visible": False}
        prompt = prompt_templates.grid_removal
    else:
        global_attrs["grid_params"] = {"visible": True, "linestyle": random.choice(GRID_LINE_STYLE)}
        prompt = prompt_templates.grid_addition

    return (VisualAttribute(global_attrs, deepcopy(visual_attrs.specific_attrs), visual_attrs.specific_attrs_key),
            list(prompt))


def change_legend_position(visual_attrs: VisualAttribute,
                           new_position: Optional[str] = None) -> Tuple[VisualAttribute, List[str]]:
    if new_position is None:
        old_position = visual_attrs.global_attrs["legend_params"]["loc"]
        available_legend_positions = [position for position in LEGEND_POSITIONS if position != old_position]
        new_position = random.choice(available_legend_positions)

    global_attrs = deepcopy(visual_attrs.global_attrs)
    global_attrs["legend_params"]["loc"] = new_position

    return (VisualAttribute(global_attrs, deepcopy(visual_attrs.specific_attrs), visual_attrs.specific_attrs_key),
            [prompt.format(new_position=LEGEND_POSITION_MAP[new_position]) for prompt in
             prompt_templates.legend_reposition])
