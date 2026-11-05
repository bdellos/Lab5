from __future__ import annotations

from dataclasses import dataclass

Position = tuple[int, int]

GRID = (
    (0, 0, 0, 0),
    (0, "X", 0, 0),
    (0, 0, 0, 0),
    (0, -1, 0, 10),
)
START: Position = (0, 0)
GOAL: Position = (3, 3)
ACTIONS = ("up", "down", "left", "right")

_DELTAS = {
    "up": (-1, 0),
    "down": (1, 0),
    "left": (0, -1),
    "right": (0, 1),
}


@dataclass
class VacuumEnvironment:

    grid: tuple = GRID
    start: Position = START
    goal: Position = GOAL

    def __post_init__(self) -> None:
        if not self.grid:
            raise ValueError("Grid must contain at least one row.")

        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        if self.cols == 0:
            raise ValueError("Grid must contain at least one column.")
        if any(len(row) != self.cols for row in self.grid):
            raise ValueError("Grid must be rectangular.")
        if not self.is_valid_position(self.start):
            raise ValueError("Start must be an in-bounds, traversable cell.")
        if not self.is_valid_position(self.goal):
            raise ValueError("Goal must be an in-bounds, traversable cell.")
        self.reset()

    def reset(self) -> Position:
        self.position = self.start
        self.done = False
        return self.position

    def is_valid_position(self, position: Position) -> bool:
        row, col = position
        return (
            0 <= row < self.rows
            and 0 <= col < self.cols
            and self.grid[row][col] != "X"
        )

    def step(self, action: str) -> tuple[Position, float, bool]:
        if self.done:
            raise RuntimeError("Episode has ended. Call reset() before stepping.")
        if action not in _DELTAS:
            raise ValueError(f"Unknown action: {action!r}")

        dr, dc = _DELTAS[action]
        row, col = self.position
        candidate = (row + dr, col + dc)

        if not self.is_valid_position(candidate):
            return self.position, 0.0, False

        self.position = candidate
        cell_value = self.grid[row + dr][col + dc]

        if self.position == self.goal or cell_value == 10:
            reward = 10.0
            self.done = True
        elif cell_value == -1:
            reward = -1.0
        else:
            reward = 0.0

        return self.position, reward, self.done
