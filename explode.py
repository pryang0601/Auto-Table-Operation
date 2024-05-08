"""Module providing functions to transform tables"""
import pandas as pd
import math
COUNTER = 0


def parse_string_to_list(s: str) -> list:
    # Check if the string contains commas or slashes
    if pd.isna(s):
        return s
    if ',' in s:
        return [x.strip() for x in s.split(',')]
    elif '/' in s:
        return [x.strip() for x in s.split('/')]
    else:
        return [s]


def explode(table_file: str, output_dir: str, explode_idx: int) -> None:
    """Perform subtitle operation"""
    global COUNTER
    COUNTER += 1
    data = pd.read_csv(table_file)
    data.iloc[:, explode_idx] = data.iloc[:, explode_idx].map(parse_string_to_list)
    data_explode = data.explode(data.columns[explode_idx])
    data_explode.to_csv(f"{output_dir}/explode{COUNTER}.csv", index=False)
