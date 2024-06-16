CREATE TRIGGER CheckPathBeforeInsert
ON file_info
INSTEAD OF INSERT
AS
BEGIN
    DECLARE @result NVARCHAR(MAX)
    DECLARE @path NVARCHAR(MAX) = (SELECT path FROM inserted)
    DECLARE @operation TABLE (
        path NVARCHAR(MAX),
        operation NVARCHAR(MAX),
        operation2 NVARCHAR(MAX),
        pattern NVARCHAR(MAX),
        pattern2 NVARCHAR(MAX),
        recommend_op_num INT,
        start_index INT,
        end_index INT,
        start_index2 INT,
        end_index2 INT
    )
    

    INSERT INTO @operation (path, operation, operation2, pattern, pattern2, recommend_op_num, start_index, end_index, start_index2, end_index2)
    EXEC sp_execute_external_script
        @language = N'Python',
        @script = N'
import pandas as pd
from typing import List
import re
import locale
from typing import Tuple
from collections import defaultdict

operation = ""
operation2 = ""
pattern = "None"
pattern2 = "None"
recommend_op_num = 0
start_index = -1
end_index = -1
start_index2 = -1
end_index2 = -1

table_file = InputDataSet.iloc[0]["path"]

def is_pivot(table_file: str) -> bool:
    """Check if it need pivot operation"""
    data = pd.read_csv(table_file)
    attrs = [data.columns[0]]
    # subtitle
    if data.iloc[0].iloc[1:].isna().all() and ":" not in attrs[0]:
       return False
    if len(data.columns)>2:
        return False
    attrs.extend(list(data.iloc[:, 0]))
    if ":" in attrs[0] and isinstance(attrs[0], str):
        attrs = [attr.split(":")[0] for attr in attrs]
    num_attrs = len(attrs)
    unique_num_attrs = len(set(attrs))
    if num_attrs > unique_num_attrs and (num_attrs%unique_num_attrs==0) and not data.iloc[:, 0].isna().any():
        return True
    else:
        return False

def is_ffill(table_file: str) -> bool:
    """Check if it need ffill operation"""
    isnan = False
    data = pd.read_csv(table_file)
    if data.iloc[-1].isnull().all():
        data.drop(data.tail(1).index, inplace=True)
    for column in data.columns:
        # Check if the column contains any NaN values
        if data[column].isna().any():
            isnan = True
            break
    return isnan

def is_subtitle(table_file: str) -> bool:
    """Check if it need subtitle operation"""
    data = pd.read_csv(table_file)
    first_row = data.iloc[0]
    is_title = first_row.iloc[1:].isna().all()
    return is_title

def is_explode(table_file: str) -> Tuple[bool, int]:
    def is_locale_number(value):
        """Check if the value is a number like 8,000"""
        try:
            # Try converting the string to a float
            number = locale.atof(value)
            # Conversion succeeded, so it''s a number
            return True
        except ValueError:
            # Conversion failed, not a valid number
            return False
        
    def is_composite(val: str):
        """Check if value is composite value"""
        date_pattern = re.compile(r"(\d{4}/\d{2}/\d{2})|(\d{2}/\d{2}/\d{4})")
        months = ["January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"]
        for month in months:
            if month in str(val):
                return False
        if date_pattern.match(str(val)):
            return False
        elif is_locale_number(str(val)) or "e.g" in str(val):
            return False    #E.g., 8,000
        else:
            return "," in str(val) or "/" in str(val) or "|" in str(val)
        
    """Check if it need explode operation"""
    data = pd.read_csv(table_file)
    for idx,col in enumerate(data.columns):
        if "," in col or "/" in col or "|" in col:
            continue
        if data[col].apply(is_composite).any():
            return True, idx
    return False, -1

