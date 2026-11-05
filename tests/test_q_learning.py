from src.q_learning import (
    QLearningAgent,
    run_greedy_episode,
    train_agent,
    update_q_value,
)


def test_nonterminal_q_update():
    # 0 + 0.1 * (2 + 0.9*5 - 0) = 0.65
    result = update_q_value(0, 2, 5, 0.1, 0.9, terminal=False)
    assert abs(result - 0.65) < 1e-12


def test_terminal_update_does_not_bootstrap():
    # Terminal update: 0 + 0.1 * (10 - 0) = 1.
    result = update_q_value(0, 10, 999, 0.1, 0.9, terminal=True)
    assert abs(result - 1.0) < 1e-12


def test_epsilon_decays_but_not_below_minimum():
    agent = QLearningAgent(epsilon=0.1, min_epsilon=0.05,
                           epsilon_decay=0.5, seed=1)
    agent.decay_exploration()
    assert agent.epsilon == 0.05
    agent.decay_exploration()
    assert agent.epsilon == 0.05


def test_agent_learns_to_reach_goal():
    agent, returns = train_agent(episodes=5000, seed=7)
    path, total_reward, reached_goal = run_greedy_episode(agent)
    assert reached_goal, f"Greedy policy did not reach goal; path={path}"
    assert path[-1] == (3, 3)
    assert total_reward > 0
    assert len(returns) == 5000
