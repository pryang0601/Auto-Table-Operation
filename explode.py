"""Module providing functions to transform tables"""
import pandas as pd
import ast
COUNTER = 0


def explode(table_file: str, output_dir: str, explode_idx: int) -> None:
    """Perform subtitle operation"""
    global COUNTER
    COUNTER += 1
    data = pd.read_csv(table_file)
    data.iloc[:, explode_idx] = data.iloc[:, explode_idx].map(ast.literal_eval)
    data_explode = data.explode(data.columns[explode_idx])
    data_explode.to_csv(f"{output_dir}/explode{COUNTER}.csv", index=False)
