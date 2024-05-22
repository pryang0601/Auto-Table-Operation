"""Module get the filepath"""
import os
from pathlib import Path
from itertools import permutations
from natsort import natsorted
import re
import time
from stack import is_stack
from pivot import is_pivot
from transpose import is_transpose
from ffill import is_ffill
from subtitle import is_subtitle
from explode import is_explode
from wide_to_long import is_wide_to_long
start_time = time.time()
first_four_ops = ["pivot", "ffill", "subtitle", "explode"]
last_three_ops = ["wide_to_long", "stack", "transpose"]
first_permutations = list(permutations(first_four_ops))
last_permutations = list(permutations(last_three_ops))
# Combine the two sets of permutations
candidates = [
    first + last
    for first in first_permutations
    for last in last_permutations
    if last.index("stack") > last.index("wide_to_long")
]
print(len(candidates))
accuracy = []
def extract_prefix(filename):
    """get the operation according to the filename"""
    pattern = r'^([a-zA-Z_]+)\d+\.csv$'
    match = re.match(pattern, filename)
    if match:
        return match.group(1)
    return None


def check_accuracy(folder_path: str) -> None:
    """Check what kind of operation we need to do"""
    operations_map = {
        "stack": is_stack,
        "pivot": is_pivot,
        "transpose": is_transpose,
        "ffill": is_ffill,
        "subtitle": is_subtitle,
        "explode": is_explode,
        "wide_to_long": is_wide_to_long
    }
    items = natsorted(os.listdir(folder_path))
    files_num = len(items)
    for candidate in candidates:
        hit = 0
        for item in items:
            item_path = os.path.join(folder_path, item)
            file_path = Path(item_path)
            file_name = file_path.name
            ground_truth = extract_prefix(file_name)
            operations = []
            for c in candidate:
                if c == "stack" or c == "wide_to_long" or candidate == "explode":
                    if operations_map[c](item_path)[0]:
                        operations.append(c)
                else:
                    if operations_map[c](item_path):
                        operations.append(c)
                if len(operations) == 2:
                    break
            if ground_truth in operations:
                hit+=1
        res = {"Permutation": candidate, "Accuracy": hit/files_num}
        print(res)
        accuracy.append(res)

dirpath = os.path.dirname(os.path.abspath(__file__))
filepath = dirpath+'/Tables'
check_accuracy(filepath)
max_accuracy = max(accuracy, key=lambda x:x["Accuracy"])
print("Max Accuracy: ", max_accuracy)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")
