import random
import json
import csv
import os
from RandomAgent import QLearningAgent

class OregonTrailMini:
    def __init__(self):
        self.reset()

    def reset(self):
        self.state = {
            "day": 0,
            "distance": 0,
            "goal": 500,
            "food": 10,
            "health": 5,
            "alive": True,
            "events": [],
        }

    def step(self, action):
        s = self.state
        s["day"] += 1
        s["events"] = []
        reward = 0

        if s["food"] <= 0:    # Reduce health from hunger,no food.
            s["health"] -= 1
        else:
            s["food"] -= 5    # Daily food consumption

        if action == "rest":
            if s["health"] < 5:
                if random.random() < 0.5:
                    s["health"] += 1

        elif action == "hunt":
            s["food"] += random.randint(5, 15) # Food found while hunting 
            if random.random() < 0.3: # Possibility of injury
                s["health"] -= 1

        elif action == "travel":
            dist = random.randint(5, 15)
            s["distance"] += dist
            s["events"].append(f"Traveled {dist} miles.")
            if random.random() < 0.1:
                s["health"] -= 1
            
        else:
            s["events"].append("Invalid action.")

        if s["health"] <= 0:
            s["alive"] = False 
            reward -= 1000

        if s["distance"] >= s["goal"]:
            s["alive"] = False          # Changing state to dead is how the game ends
            s["events"].append("You reached your goal!")
            reward += 5000 - (s["day"] * 7)

        return s.copy(), reward, not s["alive"], {}

    def get_state(self):
        return self.state.copy()

    def run_agent(self, agent, episodes=1):
        results = []
        for ep in range(episodes):
            self.reset()
            state = self.get_state()
            done = False

            while not done:
                action = agent.choose_action(state)
                next_state, reward, done, _ = self.step(action)
                agent.learn(state, action, reward, next_state)
                state = next_state

            results.append({
                "episode": ep,
                "survived_days": self.state["day"],
                "distance": self.state["distance"],
                "result": "win" if self.state["distance"] >= self.state["goal"] else "death"
            })

        # Write results to CSV of the run
        os.makedirs("trial", exist_ok=True)
        existing_files = os.listdir("trial")
        i = 0
        while f"training_results_{i:02}.csv" in existing_files:
            i += 1
        filename = f"training_results_{i:02}.csv"
        filepath = os.path.join("trial", filename)
        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)

if __name__ == "__main__":
    game = OregonTrailMini()
    agent = QLearningAgent(actions=["rest", "hunt", "travel"])
    game.run_agent(agent, episodes=50000)
