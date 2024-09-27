from chartcrafter.chart_plotter.constants import ChartType

from chartcrafter.chart_plotter.plotters import (plot_line_chart, plot_grouped_vertical_bar,
                                                                        plot_stacked_vertical_bar,
                                                                        plot_grouped_horizontal_bar,
                                                                        plot_stacked_horizontal_bar)
from chartcrafter.data_processor import Data, VisualAttribute


def plot_chart_from_unified_attr(data: Data, visual_attrs: VisualAttribute):
    chart_type = visual_attrs.global_attrs["chart_type"].lower().strip()
    if chart_type == ChartType.LINE.value:
        return plot_line_chart(data, visual_attrs)
    elif chart_type == ChartType.GROUPED_VERTICAL_BAR.value:
        return plot_grouped_vertical_bar(data, visual_attrs)
    elif chart_type == ChartType.STACKED_VERTICAL_BAR.value:
        return plot_stacked_vertical_bar(data, visual_attrs)
    elif chart_type == ChartType.GROUPED_HORIZONTAL_BAR.value:
        return plot_grouped_horizontal_bar(data, visual_attrs)
    elif chart_type == ChartType.STACKED_HORIZONTAL_BAR.value:
        return plot_stacked_horizontal_bar(data, visual_attrs)
    else:
        raise NotImplementedError(f"Chart type '{visual_attrs.global_attrs['chart_type']}'")
