"""Module providing functions to transform tables"""
import pandas as pd
from pathlib import Path


def is_pivot(table_file: str) -> bool:
    """Check if it need pivot operation"""
    data = pd.read_csv(table_file)
    attrs = [data.columns[0]]
    # subtitle
    if data.iloc[0].iloc[1:].isna().all() and ':' not in attrs[0]:
       return False
    if len(data.columns)>2:
        return False
    attrs.extend(list(data.iloc[:, 0]))
    if ':' in attrs[0] and isinstance(attrs[0], str):
        attrs = [attr.split(':')[0] for attr in attrs]
    # contains replicate values and doesn't contain Nan
    num_attrs = len(attrs)
    unique_num_attrs = len(set(attrs))
    if num_attrs > unique_num_attrs and (num_attrs%unique_num_attrs==0) and not data.iloc[:, 0].isna().any():
        return True
    else:
        return False


def pivot(table_file: str, output_dir: str) -> None:
    """Perform pivot operation"""
    file_path = Path(table_file)
    file_name = file_path.name
    df = pd.read_csv(table_file, header=None, names=["Attribute", "Value"])
    if ':' in df.iloc[[0]]["Attribute"].values[0]:
        for index, row in df.iterrows():
            attribute_value = row['Attribute']
            att = attribute_value.split(': ')[0]
            val = attribute_value.split(': ')[1]
            df.at[index, "Attribute"] = att
            df.at[index, "Value"] = val
    # df_pivot = df.pivot(index=None, columns='Attribute', values='Value')
    # pandas == 1.5.3
    df_pivot = df.pivot(index=None, columns='Attribute', values='Value').apply(
                lambda x: pd.Series(x.dropna().to_numpy()))
    df_pivot.to_csv(f"{output_dir}/{file_name}", index=False)
