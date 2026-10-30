import json
import subprocess
import sys
import tempfile
from pathlib import Path


def run_exercise(code: str, exercise: dict) -> tuple[bool, str]:
    harness = f"""
import importlib.util
import inspect
import json
spec = importlib.util.spec_from_file_location("submission", {json.dumps("submission.py")})
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
cases = json.loads({json.dumps(json.dumps(exercise["tests"]))})
def normalize(value):
    if isinstance(value, tuple):
        return [normalize(item) for item in value]
    if isinstance(value, list):
        return [normalize(item) for item in value]
    if isinstance(value, dict):
        return {{key: normalize(item) for key, item in value.items()}}
    return value

for number, case in enumerate(cases, 1):
    actual = getattr(module, {json.dumps(exercise["function"])})(*case["args"])
    if "followup_args" in case:
        actual = actual(*case["followup_args"])
    if inspect.isgenerator(actual):
        actual = list(actual)
    if normalize(actual) != case["expected"]:
        raise AssertionError(f"Test {{number}} failed: expected {{case['expected']!r}}, got {{actual!r}}")
print(f"All {{len(cases)}} tests passed.")
"""
    with tempfile.TemporaryDirectory(prefix="learn-practice-") as directory:
        submission_path = Path(directory) / "submission.py"
        submission_path.write_text(code, encoding="utf-8")
        try:
            result = subprocess.run(
                [sys.executable, "-I", "-c", harness],
                cwd=directory,
                capture_output=True,
                text=True,
                timeout=3,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return False, "Execution timed out after 3 seconds."
    output = (result.stdout + result.stderr).strip()
    if result.returncode == 0:
        return True, output or "All tests passed."
    return False, output[-3000:] or "The submitted code did not pass."
