"""
Prototype problem bank. One problem, fixed test cases.
In production this becomes a DB-backed problem store.
Each problem defines the function the candidate must implement,
plus test cases the executor runs as GROUND TRUTH for correctness.
"""

PROBLEMS = {
    "two-sum": {
        "id": "two-sum",
        "title": "Two Sum",
        "function_name": "two_sum",
        "description": (
            "Given a list of integers `nums` and an integer `target`, return the "
            "indices of the two numbers that add up to target.\n\n"
            "Return the indices as a list [i, j] with i < j. Assume exactly one "
            "valid answer exists, and you may not use the same element twice.\n\n"
            "Example: nums=[2,7,11,15], target=9  ->  [0, 1]"
        ),
        "starter_code": (
            "def two_sum(nums, target):\n"
            "    # your code here\n"
            "    pass\n"
        ),
        "test_cases": [
            {"name": "basic",        "args": [[2, 7, 11, 15], 9],      "expected": [0, 1]},
            {"name": "middle",       "args": [[3, 2, 4], 6],           "expected": [1, 2]},
            {"name": "duplicates",   "args": [[3, 3], 6],              "expected": [0, 1]},
            {"name": "negatives",    "args": [[-1, -2, -3, -4], -6],   "expected": [1, 3]},
            {"name": "large-span",   "args": [[0, 4, 3, 0], 0],        "expected": [0, 3]},
        ],
    }
}


def get_problem(problem_id: str):
    return PROBLEMS.get(problem_id)
