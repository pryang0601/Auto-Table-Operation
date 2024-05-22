"""Module providing functions to transform tables"""
import pandas as pd
import numpy as np
from pathlib import Path


def is_subtitle(table_file: str) -> bool:
    """Check if it need subtitle operation"""
    data = pd.read_csv(table_file)
    first_row = data.iloc[0]
    is_title = first_row.iloc[1:].isna().all()
    return is_title


def subtitle(table_file: str, output_dir: str) -> None:
    """Perform subtitle operation"""
    file_path = Path(table_file)
    file_name = file_path.name
    data = pd.read_csv(table_file)
    columns = data.columns
    # drop empty columns
    empty_columns = data.columns[data.isnull().all()]
    if not empty_columns.empty:
        data.drop(empty_columns, axis=1, inplace=True)
    # get subtitles
    mask = data.iloc[:, 1:].isna().all(axis=1)
    subtitles = data[columns[0]][mask]
    indexes = list(subtitles.index)
    subtitles = list(subtitles)
    data.insert(0, "Subtitle", np.NAN)
    for idx, index in enumerate(indexes):
        data.iloc[index, 0] = subtitles[idx]
    data.fillna(method="ffill", inplace=True)
    data.drop(axis=0, index=indexes, inplace=True)
    data.to_csv(f"{output_dir}/{file_name}", index=False)
