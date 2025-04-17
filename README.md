# OregonTrailMini
 
OregonTrailMini is a simple survival sim built to interact with reinforcement learning agents. I built this to be simple, readable, and easy to follow — especially for people learning how RL works.

---
 
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
 
## Game Overview

Every day, the agent picks one of three actions with corresponding effects:
- `travel`: costs food, might cause injury, moves forward
- `hunt`: costs food, might cause injury, might gain food
- `rest`: costs food, chance to heal

Health is measured from 0 to 5 — 0 means you're dead, 5 means you're healthy.

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
    game.run_agent(agent, episodes=10000)
```
In addition to this, you also have variables defined in the main OregonTrailMini class in:

```python
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
```
You shouldn’t modify day or distance; they are how we track progress. Goal can be lengthened or shortened to affect game duration (in that order). Food and health are your starting values. Health shouldn't go above 5. I wouldn’t recommend changing these in the future.

---
## Game functions 
- They control how actions affect the game
- More to come in the future here
---
 
## Reward System
 
 - **Dying is very bad**: -1000 points
 - **Winning is very good**: Up to +1000, scaled by how fast you made it
 - **Faster win is better**: Getting there fast matters (-1 point per day)

---

## Planned addition 
I want to add a more dynamic difficulty system.  
Rewards will better reflect progress — for example, dying still gives -1000 even if you were close to finishing.
Implement pickle


## 💬 Feedback
 
I'm actively looking to make improvements to the game specifically its difficulty balance.
 
If you have ideas, thoughts, or suggestions, feel free to reach out to me on GitHub.