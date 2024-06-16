--DROP PROCEDURE transform
CREATE PROCEDURE transform
    @input_id INT
AS
BEGIN
    DECLARE @path NVARCHAR(MAX)
    DECLARE @operation NVARCHAR(MAX)
    DECLARE @pattern NVARCHAR(MAX)
    DECLARE @start_index INT
    DECLARE @end_index INT

    DECLARE @transform_table TABLE (new_path NVARCHAR(MAX))
    
    SELECT 
        @path = path, 
        @operation = operation, 
        @pattern = pattern, 
        @start_index = start_index, 
        @end_index = end_index 
    FROM 
        file_info 
    WHERE 
        id = @input_id

    IF @path IS NULL
    BEGIN
        RAISERROR('The path does not exist in the file_info table.', 16, 1)
        RETURN
    END

    DECLARE @script NVARCHAR(MAX)
    SET @script = N'
import pandas as pd
import numpy as np
from pathlib import Path
import os

path = InputDataSet.iloc[0]["path"]
operation = InputDataSet.iloc[0]["operation"]
pattern = InputDataSet.iloc[0]["pattern"]
start_index = InputDataSet.iloc[0]["start_index"]
end_index = InputDataSet.iloc[0]["end_index"]

def wide_to_long(table_file: str, pat: list, output_file_name: str) -> None:
    """Perform wide-to-long operation"""

    df = pd.read_csv(table_file)

    df["id"] = df.index

    next_char = ""

    for col in df.columns.values:
        index = col.find(pat[0])
        if index != -1:
            if index + len(pat[0]) < len(col):
                next_char = col[index + len(pat[0])]
            break
    
    df = pd.wide_to_long(df, stubnames = pat, i = "id", j = "new_attribute", sep = next_char)
    
    df.to_csv(f"{output_file_name}", index=True)

def stack(start: int, end: int, table_file: str, output_file_name: str) -> None:
    """Perform stack operation"""
    data = pd.read_csv(table_file)
    file_path = Path(table_file)
    file_name = file_path.name
    start_index = start
    end_index = end
    columns = data.columns
    data = data.melt(id_vars=columns[:start_index],
                     value_vars=columns[start_index: end_index+1])
    data.to_csv(f"{output_file_name}", index=False)

def pivot(table_file: str, output_file_name: str) -> None:
    """Perform pivot operation"""
    file_path = Path(table_file)
    file_name = file_path.name
    df = pd.read_csv(table_file, header=None, names=["Attribute", "Value"])
    if ":" in df.iloc[[0]]["Attribute"].values[0]:
        for index, row in df.iterrows():
            attribute_value = row["Attribute"]
            att = attribute_value.split(": ")[0]
            val = attribute_value.split(": ")[1]
            df.at[index, "Attribute"] = att
            df.at[index, "Value"] = val
    # df_pivot = df.pivot(index=None, columns="Attribute", values="Value")
    # pandas == 1.5.3
    df_pivot = df.pivot(index=None, columns="Attribute", values="Value").apply(
                lambda x: pd.Series(x.dropna().to_numpy()))
    df_pivot.to_csv(f"{output_file_name}", index=False)

def subtitle(table_file: str, output_file_name: str) -> None:
    """Perform subtitle operation"""
    file_path = Path(table_file)
    file_name = file_path.name
    data = pd.read_csv(table_file)
    columns = data.columns
    # drop empty columns
    empty_columns = data.columns[data.isnull().all()]
    if not empty_columns.empty:
        data.drop(empty_columns, axis=1, inplace=True)
    # get subtitles
    mask = data.iloc[:, 1:].isna().all(axis=1)
    subtitles = data[columns[0]][mask]
    indexes = list(subtitles.index)
    subtitles = list(subtitles)
    data.insert(0, "Subtitle", np.NAN)
    for idx, index in enumerate(indexes):
        data.iloc[index, 0] = subtitles[idx]
    data.fillna(method="ffill", inplace=True)
    data.drop(axis=0, index=indexes, inplace=True)
    data.to_csv(f"{output_file_name}", index=False)

def transpose(table_file: str, output_file_name: str) -> None:
    """Perform transpose operation"""
    file_path = Path(table_file)
    file_name = file_path.name
    df = pd.read_csv(table_file, header=None)
    index = df.columns.values[0]
    df_t = df.set_index(index).T
    df_t.to_csv(f"{output_file_name}", index=False)

def ffill(table_file: str, output_file_name: str) -> None:
    """Perform ffill operation"""
    data = pd.read_csv(table_file)
    file_path = Path(table_file)
    file_name = file_path.name
    except_col = ["price", "description", "release"]
    cols_ffill = [idx for idx,col in enumerate(data.columns) if col.lower() not in except_col]
    data.iloc[:,cols_ffill] = data.iloc[:,cols_ffill].ffill()
    data.to_csv(f"{output_file_name}", index=False)

def explode(table_file: str, output_file_name: str, explode_idx: int) -> None:
    """Perform subtitle operation"""

    def parse_string_to_list(s: str) -> list:
        """Check if the string contains commas or slashes"""
        if not isinstance(s, str):
            return s
        if pd.isna(s):
            return s
        if "," in s:
            return [x.strip() for x in s.split(",")]
        elif "/" in s:
            return [x.strip() for x in s.split("/")]
        else:
            return [s]

    data = pd.read_csv(table_file)
    file_path = Path(table_file)
    file_name = file_path.name
    data.iloc[:, explode_idx] = data.iloc[:, explode_idx].map(parse_string_to_list)
    data = data.explode(data.columns[explode_idx])
    data.to_csv(f"{output_file_name}", index=False)

def transform_file_path(file_path):
    # Extract the directory and the file name
    directory, file_name = os.path.split(file_path)
    
    # Split the file name into name and extension
    name, ext = os.path.splitext(file_name)
    
    # Create the new file name by adding "transformed_" prefix
    new_file_name = f"transformed_{name}{ext}"
    
    # Combine the directory and the new file name to get the new file path
    new_file_path = os.path.join(directory, new_file_name)
    
    return new_file_path

new_path = transform_file_path(path)
pattern = pattern.split(", ")

fun_map = {
    "wide_to_long" : wide_to_long,
    "stack" : stack,
    "pivot" : pivot,
    "subtitle" : subtitle,
    "transpose" : transpose,
    "ffill" : ffill,
    "explode" : explode
}

if operation == "wide_to_long":
    wide_to_long(path, pattern, new_path)
elif operation == "stack":
    stack(start_index, end_index, path, new_path)
elif operation == "explode":
    explode(path, new_path, start_index)
else:
    fun_map[operation](path, new_path)



OutputDataSet = pd.DataFrame([(new_path)], columns=["new_path"])
'
    INSERT INTO @transform_table (new_path)
    EXEC sp_execute_external_script
        @language = N'Python',
        @script = @script,
        @input_data_1 = N'SELECT @path_ AS path, @operation_ AS operation, @pattern_ AS pattern, @start_index_ AS start_index, @end_index_ AS end_index',
        @params = N'@path_ NVARCHAR(MAX), @operation_ NVARCHAR(MAX), @pattern_ NVARCHAR(MAX), @start_index_ INT, @end_index_ INT',
        @path_ = @path,
        @operation_ = @operation,
        @pattern_ = @pattern,
        @start_index_ = @start_index,
        @end_index_ = @end_index

    UPDATE file_info
    SET transformed_new_path = (SELECT new_path FROM @transform_table)
    WHERE id = @input_id
END