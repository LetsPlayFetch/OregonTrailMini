# OregonTrailMini

OregonTrailMini is a simple survival sim built to interact with reinforcement learning agents. I built this to be simple, readable, and easy to follow for people learning how RL(Reinforecent Learning) works.

---
## How to Run it 
 
Once you've cloned the repo, install Python 3, any dependencies, then run:
 
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

Every day, the agent (or player) picks one of three actions with corresponding effects:
- `travel`: might cause injury, moves forward
- `hunt`: might cause injury, might gain food
- `rest`: might heal

There goal is make it to end without dying and with the best speed.

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

Above this it handles the daily food consumption, it can go negative by a few but forces itsselt to correct and makes up the defecit.

Below it validates if the game is over and steps to the next day

Run out of health, lose. 
Make it to the end, win.

---

## Game Variables

In addition to this, you also have variables defined in the main OregonTrailMini class:

```OregonTrailMini.py
def reset(self):
    self.state = {
        "day": 0,         # for counting
        "distance": 0,    #    ``
        "goal": 500,
        "food": 10,
        "health": 5,
        "alive": True,
        "events": []
    }
```

By increasing your goal, and giving the game more complex conditional logic you can affect how it learns

Right now it attains the greedy solution after about 20,000 attempts than just continues the same 'Random checking pattern 

***Add a photo here of that graph


"I have additional models built upon the base offering a much harder, and longer game..

you can the that model here over the course of 20,000

In the provided demo the given soltuion is pretty easy to obtain ourselves... We can put this kind of program into an advanced homework implementation. 

Our pioneer needs to travel 500 miles, everyday he is given 3 options. Traveling, Resting and Hunting. Traveling progresses him 10, 15, or 20 miles. 
---
## How RandomAgent Works


The most important variable is the number of episodes. This controls how many simulations the agent will run while training. 

You can set it here in:
OregonTrailMini.py
```python
if __name__ == "__main__":
    game = OregonTrailMini()
    agent = QLearningAgent(actions=["rest", "hunt", "travel"])
    game.run_agent(agent, episodes=100000)
```

The agent uses Q-learning. At first, it’s mostly guessing just trying out random actions. But as it plays more games, it starts to figure out what works and doesn’t.


Each state (move) is compressed into a key like:
```python
(state["distance"] // 10, state["food"] // 5, state["health"])
```

Then it decides what move to take here. If it's still exploring it'll just pick randomly:
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
 ```OregonTrailMini.py
         if s["health"] <= 0:
            s["alive"] = False 
            reward -= 1000

        if s["distance"] >= s["goal"]:
            s["alive"] = False          # Changing state to dead is how the game ends
            s["events"].append("You reached your goal!")
            reward += 5000 - (s["day"] * 1)

        return s.copy(), reward, not s["alive"], {}
```

# Results
![This is the graph for Oregon Trail rl, it shows performance maxind out around 7,000 trials](resources/graph1.jpg "Graph 1")

I have additional variations and builds that i hope to add for contrast here soon 
---

#

## Planned addition 
 - I want to add a more dynamic difficulty system.  
 - Rewards will better reflect progress — for example, dying still gives -1000 even if you were close to finishing.
 - Implement pickle
 - Fix death colloum to show reson of death (more advance game tracking stuff)

## Feedback
 Known Bug: Aware that theres a problem 
I'm actively looking to make improvements to the game specifically its difficulty balance.
 
If you have ideas, thoughts, or suggestions, feel free to reach out to me on GitHub.