def is_wide_to_long(table_file: str) -> Tuple[bool, list]:
    """Check if it need wide_to_long operation"""
    data = pd.read_csv(table_file)

    def find_patterns(schema_list, min_common_length=2):
        # Create a list of column names
        column_names = [col for col, dtype in schema_list]
        
        # Dictionary to store potential patterns and their counts
        pattern_dict = defaultdict(int)
        
        # Scan through each column name and find common patterns
        for col in column_names:
            # Split the column name into words
            words = re.findall(r"[A-Za-z]+|\d+", col)  # Split by words or numbers
            for i in range(len(words)):
                for j in range(i + 1, len(words) + 1):
                    # Join words to form patterns
                    pattern = " ".join(words[i:j])
                    if len(pattern) >= min_common_length:
                        pattern_dict[pattern] += 1
        
        # Filter out patterns that only occur once
        common_patterns = {pattern: count for pattern, count in pattern_dict.items() if count > 1}
        
        # Sort patterns by their counts in descending order
        sorted_patterns = sorted(common_patterns.items(), key=lambda item: item[1], reverse=True)
        
        return sorted_patterns

    def remove_redundant_patterns(patterns):
        # Sort patterns by count (descending) and then by pattern length (descending)
        patterns = sorted(patterns, key=lambda x: (-x[1], -len(x[0].split()), x[0]))
        
        # Use a set to keep track of patterns to be removed
        to_remove = set()
        
        # Identify redundant patterns
        for i, (pattern_i, count_i) in enumerate(patterns):
            for j, (pattern_j, count_j) in enumerate(patterns):
                if i != j and pattern_j not in to_remove and pattern_i not in to_remove and count_i == count_j:
                    # Check if pattern_j is a subset of pattern_i
                    if pattern_j in pattern_i:
                        to_remove.add(pattern_j)
        
        # Filter out the redundant patterns
        filtered_patterns = [pattern for pattern in patterns if pattern[0] not in to_remove]
        
        # Sort patterns by their counts in descending order
        filtered_patterns = sorted(filtered_patterns, key=lambda x: (x[1], x[0]), reverse = True)

        return filtered_patterns

    def select_most_common_patterns(patterns):
        # Initialize the variable most_common_count with the count of the first pattern in the list
        most_common_count = patterns[0][1]
        
        # Initialize the list most_common_patterns with the name of the first pattern
        most_common_patterns = [patterns[0][0]]
        
        # Iterate through the remaining patterns and their counts
        for pattern, count in patterns[1:]:
            # If the current pattern"s count is the same as most_common_count, add it to most_common_patterns
            if count == most_common_count:
                most_common_patterns.append(pattern)
            else:
                # If the current pattern"s count is different and most_common_patterns contains only one element
                if len(most_common_patterns) == 1:
                    # Update most_common_count to the current pattern"s count
                    most_common_count = count
                    # Reset most_common_patterns to only contain the current pattern
                    most_common_patterns = [pattern]
                else:
                    # If there is more than one most common pattern, exit the loop
                    break
        
        # Return the list most_common_patterns if it contains more than one pattern; otherwise, return an empty list
        return most_common_patterns if len(most_common_patterns) > 1 else []


    def filter_patterns_by_schema(schema_list, most_common_patterns):
        # Initialize an empty list to store the filtered patterns
        filtered_patterns = []

        # Get the number of patterns in the most_common_patterns list
        size = len(most_common_patterns)
        
        # Iterate over the most_common_patterns list using two indices to compare pairs of patterns
        for i in range(0, size):
            for j in range(i + 1, size):
                # Skip if the patterns at indices i and j are the same
                if most_common_patterns[i] == most_common_patterns[j]:
                    continue
                # Iterate through the schema_list to check if both patterns appear in the same schema pattern
                for schema_pattern, _ in schema_list:
                    if most_common_patterns[i] in schema_pattern and most_common_patterns[j] in schema_pattern:
                        # If pattern i is found in a schema pattern along with pattern j, and is not already in filtered_patterns, add it
                        if most_common_patterns[i] not in filtered_patterns:
                            filtered_patterns.append(most_common_patterns[i])
                        # Once a match is found for pattern i, break out of the inner loop
                        break
        
        # Return the original most_common_patterns if no patterns were filtered; otherwise, return the filtered patterns
        return most_common_patterns if len(filtered_patterns) == 0 else filtered_patterns


    def get_patterns(schema_list: list):
        # Find frequent patterns from the schema list
        frequent_patterns = find_patterns(schema_list)
        # Debug print statement to display frequent patterns (commented out)
        # print("【frequent_patterns】 : " + str(frequent_patterns))

        # Remove redundant patterns from the list of frequent patterns
        clean_patterns = remove_redundant_patterns(frequent_patterns)
        # Debug print statement to display clean patterns (commented out)
        # print("【clean_patterns】 : " + str(clean_patterns))

        # Check if there are any clean patterns
        if len(clean_patterns) > 0:
            # Select the most common patterns from the clean patterns
            most_common_patterns = select_most_common_patterns(clean_patterns)
            # Debug print statement to display most common patterns (commented out)
            # print("【most_common_patterns】 : " + str(most_common_patterns))

            # Filter the most common patterns by schema
            final_patterns = filter_patterns_by_schema(schema_list, most_common_patterns)
            # Print the final patterns
            # print("【final_patterns】 : " + str(final_patterns))
        else:
            # If no clean patterns, set final_patterns to clean_patterns (which would be an empty list)
            final_patterns = clean_patterns

        # Return the final patterns
        return final_patterns

    schema_list = [(col, dtype.name) for col, dtype in data.dtypes.items()]
    # print("【schema_list】 : " + str(schema_list))

    patterns = get_patterns(schema_list)

    if len(patterns) == 0:
        return (False, [])

    #start_idx, end_idx = find_longest_subsequence(schema_list, patterns)

    return (True, patterns)

