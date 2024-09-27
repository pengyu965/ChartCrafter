import re

import numpy as np
import pandas as pd

# Enclose pattern string by parenthesis to keep the split chars as well--to be used in future to join if needed
title_split_pattern = re.compile("(" + '|'.join((',', ':', r'\(', r'\[', r'\bor\b', r'\band\b')) + ")")


def truncate_chart_title(text, characters=None):
    # Create a pattern for the characters to split on
    if characters:
        pattern = re.compile("(" + '|'.join(map(re.escape, characters)) + ")")
    else:
        pattern = title_split_pattern

    # Use re.split to split the text based on the pattern
    parts = pattern.split(text)

    # Remove empty strings from the result
    result = ([part for part in parts if part] or [""])[0]

    split_result = result.split(' ')

    if len(split_result) > 6:
        return " ".join(split_result[:6])

    return result


def get_xtick_label_average_length(data_frame):
    return (
        int(
            np.ceil(
                data_frame[data_frame.columns[0]].astype(str).str.len().sum() / data_frame.shape[0]
            )
        )
    )


def get_bar_widths_and_center_positions(n_bars, n_groups=1):
    emp = np.arange(n_bars)
    bar_padding = 0.05
    bar_width = (1 / (n_bars + 1)) - bar_padding

    leftmost_positions = emp - (n_bars * bar_width / 2)
    rightmost_positions = emp + (n_bars * bar_width / 2) - bar_width
    center_positions = (leftmost_positions + rightmost_positions) / 2
    if n_groups == 1:
        center_positions += bar_width / 2

    return emp, bar_width, center_positions


def transpose_data_for_stacked_bar(df: pd.DataFrame) -> pd.DataFrame:
    x_label = [df.columns[0]]
    df = df.set_index(x_label).T.reset_index(names=x_label)
    df.index.name = None
    return df
    # df = df.T.reset_index()  # Create a copy of the dataframe
    # df.columns = df.iloc[0, :].values
    # df = df.drop(index=0).reset_index(drop=True)
    # return df
