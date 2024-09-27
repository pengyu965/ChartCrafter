import json
import math


def distribute_counts(orig_counts, fraction):
    # Check if the input is a dictionary
    if isinstance(orig_counts, dict):
        # If it is, apply the function recursively to each value in the dictionary
        return {k: distribute_counts(v, fraction) for k, v in orig_counts.items()}
    # If it is not a dictionary, it is an integer, so multiply by 0.125
    # And round to the nearest integer
    return math.ceil(orig_counts * fraction)


def get_test_validation_counts(edits_required, distribution=(0.8, 0.1, 0.1, 0.01)):
    train_counts = distribute_counts(edits_required, distribution[0])
    validation_counts = distribute_counts(edits_required, distribution[1])
    test_counts = distribute_counts(edits_required, distribution[2])
    test_small_counts = distribute_counts(edits_required, distribution[3])

    return train_counts, validation_counts, test_counts, test_small_counts


if __name__ == "__main__":
    edits_required = json.load(open('./chartcrafter/edits_required_total.json', "r"))
    train_counts, validation_counts, test_counts, test_small_counts = get_test_validation_counts(edits_required)
    for set_name, set_counts in (("train", train_counts), ("val", validation_counts), ("test", test_counts), ("test_small", test_small_counts)):
        with open(f"./chartcrafter/edits_required_{set_name}.json", "w") as f:
            json.dump(set_counts, f, indent=2)
