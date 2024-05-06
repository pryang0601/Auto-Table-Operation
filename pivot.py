"""Module providing functions to transform tables"""
import pandas as pd
COUNTER = 0
def pivot( table_file: str, output_dir: str)-> None:
    """Perform pivot operation"""
    global COUNTER
    COUNTER+=1
    df = pd.read_csv(table_file, header=None, names=["Attribute", "Value"])
    if ':' in df.iloc[[0]]["Attribute"].values[0]:
        for index, row in df.iterrows():
            attribute_value = row['Attribute']
            att = attribute_value.split(': ')[0]
            val = attribute_value.split(': ')[1]
            df.at[index, "Attribute"] = att
            df.at[index, "Value"] = val
    df_pivot = df.pivot(index=None, columns='Attribute', values='Value').apply(
                lambda x: pd.Series(x.dropna().to_numpy()))
    df_pivot.to_csv(f"{output_dir}/pivot{COUNTER}.csv", index= False)