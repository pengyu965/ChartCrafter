import datetime
import json
import os
import random
from typing import Optional, Literal, Tuple, List
from tqdm import tqdm
import matplotlib.pyplot as plt
from tqdm import tqdm
import sys

from chartcrafter.chart_editor.chart_converter import (convert_line_to_bar,
                                                                              convert_bar_to_line,
                                                                              convert_vertical_bar_type)
from chartcrafter.chart_editor.data_editors import apply_range_filter, apply_series_filter, \
    remove_data_point, remove_data_series, add_data_point, add_data_series
from chartcrafter.chart_editor.layout_editors import toggle_grid, change_legend_position
from chartcrafter.chart_editor.style_editors import (change_line_attr, change_bar_attr,
                                                                            change_chart_titles_font, change_font_size)
from chartcrafter.chart_plotter import plot_chart_from_unified_attr
from chartcrafter.chart_plotter.constants import ChartType
from chartcrafter.data_processor import Data, VisualAttribute, get_data_from_pmc_json
from chartcrafter.data_processor.unified_attrs_generator import generate_random_unified_attrs
from chartcrafter.utils import (create_dirs, update_edits_dict, get_counts_from_edits_json)


def get_chart_pairs(data: Data, visual_attrs: VisualAttribute,
                    selected_edit: Optional[Literal["style_edits", "layout_edits", "format_edits", "data_edits"]] = None
                    ) -> Tuple[
    Data, VisualAttribute, plt.Figure, Data, VisualAttribute, plt.Figure, List[str], List[str]]:
    # Randomly select an edit to be made
    chart_type = visual_attrs.global_attrs["chart_type"]
    data_, visual_attrs_ = None, None
    if selected_edit is None:
        selected_edit = random.choice(list(edits_required[chart_type]))

    attr_key_path = [chart_type, selected_edit]
    if selected_edit == "style_edits":
        # Decide whether common edit or chart specific edits such as colors, markers, line styles
        edit_category = random.choice(list(edits_required[chart_type][selected_edit]))
        available_attrs = [attr for attr in edits_required[chart_type][selected_edit][edit_category]]
        selected_attr = random.choice(available_attrs)
        attr_key_path.append(edit_category)
        attr_key_path.append(selected_attr)
        if edit_category == "common":
            if selected_attr == "font":
                # Change font family
                visual_attrs_, prompts = change_chart_titles_font(visual_attrs)
            else:
                # Increase/Decrease font size
                visual_attrs_, prompts = change_font_size(visual_attrs, mutate_original_attr=True)

        else:
            if chart_type == ChartType.LINE.value:
                data_, visual_attrs_, prompts = change_line_attr(data, visual_attrs, selected_attr)
            elif chart_type in (ChartType.GROUPED_VERTICAL_BAR.value, ChartType.STACKED_VERTICAL_BAR.value,
                                ChartType.STACKED_HORIZONTAL_BAR.value, ChartType.GROUPED_HORIZONTAL_BAR.value):
                data_, visual_attrs_, prompts = change_bar_attr(data, visual_attrs, selected_attr)
            else:
                raise NotImplementedError(f"Chart Type: {chart_type}")

    elif selected_edit == "layout_edits":
        change_type = random.choice([attr for attr in edits_required[chart_type][selected_edit]])
        attr_key_path.append(change_type)
        if change_type == "grid":
            visual_attrs_, prompts = toggle_grid(visual_attrs)
        else:
            visual_attrs_, prompts = change_legend_position(visual_attrs)

    elif selected_edit == "format_edits":
        available_formats = [format_ for format_ in edits_required[chart_type][selected_edit]]
        new_chart_type = random.choice(available_formats)
        attr_key_path.append(new_chart_type)

        if chart_type == ChartType.LINE.value:
            data_, visual_attrs_, prompts = convert_line_to_bar(data, visual_attrs, new_chart_type)
        elif new_chart_type == ChartType.LINE.value:
            data_, visual_attrs_, prompts = convert_bar_to_line(data, visual_attrs)
        else:
            data_, visual_attrs_, prompts = convert_vertical_bar_type(data, visual_attrs, new_chart_type)
    else:
        edit_category = random.choice(list(edits_required[chart_type][selected_edit]))
        sub_edit_category = random.choice(list(edits_required[chart_type][selected_edit][edit_category]))
        attr_key_path.append(edit_category)
        attr_key_path.append(sub_edit_category)
        if sub_edit_category == "range_based":
            data_, prompts = apply_range_filter(data)
        elif sub_edit_category == "series_based":
            data_, visual_attrs_, prompts = apply_series_filter(data, visual_attrs)
        elif sub_edit_category == "add_data_point":
            data_, prompts = add_data_point(data, visual_attrs, mutate=True)
        elif sub_edit_category == "remove_data_point":
            data_, prompts, _, _ = remove_data_point(data, visual_attrs)
        elif sub_edit_category == "add_data_series":
            data_, visual_attrs_, prompts = add_data_series(data, visual_attrs, mutate=True)
        elif sub_edit_category == "remove_data_series":
            data_, visual_attrs_, prompts, _, _ = remove_data_series(data, visual_attrs)
        else:
            raise NotImplementedError(f"Data edit: {edit_category}: {sub_edit_category}")

    chart = plot_chart_from_unified_attr(data, visual_attrs)

    # Copy original data and visual attrs as edited if do not exist
    if data_ is None:
        data_ = data.copy()
    if visual_attrs_ is None:
        visual_attrs_ = visual_attrs.copy()
    chart_ = plot_chart_from_unified_attr(data_, visual_attrs_)

    update_edits_dict(edits_required, attr_key_path)

    return data, visual_attrs, chart, data_, visual_attrs_, chart_, prompts, attr_key_path


