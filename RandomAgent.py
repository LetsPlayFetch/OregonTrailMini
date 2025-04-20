import random
import pickle

class QLearningAgent:
    def __init__(self, actions, learning_rate=0.1, discount_factor=0.95, exploration_rate=0.1):
        self.q_table = {}  # (state, action) -> value
        self.actions = actions
        self.lr = learning_rate
        self.df = discount_factor
        self.epsilon = exploration_rate

    def choose_action(self, state):
        state_key = self._state_to_key(state)
        if random.random() < self.epsilon or state_key not in self.q_table:
            return random.choice(self.actions)
        return max(self.q_table[state_key], key=self.q_table[state_key].get)

    def learn(self, state, action, reward, next_state):
        state_key = self._state_to_key(state)
        next_key = self._state_to_key(next_state)

        if state_key not in self.q_table:
            self.q_table[state_key] = {a: 0.0 for a in self.actions}
        if next_key not in self.q_table:
            self.q_table[next_key] = {a: 0.0 for a in self.actions}

        current_q = self.q_table[state_key][action]
        max_future_q = max(self.q_table[next_key].values())
        updated_q = current_q + self.lr * (reward + self.df * max_future_q - current_q)

        self.q_table[state_key][action] = updated_q

    def _state_to_key(self, state):
        return (state["distance"] , state["food"] , state["health"])
