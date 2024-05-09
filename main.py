"""Module get the filepath"""
import os
import json
from natsort import natsorted
from stack import stack
from pivot import pivot, is_pivot
from transpose import transpose
from ffill import ffill, is_ffill
from subtitle import subtitle, is_subtitle
from explode import explode, is_explode
CURRENT_DATA = ""


def is_json_file(file_path: str) -> bool:
    """Check whether the file is a json file"""
    if file_path.endswith('.json'):
        try:
            with open(file_path, 'r', encoding="utf-8") as file:
                json.load(file)
            return True
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    return False


def perform_stack(start: str, end: str,
                  table_file: str, output_dir: str) -> None:
    """Perform stack operation"""
    stack(start=start, end=end, table_file=table_file, output_dir=output_dir)


def perform_pivot(table_file: str, output_dir: str) -> None:
    """Perform pivot operation"""
    pivot(table_file=table_file, output_dir=output_dir)


def perform_transpose(table_file: str, output_dir: str) -> None:
    """Perform transpose operation"""
    transpose(table_file=table_file, output_dir=output_dir)


def perform_ffill(table_file: str, output_dir: str) -> None:
    """Perform ffill operation"""
    ffill(table_file=table_file, output_dir=output_dir)


def perform_subtitle(table_file: str, output_dir: str) -> None:
    """Perform subtitle operation"""
    subtitle(table_file=table_file, output_dir=output_dir)


def perform_explode(table_file: str, output_dir: str,
                    explode_idx: int) -> None:
    """Perform explode operation"""
    explode(table_file=table_file, output_dir=output_dir,
            explode_idx=explode_idx)


def process_folder(folder_path: str, file_output: str, operation: str) -> None:
    """Iteratibe each subfolder to perform stack"""
    global CURRENT_DATA
    items = natsorted(os.listdir(folder_path))
    # natsorted: 1,2,3,4,5...
    for item in items:
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            process_folder(item_path, file_output, operation)
        else:
            if os.path.basename(item_path) == 'data.csv':
                CURRENT_DATA = item_path
            if is_json_file(item_path):
                if operation == 'stack':
                    with open(item_path, 'r', encoding="utf-8") as j:
                        contents = json.loads(j.read())
                    label = contents['label'][0]
                    stack_start_idx = label['stack_start_idx']
                    stack_end_idx = label['stack_end_idx']
                    print(f"stack_start_idx: {stack_start_idx}, stack_end_idx: {stack_end_idx}")
                    perform_stack(start=stack_start_idx, end=stack_end_idx,
                                  table_file=CURRENT_DATA, output_dir=file_output)
                elif operation == 'pivot':
                    perform_pivot(table_file=CURRENT_DATA, output_dir=file_output)
                elif operation == 'transpose':
                    perform_transpose(table_file=CURRENT_DATA, output_dir=file_output)
                elif operation == 'ffill':
                    perform_ffill(table_file=CURRENT_DATA, output_dir=file_output)
                elif operation == 'subtitle':
                    perform_subtitle(table_file=CURRENT_DATA, output_dir=file_output)
                elif operation == 'explode':
                    with open(item_path, 'r', encoding="utf-8") as j:
                        contents = json.loads(j.read())
                    label = contents['label'][0]
                    explode_idx = label['explode_column_idx']
                    print(f"explode_column_idx: {explode_idx}")
                    perform_explode(table_file=CURRENT_DATA, output_dir=file_output, explode_idx=explode_idx)
                else:
                    pass


def check_operation(table_file: str) -> str:
    """Check what kind of operation we need to do"""
    # The order is matter!
    if is_explode(table_file):
        return "explode"
    elif is_subtitle(table_file):
        return subtitle
    elif is_pivot(table_file):
        return "pivot"
    elif is_ffill(table_file):
        return "ffill"


def run():
    """Function to run the stack operation"""
    dirpath = os.path.dirname(os.path.abspath(__file__))
    stackpath = dirpath+'/Auto-Tables-Benchmark/ATBench/stack'
    pivotpath = dirpath+'/Auto-Tables-Benchmark/ATBench/pivot'
    transpath = dirpath+'/Auto-Tables-Benchmark/ATBench/transpose'
    ffillpath = dirpath+'/Auto-Tables-Benchmark/ATBench/ffill'
    subtitlepath = dirpath+'/Auto-Tables-Benchmark/ATBench/subtitle'
    explodepath = dirpath+'/Auto-Tables-Benchmark/ATBench/explode'
    output = dirpath+'/Output'
    # operation = check_operation(table_path)
    process_folder(folder_path=subtitlepath, file_output=output, operation="subtitle")


if __name__ == '__main__':
    run()
