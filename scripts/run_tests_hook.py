import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    project_dir = Path(
        os.environ.get("CLAUDE_PROJECT_DIR", Path(__file__).resolve().parents[1])
    ).resolve()
    tests_dir = project_dir / "tests"

    test_files = (
        list(tests_dir.glob("test_*.py")) +
        list(tests_dir.glob("*_test.py"))
    ) if tests_dir.is_dir() else []

    if not test_files:
        print("HOOK: No pytest test files found; skipping.")
        return 0

    print(f"HOOK: Running {len(test_files)} test file(s) with pytest...")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=project_dir,
        text=True,
    )
    if result.returncode:
        print("HOOK: Tests failed. Review the pytest output.")
        return 2

    print("HOOK: All tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())