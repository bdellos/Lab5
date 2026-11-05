from __future__ import annotations

import random
from collections import defaultdict

from src.environment import ACTIONS, Position, VacuumEnvironment


def update_q_value(
    old_q: float,
    reward: float,
    best_next_q: float,
    learning_rate: float,
    discount_factor: float,
    terminal: bool = False,
) -> float:
    """One Q-learning update; terminal transitions do not bootstrap."""
    future_value = 0.0 if terminal else discount_factor * best_next_q
    return old_q + learning_rate * (reward + future_value - old_q)


class QLearningAgent:
    def __init__(
        self,
        actions=ACTIONS,
        learning_rate: float = 0.1,
        discount_factor: float = 0.99,
        epsilon: float = 1.0,
        min_epsilon: float = 0.05,
        epsilon_decay: float = 0.995,
        seed: int | None = 7,
    ):
        if not 0 < learning_rate <= 1:
            raise ValueError("learning_rate must be in (0, 1].")
        if not 0 <= discount_factor <= 1:
            raise ValueError("discount_factor must be in [0, 1].")
        if not 0 <= min_epsilon <= epsilon <= 1:
            raise ValueError("Require 0 <= min_epsilon <= epsilon <= 1.")
        if not 0 < epsilon_decay <= 1:
            raise ValueError("epsilon_decay must be in (0, 1].")

        self.actions = tuple(actions)
        self.alpha = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.min_epsilon = min_epsilon
        self.epsilon_decay = epsilon_decay
        self.q_values = defaultdict(float)
        self.rng = random.Random(seed)

    def choose_action(self, state: Position, explore: bool = True) -> str:
        if explore and self.rng.random() < self.epsilon:
            return self.rng.choice(self.actions)
        values = [self.q_values[(state, action)] for action in self.actions]
        best = max(values)
        best_actions = [
            action for action, value in zip(self.actions, values)
            if value == best
        ]
        return self.rng.choice(best_actions)

    def learn(
        self,
        state: Position,
        action: str,
        reward: float,
        next_state: Position,
        terminal: bool,
    ) -> None:
        old_q = self.q_values[(state, action)]
        best_next_q = max(
            self.q_values[(next_state, next_action)]
            for next_action in self.actions
        )
        self.q_values[(state, action)] = update_q_value(
            old_q,
            reward,
            best_next_q,
            self.alpha,
            self.gamma,
            terminal,
        )

    def decay_exploration(self) -> None:
        self.epsilon = max(
            self.min_epsilon, self.epsilon * self.epsilon_decay
        )


def train_agent(
    episodes: int = 5000,
    max_steps: int = 100,
    seed: int = 7,
) -> tuple[QLearningAgent, list[float]]:
    """Train from interaction; no transition or reward table is given to agent."""
    env = VacuumEnvironment()
    agent = QLearningAgent(seed=seed)
    episode_returns: list[float] = []

    for _ in range(episodes):
        state = env.reset()
        total_reward = 0.0

        for _step in range(max_steps):
            action = agent.choose_action(state)
            next_state, reward, done = env.step(action)
            agent.learn(state, action, reward, next_state, done)
            state = next_state
            total_reward += reward
            if done:
                break

        episode_returns.append(total_reward)
        agent.decay_exploration()

    return agent, episode_returns


def run_greedy_episode(
    agent: QLearningAgent,
    max_steps: int = 100,
) -> tuple[list[Position], float, bool]:
    """Evaluate the learned policy without exploration."""
    env = VacuumEnvironment()
    state = env.reset()
    path = [state]
    total_reward = 0.0

    for _ in range(max_steps):
        action = agent.choose_action(state, explore=False)
        state, reward, done = env.step(action)
        path.append(state)
        total_reward += reward
        if done:
            return path, total_reward, True

    return path, total_reward, False
