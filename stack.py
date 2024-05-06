"""Module providing functions to transform tables"""
import pandas as pd
COUNTER = 0
def stack(start: int, end:int, table_file: str, output_dir: str)-> None:
    """Perform stack operation"""
    global COUNTER
    COUNTER+=1
    data = pd.read_csv(table_file)
    start_index = start
    end_index = end
    columns = data.columns
    data = data.melt(id_vars=columns[:start_index], value_vars=columns[start_index: end_index+1])
    data.to_csv(f"{output_dir}/stack{COUNTER}.csv", index= False)
