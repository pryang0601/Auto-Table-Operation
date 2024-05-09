"""Module providing functions to transform tables"""
import pandas as pd
COUNTER = 0


def is_pivot(table_file: str) -> bool:
    """Check if it need pivot operation"""
    data = pd.read_csv(table_file)
    attrs = [data.columns[0]]
    attrs.extend(list(data.iloc[:, 0]))
    if len(attrs) > set(attrs):
        return True
    else:
        return False


def pivot(table_file: str, output_dir: str) -> None:
    """Perform pivot operation"""
    global COUNTER
    COUNTER += 1
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
    df_pivot.to_csv(f"{output_dir}/pivot{COUNTER}.csv", index=False)
