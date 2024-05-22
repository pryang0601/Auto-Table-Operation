from pathlib import Path
import os
from database import insert_file, get_file, insert_data
from main import check_operation
from stack import stack
from pivot import pivot
from transpose import transpose
from ffill import ffill
from subtitle import subtitle
from explode import explode
from wide_to_long import wide_to_long

insert_file("/home/pry/Document/table/Auto-Table-Operation/Tables/transpose2.csv")
item = get_file()
table_idx = item[0]
table_file = item[1]
# get predicted operation
operations = check_operation(table_file)
for idx, operation in enumerate(operations):
    if isinstance(operation, list):
        print(f"The {idx+1} option: {operation[0]}")
    else:
        print(f"The {idx+1} option: {operation}")
# get user's choice
action_idx = int(input())
action_op = operations[action_idx-1]
file_path = Path(table_file)
file_name = file_path.name
dirpath = os.path.dirname(os.path.abspath(__file__))
output_dir = dirpath+"/Output"
output_table = f"{output_dir}/{file_name}"
# transform dirty table and insert data into mysql
if action_op[0] == "stack":
    start = operations[action_idx-1][1][0]
    end = operations[action_idx-1][1][1]
    stack(start=start, end=end, table_file=table_file, output_dir=output_dir)
    insert_data(table_idx, "stack", start, end, output=output_table)
elif action_op[0] == "wide_to_long":
    start = operations[action_idx-1][1][0]
    end = operations[action_idx-1][1][1]
    pattern = operations[action_idx-1][1][2]
    wide_to_long(table_file, start, end, pattern, output_dir)
    insert_data(table_idx, "wide_to_long", start, end, output=output_table)
elif action_op == "pivot":
    pivot(table_file=table_file, output_dir=output_dir)
    insert_data(table_idx, "pivot", None, None, output=output_table)
elif action_op == "transpose":
    transpose(table_file, output_dir)
    insert_data(table_idx, "transpose", None, None, output=output_table)
elif action_op == "ffill":
    ffill(table_file=table_file, output_dir=output_dir)
    insert_data(table_idx, "ffill", None, None, output=output_table)
elif action_op == "subtitle":
    subtitle(table_file, output_dir)
    insert_data(table_idx, "subtitle", None, None, output=output_table)
elif action_op[0] == "explode":
    explode_idx = operations[action_idx-1][1][0]
    explode(table_file=table_file, output_dir=output_dir,
            explode_idx=explode_idx)
    insert_data(table_idx, "explode", explode_idx, None, output=output_table)
