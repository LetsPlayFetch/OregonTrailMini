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
            "goal": 2000,
            "food": 10,
            "health": 3,
            "alive": True,
            "events": []
        }

    def step(self, action):
        s = self.state
        s["day"] += 1
        s["events"] = []
        reward = 0

        if s["food"] <= 0:
            s["health"] -= 1
            s["events"].append("No food! Lost 1 health.")
        else:
            s["food"] -= 3

        if action == "rest":
            s["food"] -= 2  # increase food used for resting
            if s["health"] < 5:
                if random.random() < 0.4:
                    s["health"] += 1
                    s["events"].append("Rested and gained 1 health.")
                else:
                    s["events"].append("Rested but no health gained.")
            else:
                s["events"].append("Rested but already at full health.")
        elif action == "hunt":
            food_found = random.randint(3, 8)
            s["food"] += food_found
            if random.random() < 0.3:
                s["health"] -= 1
                s["events"].append(f"Hunted and found {food_found} food, but got injured.")
            else:
                s["events"].append(f"Hunted and found {food_found} food.")
        elif action == "travel":
            dist = random.randint(5, 15)
            s["food"] -= 2  # extra food cost for traveling
            s["distance"] += dist
            s["events"].append(f"Traveled {dist} miles.")
            if random.random() < 0.2:
                s["health"] -= 1
                s["events"].append("Injured while traveling.")
        else:
            s["events"].append("Invalid action.")
            reward = 0

        if s["health"] <= 0:
            s["alive"] = False
            s["events"].append("Died from poor health.")
            reward = -1000

        if s["distance"] >= s["goal"]:
            s["alive"] = False
            s["events"].append("You reached your goal!")
            reward = 1000 - s["day"] * 1

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

                # print(f"\nDay {self.state['day']} | Action: {action}")
                # print(f"Distance: {self.state['distance']}/{self.state['goal']} | Food: {self.state['food']} | Health: {self.state['health']}")
                # for e in self.state['events']:
                #     print(f"- {e}")

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
    game.run_agent(agent, episodes=20000)
