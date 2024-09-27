import random
from copy import deepcopy
from typing import Literal, Optional, Tuple, List

from chartcrafter.chart_editor import prompt_templates
from chartcrafter.chart_plotter.constants import COLOR_OPTIONS, HATCH_OPTIONS, MARKER_OPTIONS, \
    LINE_STYLES, FONTS, TICK_FONT_SIZE, TITLE_FONT_SIZE
from chartcrafter.data_processor import VisualAttribute, Data

chart_attr_name_map = {
    "colors": "color",
    "hatches": "hatch",
    "linestyles": "line style",
    "markers": "marker"
}

text_entity_map = {
    "chart_title": "Chart Title",
    "x_label": "X Axis Title",
    "y_label": "Y Axis Title",
    "axes_title": "Axes Title",
    "x_tick": "X Axis Tick Label",
    "y_tick": "Y Axis Tick Label",
    "axes_tick": "Axes Tick Label"
}


def change_bar_attr(data: Data, visual_attrs: VisualAttribute,
                    attr_name: Literal["colors", "hatches"] = "colors", bar_index=None,
                    new_value=None) -> Tuple[Data, VisualAttribute, List[str]]:
    if bar_index is None:
        bar_index = random.randint(0, len(data.legend_labels) - 1)
    if new_value is None:
        # Ensure new color or hatch is not same as old
        old_value = visual_attrs.specific_attrs[attr_name][bar_index]
        all_options = COLOR_OPTIONS if attr_name == "colors" else HATCH_OPTIONS
        used_options = set(visual_attrs.specific_attrs[attr_name])
        # Trying to get unused value of color or hatch
        available_options = [option for option in all_options if option not in used_options]

        # If all values have been used, try to use the value different than the current one
        if not available_options:
            available_options = [option for option in all_options if option != old_value]

        new_value = random.choice(available_options)

    specific_attrs = deepcopy(visual_attrs.specific_attrs)
    specific_attrs[attr_name][bar_index] = new_value

    return (data,
            VisualAttribute(deepcopy(visual_attrs.global_attrs), specific_attrs, visual_attrs.specific_attrs_key),
            [prompt.format(chart_entity="bar", attr_name=chart_attr_name_map[attr_name],
                           legend_label=data.legend_labels[bar_index],
                           new_value=new_value) for prompt in prompt_templates.specific_attr_change]
            )


def change_line_attr(data: Data, visual_attrs: VisualAttribute,
                     attr_name: Literal["colors", "linestyles", "markers"] = "colors", line_index=None,
                     new_value=None) -> Tuple[Data, VisualAttribute, List[str]]:
    if line_index is None:
        line_index = random.randint(0, len(data.legend_labels) - 1)
    if new_value is None:
        old_value = visual_attrs.specific_attrs[attr_name][line_index]
        used_options = set(visual_attrs.specific_attrs[attr_name])
        if attr_name == "colors":
            all_options = COLOR_OPTIONS
        elif attr_name == "linestyles":
            all_options = LINE_STYLES
        elif attr_name == "markers":
            all_options = MARKER_OPTIONS
        else:
            raise NotImplementedError(f"Attribute: {attr_name}")

        # Trying to get unused value of color. line style, or marker
        available_options = [option for option in all_options if option not in used_options]

        # If all values have been used, try to use the value different than the current one
        if not available_options:
            available_options = [option for option in all_options if option != old_value]

        new_value = random.choice(available_options)

    specific_attrs = deepcopy(visual_attrs.specific_attrs)
    specific_attrs[attr_name][line_index] = new_value

    return (data,
            VisualAttribute(deepcopy(visual_attrs.global_attrs), specific_attrs, visual_attrs.specific_attrs_key),
            [prompt.format(chart_entity="line", attr_name=chart_attr_name_map[attr_name],
                           legend_label=data.legend_labels[line_index],
                           new_value=new_value) for prompt in prompt_templates.specific_attr_change]
            )


