"""Module providing functions to transform tables"""
import pandas as pd
COUNTER = 0
def ffill(table_file: str, output_dir: str)-> None:
    """Perform ffill operation"""
    global COUNTER
    COUNTER+=1
    data = pd.read_csv(table_file)
    print(data)
    data = data.ffill(axis=0)
    data.to_csv(f"{output_dir}/ffill{COUNTER}.csv", index= False)