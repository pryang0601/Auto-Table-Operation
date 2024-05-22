"""Module providing functions to transform tables"""
import pandas as pd
import os
from difflib import SequenceMatcher
import re
from pathlib import Path

def similar(a, b):
    """Compute similarity between two strings using SequenceMatcher."""
    return SequenceMatcher(None, a, b).ratio()


def find_start_end_indices(data):

    num_cols = len(data.columns)

    def hasNumber(stringVal):
        return any(elem.isdigit() for elem in stringVal)
    
    def check_homogeneity(start_col):

        base_type = None
        for col in range(start_col, num_cols): # 0, 1, 2, 3 ,4
            # Check the type of each value in the column
            col_values = data.iloc[:, col].dropna()
            col_type = col_values.apply(lambda x: type(x).__name__).unique()
            if (col_type.size == 0):
                continue
            if len(col_type) != 1:
                break
            current_type = col_type[0]

            # Check if the column should be considered as int due to mixed types
            if current_type == 'str' and any(hasNumber(str(val)) for val in col_values):
                current_type = 'int'
                
            if base_type is None:
                base_type = current_type
            if current_type != base_type:
                return col
                break
            
        return col  # return the next start_point

    start_col = 0
    while(True):
        last_col = check_homogeneity(start_col)
        # print(last_col)
        if (last_col == num_cols - 1):
            break
        else:
            start_col = last_col # 2
    
    return last_col, start_col

def filter_by_similarity(column_names, last_col, start_col, fasttext_model):

    # Cosine similarity between column_names
    for i in range(len(column_names)-1):
        # similarity_score = cosine_similarity(lsa_result[i].reshape(1, -1), lsa_result[i+1].reshape(1, -1))
        try:
            similarity_score = similar(column_names[i], column_names[i+1])
            print(f"similarity score of {column_names[i]} and {column_names[i+1]}", similarity_score)
        except KeyError as e:
            print(f"Warning: {e} not found in the model. Assigning default similarity score.")


def filter_by_numeric(column_names, last_col, start_col):

    cur = start_col
    while cur <= last_col and not any(char.isdigit() for char in column_names[cur]):
        cur += 1
    
    if (cur <= last_col):
        start_col = cur

    cur = last_col
    while cur >= start_col and not any(char.isdigit() for char in column_names[cur]):
        cur -= 1
    
    if (cur >= start_col):
        last_col = cur


    return last_col, start_col
    
    

def is_stack(table_file: str) -> list: # return [isstack, predicted_start_index, predicted_end_index]
    data = pd.read_csv(table_file)
    filepath = table_file.split("/")[-2]

    column_names = data.columns.values

    last_col, start_col = find_start_end_indices(data) 
    # print(f"{filepath} predicted: {start_col}, {last_col}")
    last_col, start_col = filter_by_numeric(column_names, last_col, start_col)
    # print(f"{filepath} predicted: {start_col}, {last_col}")


    if (last_col - start_col + 1) < 2:
        return [False]
    else:
        return [True, [start_col, last_col]]



def stack(start: int, end: int, table_file: str, output_dir: str) -> None:
    """Perform stack operation"""
    data = pd.read_csv(table_file)
    file_path = Path(table_file)
    file_name = file_path.name
    start_index = start
    end_index = end
    columns = data.columns
    data = data.melt(id_vars=columns[:start_index],
                     value_vars=columns[start_index: end_index+1])
    data.to_csv(f"{output_dir}/{file_name}", index=False)


