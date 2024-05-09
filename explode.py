"""Module providing functions to transform tables"""
import re
import pandas as pd
COUNTER = 0


def is_composite(val: str):
    """Check if value is composite value"""
    date_pattern = re.compile(r'(\d{4}/\d{2}/\d{2})|(\d{2}/\d{2}/\d{4})')
    if date_pattern.match(str(val)):
        return False
    else:
        return ',' in str(val) or '/' in str(val) or "|" in str(val)


def is_explode(table_file: str) -> bool:
    """Check if it need explode operation"""
    data = pd.read_csv(table_file)
    for col in data.columns:
        if data[col].apply(is_composite).any():
            return True
    return False


def parse_string_to_list(s: str) -> list:
    """Check if the string contains commas or slashes"""
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
