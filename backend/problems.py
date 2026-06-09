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
            "<p>Given an array of integers <code>nums</code> and an integer <code>target</code>, "
            "return <em>indices of the two numbers such that they add up to <code>target</code></em>.</p>"
            "<p>You may assume that each input would have <strong>exactly one solution</strong>, "
            "and you may not use the <em>same</em> element twice.</p>"
            "<p>You can return the answer in any order.</p>"
            "<div style='margin-top: 20px;'><strong>Example 1:</strong></div>"
            "<blockquote style='margin: 8px 0; padding: 8px 12px; background: #1f2937; border-left: 4px solid #30363d; border-radius: 4px;'>"
            "<strong>Input:</strong> nums = [2,7,11,15], target = 9<br/>"
            "<strong>Output:</strong> [0,1]<br/>"
            "<strong>Explanation:</strong> Because nums[0] + nums[1] == 9, we return [0, 1]."
            "</blockquote>"
            "<div style='margin-top: 16px;'><strong>Example 2:</strong></div>"
            "<blockquote style='margin: 8px 0; padding: 8px 12px; background: #1f2937; border-left: 4px solid #30363d; border-radius: 4px;'>"
            "<strong>Input:</strong> nums = [3,2,4], target = 6<br/>"
            "<strong>Output:</strong> [1,2]"
            "</blockquote>"
            "<div style='margin-top: 16px;'><strong>Example 3:</strong></div>"
            "<blockquote style='margin: 8px 0; padding: 8px 12px; background: #1f2937; border-left: 4px solid #30363d; border-radius: 4px;'>"
            "<strong>Input:</strong> nums = [3,3], target = 6<br/>"
            "<strong>Output:</strong> [0,1]"
            "</blockquote>"
            "<div style='margin-top: 20px; font-weight: bold;'>Constraints:</div>"
            "<ul style='margin-top: 6px; padding-left: 20px;'>"
            "<li><code>2 &lt;= nums.length &lt;= 10<sup>4</sup></code></li>"
            "<li><code>-10<sup>9</sup> &lt;= nums[i] &lt;= 10<sup>9</sup></code></li>"
            "<li><code>-10<sup>9</sup> &lt;= target &lt;= 10<sup>9</sup></code></li>"
            "<li><strong>Only one valid answer exists.</strong></li>"
            "</ul>"
            "<div style='margin-top: 20px;'><strong>Follow-up:</strong> Can you come up with an algorithm that is less than <code>O(n<sup>2</sup>)</code> time complexity?</div>"
        ),
        "hint": "Try using a hash map to store the index of each number as you traverse the array. For each number, check if its complement (target - number) already exists in the hash map.",
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
