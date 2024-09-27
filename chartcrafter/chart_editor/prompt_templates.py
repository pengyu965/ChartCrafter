# Chart specific attrs changes
# color_change = "Change the {chart_entity} color for {legend_label} to {new_color}"
# line_style_change = "Change the line style for {legend_label} to {new_style}"
# marker_change = "Change the marker for {legend_label} to {new_marker}"
# bar_pattern_change = "Change the bar pattern for {legend_label} to {new_pattern}"

specific_attr_change = (
    "Modify the {attr_name} of {chart_entity} for {legend_label} to {new_value}",
    "Adjust the {attr_name} for {chart_entity} related to {legend_label} to {new_value}",
    "Update the {attr_name} in {chart_entity} for {legend_label} to {new_value}",
    "Set {new_value} for {attr_name} of {chart_entity} associated with {legend_label}",
    "Change {attr_name} for {legend_label} in {chart_entity} to {new_value}",
    "Revise the {attr_name} of {chart_entity} attributed to {legend_label} as {new_value}",
    "Alter the {attr_name} belonging to {chart_entity} linked with {legend_label} to {new_value}"
)
# Global attrs changes
font_change = (
    "Update the font of {entity} to {new_font}",
    "Modify the {entity} font to {new_font}",
    "Change {entity} font to {new_font}",
    "Set the font of {entity} to {new_font}",
    "Revise {entity} font as {new_font}",
    "Adjust {entity} font to {new_font}",
    "Switch {entity} font to {new_font}"
)
# font_size_increase = "Increase the font size for {entity}"
# font_size_decrease = "Decrease the font size for {entity}"
font_size_change = ("{change_type} the font size of {entity}", )

grid_addition = (
    "Introduce grid lines to the plot",
    "Include grid lines on the given plot",
    "Add grid lines to the plot",
    "Apply grid lines to the given plot",
    "Activate grid lines on the plot",
    "Display grid lines on the given plot",
    "Enable grid lines for the plot"
)
grid_removal = (
    "Remove grid lines from the plot",
    "Erase grid lines on the given plot",
    "Delete grid lines from the plot",
    "Hide grid lines on the given plot",
    "Omit grid lines on the plot",
    "Deactivate grid lines for the plot",
    "Eliminate grid lines from the given plot"
)

legend_reposition = (
    "Shift the legend to {new_position}",
    "Reposition the legend to {new_position}",
    "Relocate the legend to {new_position}",
    "Move the legend position to {new_position}",
    "Adjust the legend to {new_position}",
    "Change the legend location to {new_position}",
    "Place the legend at {new_position}"
)

# Chart conversion
chart_conversion = (
    "Switch the {old_chart_type} Chart to {new_chart_type} Chart",
    "Transform the {old_chart_type} Chart into a {new_chart_type} Chart",
    "Generate {new_chart_type} from {old_chart_type}",
    "Convert the {old_chart_type} Chart to {new_chart_type} format",
    "Update the chart from {old_chart_type} to {new_chart_type} style",
    "Alter the {old_chart_type} Chart to {new_chart_type} Chart format",
    "Modify the chart type to {new_chart_type} from {old_chart_type}"
)

# Data Edits
range_based_filter = "Show only data from {start_col} to {end_col}"
series_based_filter = "Show only data for Series {series_1} and Series {series_2}"
data_point_addition = "Add values {values_list_str} for following {label_add_from}"
data_point_deletion = "Delete the data for all data series on {label_to_delete}"
data_series_addition = "Add the following data for {criteria}, {values_list_str}"
