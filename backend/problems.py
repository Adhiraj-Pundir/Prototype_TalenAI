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
    },
    "palindrome-number": {
        "id": "palindrome-number",
        "title": "Palindrome Number",
        "function_name": "is_palindrome",
        "description": (
            "Given an integer `x`, return true if `x` is a palindrome, and false otherwise.\n\n"
            "An integer is a palindrome when it reads the same forward and backward.\n\n"
            "Example 1: x = 121 -> true\n"
            "Example 2: x = -121 -> false (From left to right, it reads -121. From right to left, it becomes 121-.)\n"
            "Example 3: x = 10 -> false\n"
        ),
        "starter_code": (
            "def is_palindrome(x):\n"
            "    # your code here\n"
            "    pass\n"
        ),
        "test_cases": [
            {"name": "positive-palindrome",  "args": [121],    "expected": True},
            {"name": "negative",             "args": [-121],   "expected": False},
            {"name": "ends-with-zero",       "args": [10],     "expected": False},
            {"name": "zero",                 "args": [0],      "expected": True},
            {"name": "large-palindrome",     "args": [12321],  "expected": True},
        ],
    },
    "valid-anagram": {
        "id": "valid-anagram",
        "title": "Valid Anagram",
        "function_name": "is_anagram",
        "description": (
            "Given two strings `s` and `t`, return true if `t` is an anagram of `s`, and false otherwise.\n\n"
            "An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, "
            "typically using all the original letters exactly once.\n\n"
            "Example 1: s = 'anagram', t = 'nagaram' -> true\n"
            "Example 2: s = 'rat', t = 'car' -> false\n"
        ),
        "starter_code": (
            "def is_anagram(s, t):\n"
            "    # your code here\n"
            "    pass\n"
        ),
        "test_cases": [
            {"name": "basic-true",     "args": ["anagram", "nagaram"],  "expected": True},
            {"name": "basic-false",    "args": ["rat", "car"],          "expected": False},
            {"name": "length-diff",    "args": ["a", "ab"],             "expected": False},
            {"name": "empty",          "args": ["", ""],                "expected": True},
            {"name": "same-letters",   "args": ["aabb", "bbaa"],        "expected": True},
        ],
    }
}


def get_problem(problem_id: str):
    return PROBLEMS.get(problem_id)
