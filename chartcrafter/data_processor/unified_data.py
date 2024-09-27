from dataclasses import dataclass
from typing import Tuple
from copy import deepcopy
import pandas as pd


@dataclass
class Data:
    data_table: pd.DataFrame
    chart_title: str
    x_axis_title: str
    y_axis_title: str

    @property
    def legend_labels(self) -> Tuple[str]:
        return tuple(self.data_table.columns[1:])

    def to_unified_data(self):
        return {
            "data_table": (self.data_table.to_csv(index=False, sep="|")
                           .replace("|", " | ")
                           .replace("\n", " <0x0A> ")
                           ),
            "chart_title": self.chart_title,
            "x_axis_title": self.x_axis_title,
            "y_axis_title": self.y_axis_title
        }

    def copy(self):
        return Data(
            self.data_table.copy(deep=True),
            self.chart_title,
            self.x_axis_title,
            self.y_axis_title
        )


@dataclass
class VisualAttribute:
    global_attrs: dict
    specific_attrs: dict
    specific_attrs_key: str  # To know the JSON key for read/write

    def to_unified_data(self):
        return {
            "global_properties": self.global_attrs,
            self.specific_attrs_key: self.specific_attrs
        }

    def copy(self):
        return VisualAttribute(
            deepcopy(self.global_attrs),
            deepcopy(self.specific_attrs),
            self.specific_attrs_key
        )