def is_stack(table_file: str) -> list: # return [isstack, predicted_start_index, predicted_end_index]

    data = pd.read_csv(table_file)
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
                if current_type == "str" and any(hasNumber(str(val)) for val in col_values):
                    current_type = "int"
                    
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
    
    column_names = data.columns.values

    last_col, start_col = find_start_end_indices(data) 
    # print(f"{filepath} predicted: {start_col}, {last_col}")
    last_col, start_col = filter_by_numeric(column_names, last_col, start_col)
    # print(f"{filepath} predicted: {start_col}, {last_col}")

    if (last_col - start_col + 1) < 2:
        return [False]
    else:
        return [True, [start_col, last_col]]

def is_transpose(table_file: str) -> bool:
    """Check if it needs a transpose operation"""
    data = pd.read_csv(table_file)
    is_rowName_allStrings = all(isinstance(row, str) for row in data.iloc[:, 0])
    is_colName_allStrings = all(isinstance(col, str) or isinstance(col, int) or
                                isinstance(col, float) for col in data.columns)
    
    def check_rowItem_type(row):
        first_type = type(row.iloc[1])
        # print("first type", first_type)
        for col_idx in range(1, len(row)):
            # print(col_idx, " type: ", type(row.iloc[col_idx]))
            current_type = type(row.iloc[col_idx])
            if (isinstance(current_type, (int, float)) and isinstance(first_type, (int, float))):
                continue
            elif current_type != first_type:
                return False
        return True
    
    is_rowItem_same_type = data.iloc[1:].apply(check_rowItem_type, axis=1).all()
    return is_rowName_allStrings and is_colName_allStrings and is_rowItem_same_type

def check_operation(table_file: str) -> List:
    """Check what kind of operation we need to do"""
    operations_map = {
        "pivot": is_pivot,
        "ffill": is_ffill,
        "subtitle": is_subtitle,
        "explode": is_explode,
        "wide_to_long": is_wide_to_long,
        "stack": is_stack,
        "transpose": is_transpose
    }
    candidates = list(operations_map.keys())
    operations = []
    
    for candidate in candidates:
        
        res = operations_map[candidate](table_file)

        if candidate == "explode":
            if res[0]:
                operations.append([candidate, [res[1], -1, "None"]])
        elif candidate == "stack":
            if res[0]:
                print("stack!!!")
                operations.append([candidate, [res[1][0], res[1][1], "None"]])
        elif candidate == "wide_to_long":
            if res[0]:
                print("wide_to_long!!!")
                operations.append([candidate, [-1, -1, res[1]]])
        elif res:
            operations.append([candidate, [-1, -1, "None"]])

        if len(operations) == 2:
            break

    return operations




result = check_operation(table_file)

operation = result[0][0]
start_index = result[0][1][0]
end_index = result[0][1][1]
pattern = result[0][1][2]
if pattern != "None":
    delimiter = ", "
    pattern = delimiter.join(pattern)

print(operation, start_index, end_index, pattern)

if(len(result) == 2):
    operation2 = result[1][0]
    start_index2 = result[1][1][0]   
    end_index2 = result[1][1][1] 
    pattern2 = result[1][1][2]
    if pattern2 != "None":
        delimiter = ", "
        pattern2 = delimiter.join(pattern2)
    recommend_op_num = 2
else:
    recommend_op_num = 1
print(operation2, start_index2, end_index2, pattern2)

OutputDataSet = pd.DataFrame([(table_file, operation, operation2, pattern, pattern2,  recommend_op_num, start_index, end_index, start_index2, end_index2)],
                             columns=["path", "operation", "operation2", "pattern", "pattern2", "recommend_op_num", "start_index", "end_index", "start_index2", "end_index2"])
print(OutputDataSet)',
        @input_data_1 = N'SELECT @p as path',
        @params = N'@p NVARCHAR(MAX)',
        @p = @path;
        --WITH RESULT SETS ((operation NVARCHAR(MAX)));

    INSERT INTO file_info (path, operation, pattern, start_index, end_index)
        SELECT path, operation, pattern, start_index, end_index
        FROM @operation;

    IF (SELECT recommend_op_num FROM @operation) = 2
    BEGIN
        INSERT INTO file_info (path, operation, pattern, start_index, end_index)
        SELECT path, operation2, pattern2, start_index2, end_index2
        FROM @operation;
    END
END
