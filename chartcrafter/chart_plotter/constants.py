from enum import Enum

FIG_SIZE = (10, 8)
HATCH_OPTIONS = ['xx', '.', '*', '/', '\\', None]
COLOR_OPTIONS = ["b", 'g', 'r', 'c', 'm', 'y', 'k']
MARKER_OPTIONS = ["o", "^", "s", "*", None]
LINE_STYLES = ['solid', 'dotted', 'dashed', 'dashdot', 'dense dotted', 'loose dotted', 'dense dashed', 'loose dashed']
LINE_STYLES_STR_MAP = {'dense dotted': (0, (1, 1)), 'loose dotted': (0, (1, 3)),
                       'dense dashed': (0, (2, 1)), 'loose dashed': (0, (10, 3))}

FONTS = ['monospace', 'Serif', 'sans-serif', 'Arial Black']
TITLE_FONT_SIZE = ['medium', 'large', 'x-large']
TICK_FONT_SIZE = ['small', 'medium']

GRID_LINE_STYLE = ['solid', 'dashed']

LEGEND_POSITIONS = [0, 1, 2, 3, 4, 8, 9]  # ToDo: May be remove 8 later (Its currently mentioned in the paper)
LEGEND_POSITION_MAP = {
    0: "best",
    1: "upper right",
    2: "upper left",
    3: "lower left",
    4: "lower right",
    8: "lower center",  # ToDo: May be remove this later (Its currently mentioned in the paper)
    9: "upper center"
}
LEGEND_N_COLUMNS = [1, 2, 3]


class ChartType(Enum):
    LINE = "line"
    GROUPED_VERTICAL_BAR = "grouped vertical bar"
    STACKED_VERTICAL_BAR = "stacked vertical bar"
    GROUPED_HORIZONTAL_BAR = "grouped horizontal bar"
    STACKED_HORIZONTAL_BAR = "stacked horizontal bar"
