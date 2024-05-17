"""Module providing functions to transform tables"""
import pandas as pd
from collections import defaultdict
import re
COUNTER = 0

def find_patterns(schema_list, min_common_length=2):
    # Create a list of column names
    column_names = [col for col, dtype in schema_list]
    
    # Dictionary to store potential patterns and their counts
    pattern_dict = defaultdict(int)
    
    # Scan through each column name and find common patterns
    for col in column_names:
        # Split the column name into words
        words = re.findall(r'[A-Za-z]+|\d+', col)  # Split by words or numbers
        for i in range(len(words)):
            for j in range(i + 1, len(words) + 1):
                # Join words to form patterns
                pattern = ' '.join(words[i:j])
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
        # If the current pattern's count is the same as most_common_count, add it to most_common_patterns
        if count == most_common_count:
            most_common_patterns.append(pattern)
        else:
            # If the current pattern's count is different and most_common_patterns contains only one element
            if len(most_common_patterns) == 1:
                # Update most_common_count to the current pattern's count
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


def get_patterns(schema_list: list) -> bool:
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
        print("【final_patterns】 : " + str(final_patterns))
    else:
        # If no clean patterns, set final_patterns to clean_patterns (which would be an empty list)
        final_patterns = clean_patterns

    # Return the final patterns
    return final_patterns


def find_longest_subsequence(schema_list, final_patterns):
    # Extract schema names from the schema_list
    schema_name = [name for name, _ in schema_list]
    schema_name_size = len(schema_name)

    # Initialize variables to track the start and end indices of the current subsequence
    start_idx, end_idx = -1, -1
    # Initialize variables to track the maximum length of the subsequence and its start and end indices
    max_len, final_start_idx, final_end_idx = 0, -1, -1

    # Iterate through each schema name
    for i in range(schema_name_size):
        check = False
        name = schema_name[i]
        # Check if any pattern in final_patterns matches the current schema name
        for pat in final_patterns:
            if re.search(pat, name):
                check = True
                break
        if check:
            # If a pattern matches, update the start and end indices
            if start_idx == -1:
                start_idx, end_idx = i, i
            else:
                end_idx = i
            
            # Update the maximum length and final start and end indices if the current subsequence is longer
            if max(end_idx - start_idx + 1, max_len):
                max_len = end_idx - start_idx + 1
                final_start_idx = start_idx
                final_end_idx = end_idx
        else:
            # Reset the start and end indices if no pattern matches
            start_idx, end_idx = -1, -1

    # Return the start and end indices of the longest subsequence
    return start_idx, end_idx



def is_wide_to_long(table_file: str) -> bool:
    """Check if it need wide_to_long operation"""
    data = pd.read_csv(table_file)

    schema_list = [(col, dtype.name) for col, dtype in data.dtypes.items()]
    # print("【schema_list】 : " + str(schema_list))

    patterns = get_patterns(schema_list)

    if len(patterns) == 0:
        return (False, [])

    start_idx, end_idx = find_longest_subsequence(schema_list, patterns)

    return (True, [start_idx, end_idx])

def wide_to_long(table_file: str, output_dir: str) -> None:
    """Perform wide-to-long operation"""
    global COUNTER

    COUNTER += 1

    df = pd.read_csv(table_file, header=None)

    index = df.columns.values[0]

    df_t = df.set_index(index).T
    
    df_t.to_csv(f"{output_dir}/transpose{COUNTER}.csv", index=False)
