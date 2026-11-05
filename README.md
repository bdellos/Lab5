# Lab 5: Vacuum Grid Q-Learning

This line exists to trigger the automatic test hook.

## Environment

The default environment is a 4x4 grid indexed by zero-based `(row, column)`
coordinates. The robot starts at `(0, 0)`, `(1, 1)` is blocked, `(3, 1)` gives
`-1`, and `(3, 3)` contains the `10` goal. Other cells contain `0`.

The simulator currently treats moves off-grid or into `X` as no-ops with
zero reward. Entering `-1` gives `-1` and leaves the episode active; entering
the goal gives `10` and ends it. These movement and reward semantics are the
implemented behavior; confirm them against the assignment handout if it
specifies different rules.

## Learning

`QLearningAgent` learns action values from observed
`(state, action, reward, next_state, terminal)` transitions. It is not given a
route, transition table, or reward table. `train_agent` runs 5,000 episodes
with a 100-step episode limit by default; `run_greedy_episode` evaluates the
learned values without exploration.

Current configuration defaults (implementation choices, not stated assignment
requirements):

| Parameter | Value |
|---|---:|
| Learning rate | 0.1 |
| Discount factor | 0.99 |
| Initial exploration rate | 1.0 |
| Minimum exploration rate | 0.05 |
| Exploration decay | 0.995 per episode |
| Random seed | 7 |

## Tests and hook

Run the test suite with `python -m pytest -q`. The Claude Code
`PostToolUse` hook in `.claude/settings.json` runs `scripts/run_tests_hook.py`
after matched `Write` or `Edit` tools; that script runs the full pytest suite
when test files exist. It does not cover every way files can be changed (for
example, shell edits or edits by another agent that do not use those tools).
The `Stop` hook is a review prompt, not a test command.

To run only the environment tests, use
`python -m pytest -q tests/test_environment.py`.

For VS Code's Copilot agent session target, `.github/hooks/run-tests.json`
runs the same script after every successful tool use, including file edits.
This hook is not limited to edit tools, so it also runs after other tool calls.
Workspace hook support is preview functionality and may require workspace
trust; select the Copilot session target and reload/start a session after
adding or changing the hook.