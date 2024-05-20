import itertools
import time
from main import *

# Assuming you have a function to evaluate the accuracy of a given permutation
def evaluate_permutation(folder_path: str, permutation: list) -> float:
    """Iteratibe each subfolder to check operation to perform"""
    items = natsorted(os.listdir(folder_path))
    hit = 0
    total_file = 0
    for item in items:
        item_path = os.path.join(folder_path, item)
        file_path = Path(item_path)
        file_name = file_path.name
        candidate = []

        # calculate candidate
        for func, operation in permutation:
            if (operation == "stack" or operation == "wide_to_long"):
                if (func(item_path)[0]):
                    candidate.append(operation)

            elif (func(item_path)):
                candidate.append(operation)

            if (len(candidate) == 2):
                break
        
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

    # List of function references
    functions = [[is_pivot, "pivot"], 
                 [is_stack, "stack"], 
                 [is_wide_to_long, "wide_to_long"],
                 [is_subtitle, "subtitle"],
                 [is_explode, "explode"], 
                 [is_transpose, "transpose"],
                 [is_ffill, "ffill"]]

    # Generate all permutations of the functions
    permutations = list(itertools.permutations(functions))

    # Filter out permutations where 'wide_to_long' is ahead of 'stack'
    filtered_permutations = [perm for perm in permutations if perm.index([is_wide_to_long, 'wide_to_long']) < perm.index([is_stack, 'stack'])]

    # Filter out permutations where (subtitle, explode, ffill, pivot) is ahead of (wide_to_long, stack, transpose)
    filtered_permutations = [perm for perm in filtered_permutations
                         if (perm.index([is_subtitle, 'subtitle']) < perm.index([is_wide_to_long, 'wide_to_long']) and
                             perm.index([is_explode, 'explode']) < perm.index([is_wide_to_long, 'wide_to_long']) and
                             perm.index([is_ffill, 'ffill']) < perm.index([is_wide_to_long, 'wide_to_long']) and
                             perm.index([is_pivot, 'pivot']) < perm.index([is_wide_to_long, 'wide_to_long']) and
                             perm.index([is_subtitle, 'subtitle']) < perm.index([is_stack, 'stack']) and
                             perm.index([is_explode, 'explode']) < perm.index([is_stack, 'stack']) and
                             perm.index([is_ffill, 'ffill']) < perm.index([is_stack, 'stack']) and
                             perm.index([is_pivot, 'pivot']) < perm.index([is_stack, 'stack']) and
                             perm.index([is_subtitle, 'subtitle']) < perm.index([is_transpose, 'transpose']) and
                             perm.index([is_explode, 'explode']) < perm.index([is_transpose, 'transpose']) and
                             perm.index([is_ffill, 'ffill']) < perm.index([is_transpose, 'transpose']) and
                             perm.index([is_pivot, 'pivot']) < perm.index([is_transpose, 'transpose'])
                            )]

    # Find the permutation with the highest accuracy
    best_permutation = None
    highest_accuracy = 0

    count = 0
    for perm in filtered_permutations:
        startTime = time.time()
        accuracy = evaluate_permutation(filepath, perm)
        endTime = time.time()
        print(f"{count}:    permutation: {perm}, acc:{accuracy}, running_time:{endTime-startTime}")
        if accuracy > highest_accuracy:
            highest_accuracy = accuracy
            best_permutation = perm

        count += 1

    # Print the best permutation and its accuracy
    print("Best permutation:", [func for func in best_permutation])
    print("Highest accuracy:", highest_accuracy)

if __name__ == '__main__':
    main()