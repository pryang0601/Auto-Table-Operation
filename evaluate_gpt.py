from llm_check_gpt import *
from main import *
import time

# Assuming you have a function to evaluate the accuracy of a given permutation
def evaluate_gpt(folder_path: str, functions) -> float:

    """Iteratibe each subfolder to check operation to perform"""
    items = natsorted(os.listdir(folder_path))
    hit = 0
    total_file = 0
    for item in items:
        item_path = os.path.join(folder_path, item)
        file_path = Path(item_path)
        file_name = file_path.name
        candidate = []
        # print(f"file: {item_path}")
        # calculate candidate
        for func, operation in functions:

            if (func(item_path).startswith("(True")):
                candidate.append(operation)
                # print("!!!")

            if (len(candidate) == 2):
                break

        print(candidate)
        # calculate hit
        for op in candidate:
            if file_name.startswith(op):
                hit += 1
                break

        total_file += 1
    
    acc = hit / total_file
    return acc


def main():
    """Function to run the transformation operation"""
    dirpath = os.path.dirname(os.path.abspath(__file__))
    filepath = dirpath+'/Tables'

    # Find the permutation with the highest accuracy
    # best_permutation = None
    # highest_accuracy = 0
    # List of function references
    functions = [[is_pivot_gpt, "pivot"], 
                 [is_subtitle_gpt, "subtitle"],
                 [is_explode_gpt, "explode"], 
                 [is_ffill_gpt, "ffill"],
                 [is_wide_to_long_gpt, "wide_to_long"],
                 [is_stack_gpt, "stack"], 
                 [is_transpose_gpt, "transpose"]]

    # for perm in filtered_permutations:
    startTime = time.time()
    accuracy = evaluate_gpt(filepath, functions)
    endTime = time.time()
    print(f"permutation: {functions}, acc:{accuracy}, running_time:{endTime-startTime}")

    # Print the best permutation and its accuracy
    # print("Best permutation:", [func for func in best_permutation])
    # print("Highest accuracy:", highest_accuracy)

if __name__ == '__main__':
    main()