---
name: validate-environment
description: This skill validates the environment for things like boundaries and terminal states.
---
If a terminal state is reached, return what the state is; for example, if the goal state is reached, return "goal state reached". If a boundary is reached, return "boundary reached". If the environment is valid and no terminal state or boundary is reached, return "environment valid".