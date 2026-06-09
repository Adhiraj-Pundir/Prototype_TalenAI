"""
PROTOTYPE EXECUTOR — runs candidate code in a subprocess with a timeout.

!!! SECURITY WARNING !!!
This executes arbitrary user code on the host with NO sandboxing.
Fine for a local demo. For production you MUST swap this for an isolated
runner: Judge0 (hosted code-execution API), a per-submission Docker
container with no network + resource limits, or gVisor/Firecracker.
Do not ship this function to anything candidates can reach.
"""

import subprocess
import json
import tempfile
import os

TIMEOUT_SECONDS = 10


def run_python(code: str, function_name: str, test_cases: list) -> list:
    harness = f'''
import json

{code}

_results = []
_tests = {json.dumps(test_cases)}
for _t in _tests:
    try:
        _got = {function_name}(*_t["args"])
        _passed = _got == _t["expected"]
        _results.append({{
            "name": _t["name"], "passed": _passed,
            "expected": repr(_t["expected"]), "got": repr(_got), "error": None
        }})
    except Exception as _e:
        _results.append({{
            "name": _t["name"], "passed": False,
            "expected": repr(_t["expected"]), "got": None, "error": str(_e)
        }})
print(json.dumps(_results))
'''
    path = None
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
            f.write(harness)
            path = f.name

        proc = subprocess.run(
            ["python3", path],
            capture_output=True, text=True, timeout=TIMEOUT_SECONDS,
        )

        if proc.returncode != 0:
            # syntax error / crash before any test ran
            return [{
                "name": "compile_or_runtime",
                "passed": False,
                "expected": "code that runs",
                "got": None,
                "error": (proc.stderr.strip() or "Unknown error")[:800],
            }]

        last_line = proc.stdout.strip().splitlines()[-1]
        return json.loads(last_line)

    except subprocess.TimeoutExpired:
        return [{
            "name": "timeout", "passed": False,
            "expected": f"finish within {TIMEOUT_SECONDS}s",
            "got": None, "error": "Execution timed out (possible infinite loop)",
        }]
    except Exception as e:
        return [{
            "name": "harness_error", "passed": False,
            "expected": "", "got": None, "error": str(e),
        }]
    finally:
        if path and os.path.exists(path):
            os.unlink(path)
