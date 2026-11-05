import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


def report(message: str, copilot_mode: bool) -> None:
    if copilot_mode:
        print(json.dumps({"type": "progress", "message": message}), flush=True)
    else:
        print(f"HOOK: {message}")


def main(copilot_mode: bool = False) -> int:
    project_dir = Path(
        Path(__file__).resolve().parents[1]
        if copilot_mode
        else os.environ.get("CLAUDE_PROJECT_DIR", Path(__file__).resolve().parents[1])
    ).resolve()
    tests_dir = project_dir / "tests"

    test_files = (
        list(tests_dir.glob("test_*.py")) +
        list(tests_dir.glob("*_test.py"))
    ) if tests_dir.is_dir() else []

    if not test_files:
        report("No pytest test files found; skipping.", copilot_mode)
        if copilot_mode:
            print("{}")
        return 0

    report(f"Running {len(test_files)} test file(s) with pytest...", copilot_mode)
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=project_dir,
        text=True,
        capture_output=copilot_mode,
    )
    if copilot_mode:
        for output in (result.stdout, result.stderr):
            if output:
                print(output, file=sys.stderr, end="" if output.endswith("\n") else "\n")
        summary = next(
            (
                line.strip()
                for line in reversed((result.stdout + result.stderr).splitlines())
                if re.search(r"\b(passed|failed|error|errors|skipped|xfailed)\b", line)
            ),
            f"pytest exited with status {result.returncode}",
        )
        report(f"pytest: {summary}", copilot_mode)
        print("{}")
    if result.returncode:
        if not copilot_mode:
            print("HOOK: Tests failed. Review the pytest output.")
        return 2

    if not copilot_mode:
        print("HOOK: All tests passed.")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--copilot", action="store_true")
    args = parser.parse_args()
    raise SystemExit(main(copilot_mode=args.copilot))
