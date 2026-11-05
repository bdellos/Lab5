import pytest

from src.environment import GRID, START, VacuumEnvironment


def test_grid_shape_and_known_cells():
    assert GRID == (
        (0, 0, 0, 0),
        (0, "X", 0, 0),
        (0, 0, 0, 0),
        (0, -1, 0, 10),
    )
    assert len(GRID) == 4
    assert all(len(row) == 4 for row in GRID)
    assert START == (0, 0)
    assert GRID[1][1] == "X"
    assert GRID[3][1] == -1
    assert GRID[3][3] == 10


def test_cannot_move_into_blocked_cell():
    env = VacuumEnvironment()
    env.position = (1, 0)
    next_state, reward, done = env.step("right")
    assert next_state == (1, 0)
    assert reward == 0
    assert done is False


def test_boundary_move_is_rejected():
    env = VacuumEnvironment()
    next_state, reward, done = env.step("up")
    assert next_state == (0, 0)
    assert reward == 0
    assert done is False


def test_negative_cell_is_penalty_not_terminal():
    env = VacuumEnvironment()
    env.position = (3, 0)
    next_state, reward, done = env.step("right")
    assert next_state == (3, 1)
    assert reward == -1
    assert done is False

    next_state, reward, done = env.step("right")
    assert next_state == (3, 2)
    assert reward == 0
    assert done is False


def test_goal_gives_ten_and_ends_episode():
    env = VacuumEnvironment()
    env.position = (3, 2)
    next_state, reward, done = env.step("right")
    assert next_state == (3, 3)
    assert reward == 10
    assert done is True


def test_unknown_action_does_not_change_environment():
    env = VacuumEnvironment()
    with pytest.raises(ValueError, match="Unknown action"):
        env.step("stay")
    assert env.position == START
    assert env.done is False


@pytest.mark.parametrize(
    "grid",
    [(), ((),), ((0, 0), (0,))],
    ids=["no-rows", "no-columns", "non-rectangular"],
)
def test_malformed_grid_is_rejected(grid):
    with pytest.raises(ValueError):
        VacuumEnvironment(grid=grid)


@pytest.mark.parametrize(
    ("start", "goal"),
    [
        ((-1, 0), (3, 3)),
        ((1, 1), (3, 3)),
        ((0, 0), (4, 3)),
        ((0, 0), (1, 1)),
    ],
    ids=["start-out-of-bounds", "start-blocked", "goal-out-of-bounds", "goal-blocked"],
)
def test_invalid_start_or_goal_is_rejected(start, goal):
    with pytest.raises(ValueError, match="Start|Goal"):
        VacuumEnvironment(start=start, goal=goal)


def test_cannot_step_after_terminal_until_reset():
    env = VacuumEnvironment()
    env.position = (3, 2)
    env.step("right")
    with pytest.raises(RuntimeError, match="Episode has ended"):
        env.step("left")
    assert env.reset() == START
    assert env.done is False