if __name__ == "__main__":
    file_dir = "./adobe_train_gt/"
    output_path = "./out/"

    with open("./chartcrafter/chart_categories.json", "r") as json_file:
        categories = json.load(json_file)

    for split in ["train","val","test","test_small"]:
    # for split in ["test_small"]:
        split_path = os.path.join(output_path, split)
        create_dirs(*[os.path.join(split_path, sub_dir) for sub_dir in
                    ("images", "edited_images")])
    
        with open(f'./chartcrafter/edits_required_{split}.json') as json_file:
            edits_required: dict = json.load(json_file)
            implemented_chart_types = {chart_type.value for chart_type in ChartType}
            for chart_type in list(edits_required.keys()):
                if chart_type not in implemented_chart_types:
                    print(f"{chart_type} is not implemented. Discarding from edits required JSON.")
                    edits_required.pop(chart_type)
        # Uncomment below code and pass the list of edits and the chart_types too, to be performed
        # limit_edits(edits_required, included_edits=["data_edits"])
        edit_summary = {}
        if not os.path.isabs(split_path):
            split_path = os.path.abspath(split_path)

        edits_count = get_counts_from_edits_json(edits_required)
        main_progress_bar = tqdm(edits_count.items(), total=len(edits_count), leave=True, desc="Chart Type", position=0,
                                bar_format="{l_bar}%s{bar}%s{r_bar}" % ("\033[91m", "\033[0m"))
        
        
        if "test" in split:
            split = "test"

        for chart_type, chart_edit_count in main_progress_bar:
            main_progress_bar.set_description(f"Chart Type => {chart_type}")
            idx = 0
            n_files = len(categories[chart_type][split])
            progress_bars = {}  # dict to keep track of each individual bar
            # Create a new progress bar for each edit type
            for edit_type, value in chart_edit_count.items():
                # leave=True so bars remain displayed, position=len(progress_bars) to avoid overwriting each other
                progress_bars[edit_type] = tqdm(total=value, desc=f"{chart_type}=>{edit_type}", leave=True,
                                                position=len(progress_bars) + 1)

            while chart_type in edits_required:
                chart_id = categories[chart_type][split][idx]
                file_path = os.path.join(file_dir, f"{chart_id}.json")
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, "r") as f:
                            pmc_dict = json.load(f)
                        data, _ = get_data_from_pmc_json(pmc_dict)
                        visual_attrs = generate_random_unified_attrs(data, chart_type)

                        (data,visual_attrs,chart,
                        data_,visual_attrs_,chart_,
                        prompts,edit_type_path) = get_chart_pairs(data, visual_attrs)

                        # Generate unique id per chart per edit to avoid conflicts
                        unique_id = str(datetime.datetime.now().timestamp()).replace(".", "-")
                        output_image_name = f"{chart_id}-{unique_id}.png"
                        orig_img_path = "images/"+output_image_name
                        edit_img_path = "edited_images/"+output_image_name

                        chart.savefig(os.path.join(split_path,orig_img_path))
                        chart_.savefig(os.path.join(split_path,edit_img_path))
    
                        plt.close(chart)
                        plt.close(chart_)

                        edit_summary[len(edit_summary) + 1] = {
                            "original_image": orig_img_path,
                            "editing_prompts": prompts,
                            "edit_type": edit_type_path,
                            "edited_image": edit_img_path,
                            "visual_attributes": visual_attrs.to_unified_data(),
                            "edited_visual_attributes": visual_attrs_.to_unified_data(),
                            "underlying_data": data.to_unified_data(),
                            "edited_underlying_data": data_.to_unified_data()
                        }
                        current = progress_bars[edit_type_path[1]]
                        current.update(1)
                    except json.JSONDecodeError as e:
                        print(f"Invalid JSON, skipping: {chart_id}")
                    except NotImplementedError:
                        print(f"Data edits yet to be implemented: {chart_id}")
                    except ValueError as e:
                        print(f"ValueError {e} chart_id: {chart_id}")
                    except Exception as e:
                        # ToDo: Fix other error cases
                        # print(e, chart_id)
                        pass
                idx = (idx + 1) % n_files
                for edit, each_progress in list(progress_bars.items()):
                    each_progress.close()
                    progress_bars.pop(edit)
        with open(os.path.join(split_path, "summary.json"), "w") as summary_file:
            json.dump(edit_summary, summary_file, indent=2)
