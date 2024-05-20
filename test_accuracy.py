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
perms = list(permutations(["stack", "pivot", "transpose", "ffill", "subtitle", "explode", "wide_to_long"]))
candidates = [
    item for item in list(perms)
    if item.index("transpose") == 6 and item.index("stack") >= item.index("wide_to_long")
]
print(len(candidates))
accuracy = []
def extract_prefix(filename):
    """get the operation according to the filename"""
    pattern = r'^([a-zA-Z]+)\d+\.csv$'
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
                if operations_map[c](item_path):
                    operations.append(c)
                if len(operations)==2:
                    break
            if ground_truth in operations:
                hit+=1
        res = {"Permutation": candidate, "Accuracy": hit/files_num}
        print(res)
        accuracy.append(res)

dirpath = os.path.dirname(os.path.abspath(__file__))
filepath = dirpath+'/Tables'
check_accuracy(filepath)
print("Accuracy: ", accuracy)
max_accuracy = max(accuracy, key=lambda x:x["Accuracy"])
print("Max Accuracy: ", max_accuracy)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")
