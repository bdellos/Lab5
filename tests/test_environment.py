from src.environment import GRID, START, VacuumEnvironment


def test_grid_shape_and_known_cells():
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


def test_goal_gives_ten_and_ends_episode():
    env = VacuumEnvironment()
    env.position = (3, 2)
    next_state, reward, done = env.step("right")
    assert next_state == (3, 3)
    assert reward == 10
    assert done is True


def test_cannot_step_after_terminal_until_reset():
    env = VacuumEnvironment()
    env.position = (3, 2)
    env.step("right")
    try:
        env.step("left")
        assert False, "Expected RuntimeError after terminal state"
    except RuntimeError:
        pass
    assert env.reset() == START
