"""Module providing functions to transform tables"""
import pandas as pd
COUNTER = 0


def is_ffill(table_file: str) -> bool:
    """Check if it need ffill operation"""
    isnan = False
    data = pd.read_csv(table_file)
    for column in data.columns:
        # Check if the column contains any NaN values
        if data[column].isna().any():
            print(f"Column '{column}' contains NaN values.")
            isnan = True
            break
    return isnan


def ffill(table_file: str, output_dir: str) -> None:
    """Perform ffill operation"""
    global COUNTER
    COUNTER += 1
    data = pd.read_csv(table_file)
    data = data.ffill(axis=0)
    data.to_csv(f"{output_dir}/ffill{COUNTER}.csv", index=False)
