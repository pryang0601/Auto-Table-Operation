"""Module providing functions to transform tables"""
import re
import locale
from typing import Tuple
import pandas as pd
COUNTER = 0


def is_locale_number(value):
    """Check if the value is a number like 8,000"""
    try:
        # Try converting the string to a float
        number = locale.atof(value)
        # Conversion succeeded, so it's a number
        return True
    except ValueError:
        # Conversion failed, not a valid number
        return False


def is_composite(val: str):
    """Check if value is composite value"""
    date_pattern = re.compile(r'(\d{4}/\d{2}/\d{2})|(\d{2}/\d{2}/\d{4})')
    months = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"]
    for month in months:
        if month in str(val):
            return False
    if date_pattern.match(str(val)):
        return False
    elif is_locale_number(str(val)) or 'e.g' in str(val):
        return False    #E.g., 8,000
    else:
        return ',' in str(val) or '/' in str(val) or "|" in str(val)


def is_explode(table_file: str) -> Tuple[bool, list]:
    """Check if it need explode operation"""
    data = pd.read_csv(table_file)
    for idx,col in enumerate(data.columns):
        if "," in col or "/" in col or "|" in col:
            continue
        if data[col].apply(is_composite).any():
            return True, [idx]
    return False, -1


def parse_string_to_list(s: str) -> list:
    """Check if the string contains commas or slashes"""
    if not isinstance(s, str):
        return s
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
    # print(data.iloc[:,explode_idx])
    data = data.explode(data.columns[explode_idx])
   # print(data.iloc[:,explode_idx])
    data.to_csv(f"{output_dir}/explode{COUNTER}.csv", index=False)
