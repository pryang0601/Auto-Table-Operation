"""Module providing functions to transform tables"""
import pandas as pd
COUNTER = 0


def is_transpose(table_file: str) -> bool:
    """Check if it need transpose operation"""
    df = pd.read_csv(table_file)
    is_rowName_allStrings = all(isinstance(row, str) for row in df.iloc[:, 0])
    is_colName_allStrings = all(isinstance(col, str) or isinstance(col, int) or
                                isinstance(col, float) for col in df.columns)
    def check_rowItem_type(row):
        first_type = type(row.iloc[1])
        # print("first type",first_type)
        for col_idx in range(1, len(row)):
            # print(col_idx," type: ",type(row.iloc[col_idx]))
            current_type = type(row.iloc[col_idx])
            if type(current_type) != first_type:
                if (isinstance(current_type, int) or isinstance(current_type, float)) and \
                (isinstance(first_type, int) or isinstance(first_type, float)):
                    continue
            else:
                return False
        return True
        
    is_rowItem_same_type = df.iloc[1:].apply(check_rowItem_type, axis=1).all()
    # print(is_rowName_allStrings, is_colName_allStrings, is_rowItem_same_type)
    return is_rowName_allStrings and is_colName_allStrings and is_rowItem_same_type


def transpose(table_file: str, output_dir: str) -> None:
    """Perform transpose operation"""
    global COUNTER
    COUNTER += 1
    df = pd.read_csv(table_file, header=None)
    index = df.columns.values[0]
    df_t = df.set_index(index).T
    df_t.to_csv(f"{output_dir}/transpose{COUNTER}.csv", index=False)
