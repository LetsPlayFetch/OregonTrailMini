# OregonTrailMini

OregonTrailMini is a simple survival sim built to interact with reinforcement learning agents. I built this to be simple, readable, and easy to follow — especially for people learning how RL works.

---
## Version Updates
Simplified game logic, removed bloat 

## How to Run it 
 
Once you've cloned the repo, install Python 3 and any dependencies, then run:
 
```bash
python3 OregonTrailMini.py
```
 
That’s it. It will automatically run simulations using Q-learning.
 
Once it finishes all simulations, it will output a file like:
 
```
training_results_00.csv
```
 
You can use this to interpret how well the agent learned over time 

---
 
## How the game works

Every day, the agent picks one of three actions with corresponding effects:
- `travel`: might cause injury, moves forward
- `hunt`: might cause injury, might gain food
- `rest`: might heal

You can build upon this logic, or change the effects of events here 
```OregonTrailMini.py
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
```

Additional logic is handled above and below this,

Run out of health and it’s game over. Make it to the end, you win.

---

## Game Variables


The most important variable is the number of episodes.
This controls how many simulations the agent will run while training

You can set it here in:
OregonTrailMini.py
```python
if __name__ == "__main__":
    game = OregonTrailMini()
    agent = QLearningAgent(actions=["rest", "hunt", "travel"])
    game.run_agent(agent, episodes=100000)
```
In addition to this, you also have variables defined in the main OregonTrailMini class in:

```python
def reset(self):
    self.state = {
        "day": 0,
        "distance": 0,
        "goal": 500,
        "food": 10,
        "health": 5,
        "alive": True,
        "events": []
    }
```
You shouldn’t modify day or distance; they are how we track progress. Goal can be lengthened or shortened to affect game duration (in that order). Food and health are your starting values. Health shouldn't go above 5. I wouldn’t recommend changing these in the future.

---
## How RandomAgent Works

The agent uses Q-learning. At first, it’s mostly guessing just trying out random actions. But as it plays more games, it starts to figure out what works and doesn’t.


Each state (move) is compressed into a key like:
```python
(state["distance"] // 10, state["food"] // 5, state["health"])
```

Then it decides what move to take. If it's still exploring it'll just pick randomly:
```python
if random.random() < self.epsilon:
    return random.choice(self.actions)
```

Otherwise, it goes with what it thinks is best:
```python
return max(self.q_table[state_key], key=self.q_table[state_key].get)
```

Every time it does something, it updates its memory (Q-table) like this:
```python
updated_q = current_q + self.lr * (reward + self.df * max_future_q - current_q)
```


## Reward System
 
 - **Dying is very bad**: -1000 points
 - **Winning is very good**: Up to +1000, scaled by how fast you made it
 - **Faster win is better**: Getting there fast matters (-1 point per day)

---

## Planned addition 
 - I want to add a more dynamic difficulty system.  
 - Rewards will better reflect progress — for example, dying still gives -1000 even if you were close to finishing.
 - Implement pickle
 - Add Trials to 

## 💬 Feedback
 
I'm actively looking to make improvements to the game specifically its difficulty balance.
 
If you have ideas, thoughts, or suggestions, feel free to reach out to me on GitHub.