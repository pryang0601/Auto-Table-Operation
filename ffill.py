"""Module providing functions to transform tables"""
import pandas as pd
from pathlib import Path


def is_ffill(table_file: str) -> bool:
    """Check if it need ffill operation"""
    isnan = False
    data = pd.read_csv(table_file)
    if data.iloc[-1].isnull().all():
        data.drop(data.tail(1).index, inplace=True)
    for column in data.columns:
        # Check if the column contains any NaN values
        if data[column].isna().any():
            isnan = True
            break
    return isnan


def ffill(table_file: str, output_dir: str) -> None:
    """Perform ffill operation"""
    data = pd.read_csv(table_file)
    file_path = Path(table_file)
    file_name = file_path.name
    except_col = ['price', 'description', 'release']
    cols_ffill = [idx for idx,col in enumerate(data.columns) if col.lower() not in except_col]
    data.iloc[:,cols_ffill] = data.iloc[:,cols_ffill].ffill()
    data.to_csv(f"{output_dir}/{file_name}", index=False)
