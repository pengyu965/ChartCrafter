import matplotlib.pyplot as plt
import numpy as np

from chartcrafter.chart_plotter.chart_utils import get_bar_widths_and_center_positions, \
    truncate_chart_title, transpose_data_for_stacked_bar
from chartcrafter.chart_plotter.constants import LINE_STYLES_STR_MAP, FIG_SIZE
from chartcrafter.data_processor import Data, VisualAttribute


def init_fig(**kwargs):
    fig = plt.figure(figsize=FIG_SIZE, **kwargs, )
    ax = fig.add_subplot(111)
    ax.ticklabel_format(style="plain")

    return fig, ax


def plot_common_attrs(plotter):
    def func(*args, **kwargs):
        fig, ax = plotter(*args, **kwargs)
        args = list(args)
        for idx, key_param in enumerate(("data", "visual_attrs")):
            if kwargs.get(key_param):
                args[idx] = kwargs.get(key_param)

        data, visual_attrs = args

        ax.set_xlabel(data.x_axis_title, **visual_attrs.global_attrs.get("xlabel_params", {}))
        ax.set_ylabel(data.y_axis_title, **visual_attrs.global_attrs.get("ylabel_params", {}))
        ax.set_title(truncate_chart_title(data.chart_title), **visual_attrs.global_attrs.get("chart_title_params", {}))
        if not (len(data.legend_labels) == 1 and data.legend_labels[0] == ""):
            ax.legend(**visual_attrs.global_attrs.get("legend_params", {}))
        ax.grid(**visual_attrs.global_attrs.get("grid_params", {}))
        ax.tick_params(**visual_attrs.global_attrs.get("x_tick_params", {}))
        ax.tick_params(**visual_attrs.global_attrs.get("y_tick_params", {}))

        fig.tight_layout()

        return fig

    return func


@plot_common_attrs
def plot_line_chart(data: Data, visual_attrs: VisualAttribute):
    fig, ax = init_fig()
    for idx, col in enumerate(data.data_table.columns[1:]):
        line_kwargs = {"label": str(col)}
        for key in ("linestyles", "colors", "markers"):
            line_kwargs[key[:-1]] = visual_attrs.specific_attrs[key][idx]
        else:
            line_kwargs["linestyle"] = LINE_STYLES_STR_MAP.get(line_kwargs["linestyle"])
        ax.plot(data.data_table.iloc[:, 0], data.data_table[col], **line_kwargs)
    return fig, ax


@plot_common_attrs
def plot_grouped_vertical_bar(data: Data, visual_attrs: VisualAttribute):
    fig, ax = init_fig()
    n_bars, n_groups = data.data_table.shape[0], data.data_table.shape[1] - 1
    emp, bar_width, center_positions = get_bar_widths_and_center_positions(n_bars, n_groups)

    first_col = data.data_table.columns[0]

    for idx, col in enumerate(data.data_table.columns[1:]):
        base_positions = emp - (n_groups * bar_width / 2) + (idx * bar_width)
        kwargs = dict(width=bar_width,
                      label=str(col),
                      color=visual_attrs.specific_attrs["colors"][idx],
                      hatch=visual_attrs.specific_attrs["hatches"][idx]
                      )
        args = [base_positions]
        args.append(data.data_table[[col]].rename(columns={col: "y"})["y"])
        ax.bar(*args, **kwargs)

    ax.set_xticks(center_positions)
    ax.set_xticklabels(data.data_table[first_col])

    return fig, ax


@plot_common_attrs
def plot_stacked_vertical_bar(data, visual_attrs):
    df = transpose_data_for_stacked_bar(data.data_table)
    fig, ax = init_fig()
    emp, bar_width, center_positions = get_bar_widths_and_center_positions(df.shape[1] - 1, 1)

    x_ticks = df.columns[1:].astype("string").fillna("")

    bottoms = np.zeros(df.shape[1] - 1)
    for idx in range(df.shape[0]):
        # for idx, row in df.iterrows():
        ax.bar(x_ticks, df.iloc[idx, 1:].values,
               label=str(df.iat[idx, 0]),
               bottom=bottoms,
               hatch=visual_attrs.specific_attrs['hatches'][idx],
               color=visual_attrs.specific_attrs['colors'][idx],
               width=bar_width,
               )

        bottoms += df.iloc[idx, 1:]

    ax.set_xticks(center_positions)
    ax.set_xticklabels(x_ticks)

    return fig, ax


@plot_common_attrs
def plot_grouped_horizontal_bar(data: Data, visual_attrs: VisualAttribute):
    fig, ax = init_fig()
    n_bars, n_groups = data.data_table.shape[0], data.data_table.shape[1] - 1
    emp, bar_width, center_positions = get_bar_widths_and_center_positions(n_bars, n_groups)

    first_col = data.data_table.columns[0]

    for idx, col in enumerate(data.data_table.columns[1:]):
        base_positions = emp - (n_groups * bar_width / 2) + (idx * bar_width)
        kwargs = dict(height=bar_width,
                      label=str(col),
                      color=visual_attrs.specific_attrs["colors"][idx],
                      hatch=visual_attrs.specific_attrs["hatches"][idx]
                      )
        args = [base_positions]
        args.append(data.data_table[[col]].rename(columns={col: "y"})["y"])
        ax.barh(*args, **kwargs)

    ax.set_yticks(center_positions)
    ax.set_yticklabels(data.data_table[first_col])

    return fig, ax


@plot_common_attrs
def plot_stacked_horizontal_bar(data, visual_attrs):
    df = transpose_data_for_stacked_bar(data.data_table)
    fig, ax = init_fig()
    emp, bar_width, center_positions = get_bar_widths_and_center_positions(df.shape[1] - 1, 1)

    y_ticks = df.columns[1:].astype("string").fillna("")

    lefts = np.zeros(df.shape[1] - 1)
    for idx in range(df.shape[0]):
        # for idx, row in df.iterrows():
        ax.barh(y_ticks, df.iloc[idx, 1:].values,
                label=str(df.iat[idx, 0]),
                left=lefts,
                hatch=visual_attrs.specific_attrs['hatches'][idx],
                color=visual_attrs.specific_attrs['colors'][idx],
                height=bar_width,
                )

        lefts += df.iloc[idx, 1:]

    ax.set_yticks(center_positions)
    ax.set_yticklabels(y_ticks)

    return fig, ax