def change_chart_titles_font(visual_attrs: VisualAttribute,
                             entity: Optional[Literal["chart_title", "axes_title", "x_label", "y_label"]] = None,
                             new_font: Optional[str] = None) -> Tuple[VisualAttribute, List[str]]:
    if not entity:
        entity = random.choice(["chart_title", "x_label", "y_label", "axes_title"])
    if entity == "axes_title":
        global_attrs_keys = ["x_label_params", "y_label_params"]
    else:
        global_attrs_keys = [f"{entity}_params"]

    global_attrs = deepcopy(visual_attrs.global_attrs)
    if new_font is None:
        # Ensure new font is not same as old
        old_font = global_attrs[global_attrs_keys[0]]["fontname"]
        new_font = random.choice([font for font in FONTS if font != old_font])

    for key in global_attrs_keys:
        global_attrs[key]["fontname"] = new_font

    return (VisualAttribute(global_attrs, deepcopy(visual_attrs.specific_attrs), visual_attrs.specific_attrs_key),
            [prompt.format(entity=text_entity_map.get(entity, entity), new_font=new_font) for prompt in
             prompt_templates.font_change])


def change_font_size(visual_attrs: VisualAttribute,
                     change_type: Optional[Literal["increase", "decrease"]] = None,
                     entity: Optional[Literal[
                         "chart_title", "axes_title", "x_label", "y_label", "axes_tick", "x_tick", "y_tick"]] = None,
                     new_size: Optional[str] = None,
                     mutate_original_attr: bool = False) -> Tuple[VisualAttribute, List[str]]:
    if not entity:
        entity = random.choice(["chart_title", "axes_title", "x_label", "y_label", "axes_tick", "x_tick", "y_tick"])
    key_paths = None
    if "tick" in entity:
        all_available_sizes = TICK_FONT_SIZE
        font_size_attr_name = "labelsize"
        if entity == "axes_tick":
            key_paths = [["x_tick_params", font_size_attr_name], ["y_tick_params", font_size_attr_name]]
            current_size = visual_attrs.global_attrs["x_tick_params"][font_size_attr_name]
        else:
            current_size = visual_attrs.global_attrs[f"{entity}_params"][font_size_attr_name]
    else:
        all_available_sizes = TITLE_FONT_SIZE
        font_size_attr_name = "fontsize"
        if entity == "axes_title":
            key_paths = [["x_label_params", font_size_attr_name], ["y_label_params", font_size_attr_name]]
            current_size = visual_attrs.global_attrs["x_label_params"]["fontsize"]
        else:
            current_size = visual_attrs.global_attrs[f"{entity}_params"][font_size_attr_name]
    if key_paths is None:
        key_paths = [[f"{entity}_params", font_size_attr_name]]

    if not change_type:
        change_type = random.choice(["increase", "decrease"])

    if change_type == "decrease":
        # reverse the list for decreasing the font size
        last_available = "smallest"
        all_available_sizes = all_available_sizes[::-1]
    else:
        last_available = "largest"

    if new_size is None:
        available_sizes = all_available_sizes[:]
        start_index = 0
        while start_index < len(available_sizes) - 1:
            if available_sizes[start_index] == current_size:
                break
            start_index += 1
        if start_index == len(available_sizes) - 1:
            if not mutate_original_attr:
                raise ValueError(f"{entity} already has {last_available} size available")
            else:
                # Change the original size to facilitate the increase/decrease operation
                start_index = random.randint(0, len(available_sizes) - 2)
                for key_path in key_paths:
                    dict_ = visual_attrs.global_attrs
                    for key in key_path[:-1]:
                        dict_ = dict_[key]
                    dict_[key_path[-1]] = random.choice(all_available_sizes[:start_index + 1])

        new_size = random.choice(available_sizes[start_index + 1:])

    global_attrs = deepcopy(visual_attrs.global_attrs)
    for key_path in key_paths:
        dict_ = global_attrs
        for key in key_path[:-1]:
            dict_ = dict_[key]
        dict_[key_path[-1]] = new_size

    return (VisualAttribute(global_attrs, deepcopy(visual_attrs.specific_attrs), visual_attrs.specific_attrs_key),
            [prompt.format(change_type=change_type.title(),
                           entity=text_entity_map.get(entity, entity)) for prompt in prompt_templates.font_size_change]
            )
