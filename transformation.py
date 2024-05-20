"""Module providing functions to transform tables"""
from stack import stack
from pivot import pivot
from transpose import transpose
from ffill import ffill
from subtitle import subtitle
from explode import explode
from wide_to_long import wide_to_long


def main(operation, table_file, output_dir, **kwargs):
    """transform dirty table base on the input operation"""
    operations_map = {
        "stack": stack,
        "pivot": pivot,
        "transpose": transpose,
        "ffill": ffill,
        "subtitle": subtitle,
        "explode": explode,
        "wide_to_long": wide_to_long
    }
    if operation not in operations_map:
        raise ValueError(f"Invalid operation: {operation}")
    if operation == "stack":
        try:
            start_idx = kwargs["start"]
            end_idx = kwargs["end"]
        except KeyError as e:
            raise KeyError("Missing required parameters for 'stack': 'start' and 'end'") from e
        operations_map[operation](start_idx, end_idx, table_file, output_dir)
    elif operation == "explode":
        try:
            explode_idx = kwargs["explode_index"]
        except KeyError as e:
            raise KeyError("Missing required parameter for 'explode': 'explode_idx'") from e
        operations_map[operation](table_file, output_dir, explode_idx)
    else:
        operations_map[operation](table_file, output_dir)
