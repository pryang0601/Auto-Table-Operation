"""Module providing functions to transform tables"""
import pandas as pd
COUNTER = 0
def transpose( table_file: str, output_dir: str)-> None:
    """Perform transpose operation"""
    global COUNTER
    COUNTER+=1
    df = pd.read_csv(table_file, header= None)
    index = df.columns.values[0]
    df_t = df.set_index(index).T
    df_t.to_csv(f"{output_dir}/transpose{COUNTER}.csv", index= False)
