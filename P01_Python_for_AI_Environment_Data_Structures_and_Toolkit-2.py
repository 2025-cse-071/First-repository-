# # Practical 01 — Python for AI - Environment, Data Structures and the Toolkit
# 
# **Artificial Intelligence 3(2-1) · BS Computer Science · Semester III**
# 
# | | |
# |---|---|
# | **Week** | 1 |
# | **Related lectures** | Lectures 1 and 2 |
# | **Duration** | 3 hours |
# | **Submission** | This notebook, run top to bottom from a clean kernel |



# ## 1. Objectives
# 
# By the end of this session you will be able to:
# 
# 1. Set up and verify the Python environment used throughout this course.
# 2. Use the data structures that every later practical depends on: lists, dictionaries, sets and tuples.
# 3. Write and use generators, and explain how they differ from lists.
# 4. Represent an agent's percepts, actions and belief state in Python.
# 5. Implement the sense-update-decide-act loop from Lecture 2.



# ## 2. Background theory
# 
# Lecture 2 described an agent as running a loop: it senses the environment, updates a bounded summary of the past called the **belief state**, decides on an action from that summary alone, and acts. Today you build that loop in Python.
# 
# The programming ideas here are not incidental. Every later practical uses dictionaries to map situations to values, sets to record what has already been visited, and generators to produce candidate moves one at a time rather than building an enormous list in memory. If these are unfamiliar now, the search practicals in weeks 4 and 5 will be much harder than they need to be.



# **Key points to keep in mind while you work:**
# 
# - A belief state is whatever the agent remembers; anything not in it cannot influence its behaviour.
# - A generator produces values on demand, so it never builds the whole sequence in memory.
# - A dictionary lookup is fast regardless of size, which is why we use them for state tables.
# - A set membership test is also fast, which is why we use sets to record visited states.



# ## 3. Apparatus and setup
# 
# **Software:** Python 3.10 or later, Jupyter Notebook or JupyterLab, NumPy, Matplotlib.
# 
# Run the cell below first. If any import fails, install the missing package with `pip install <package>` and run the cell again before continuing.



import sys
print('Python', sys.version.split()[0])

import numpy, matplotlib
print('numpy', numpy.__version__)
print('matplotlib', matplotlib.__version__)
print('\nEnvironment ready.')



# ## 4. Procedure
# 
# Work through these steps in order. The code here is given to you and should run as it stands — read it, run it, and make sure you understand what each part does before moving on to your own tasks in Section 5.



# ### Step 1 — The data structures you will actually use
# 
# Run this and read the output carefully. Each of these four structures is used for a specific purpose in later practicals, noted in the comments.



# A list: an ordered sequence you can add to. Used for the frontier in search.
frontier = ['A', 'B', 'C']
frontier.append('D')
print('frontier      :', frontier)

# A dictionary: a lookup table. Used for mapping states to values.
distance = {'A': 0, 'B': 3, 'C': 7}
print('distance to B :', distance['B'])

# A set: fast membership testing. Used to record what we have already seen.
visited = {'A', 'B'}
print('seen C?       :', 'C' in visited)

# A tuple: a fixed group of values. Used for coordinates and immutable states.
position = (3, 5)
print('position      :', position, 'row', position[0])



# ### Step 2 — Generators: producing values one at a time
# 
# A generator computes each value only when it is asked for. In search problems the list of possible next moves can be enormous, so producing them one at a time matters. Note what happens when you consume a generator twice.



def squares_list(n):
    return [x * x for x in range(n)]        # builds the whole list at once

def squares_gen(n):
    for x in range(n):
        yield x * x                          # produces one value at a time

print('list   :', squares_list(5))
print('gen    :', list(squares_gen(5)))

g = squares_gen(5)
print('first sum :', sum(g))
print('second sum:', sum(g), '   <- a generator is consumed once')



# ### Step 3 — An agent and its environment
# 
# Here is a minimal agent in a corridor of rooms. It can move left or right, it senses only whether the current room is dirty, and its belief state records which rooms it has already cleaned. Read the loop and identify the four stages from Lecture 2.



import random
random.seed(0)

class Environment:
    def __init__(self, n_rooms=5):
        self.n = n_rooms
        self.dirty = {r: random.choice([True, False]) for r in range(n_rooms)}
        self.position = 0

    def percept(self):
        # The agent sees ONLY whether the current room is dirty.
        return {'dirty': self.dirty[self.position]}

    def act(self, action):
        if action == 'clean':
            self.dirty[self.position] = False
        elif action == 'right' and self.position < self.n - 1:
            self.position += 1
        elif action == 'left' and self.position > 0:
            self.position -= 1

env = Environment()
print('true state (hidden from the agent):', env.dirty)
print('what the agent can see           :', env.percept())



# ### Step 4 — The sense-update-decide-act loop
# 
# This agent keeps a belief state: the set of rooms it believes it has cleaned. Notice that the decision uses only the belief state and the current percept.



def run_agent(env, steps=12, verbose=True):
    cleaned = set()                       # THE BELIEF STATE
    for t in range(steps):
        percept = env.percept()           # SENSE
        if percept['dirty']:              # UPDATE + DECIDE
            action = 'clean'
            cleaned.add(env.position)
        else:
            action = 'right'
        if verbose:
            print('t=%2d  room=%d  percept=%-5s  action=%-5s  belief=%s'
                  % (t, env.position, percept['dirty'], action, sorted(cleaned)))
        env.act(action)                   # ACT
    return cleaned

env = Environment()
cleaned = run_agent(env)
print('\nrooms still dirty:', [r for r, d in env.dirty.items() if d])



# ## 5. Tasks
# 
# These are your work. Each cell marked `# TODO` is for you to complete. Write your own code; do not copy the procedure cells unchanged.



# ### Task 1 — Predict before you run
# 
# Write a generator that produces the first n even numbers. Before running it, write in a comment what you expect `sum()` to return the second time it is called on the same generator, and then check.
# 
# > **Marks:** 2



# TODO
# My prediction for the second sum: 

def even_numbers(n):
    pass



# ### Task 2 — Give the agent a better policy
# 
# The agent above always moves right, so it walks off the end of the corridor and stops making progress. Write a new policy that uses the belief state to turn around when it reaches the end. Run it and confirm every room is cleaned.
# 
# > **Marks:** 4



# TODO: write run_agent_v2 with a policy that reverses direction at the ends



# ### Task 3 — Break the belief state deliberately
# 
# Remove the belief state from your agent — that is, stop recording which rooms have been cleaned — and run it again. Describe in a comment what changes about its behaviour, and explain why in terms of Lecture 2.
# 
# > **Marks:** 4



# TODO: an agent with no belief state, plus your explanation as a comment



# ### Task 4 — Count the work
# 
# Modify your agent to count how many actions it takes to clean every room. Run it on corridors of 5, 10 and 20 rooms and record the counts in the observations table.
# 
# > **Marks:** 3



# TODO: return the number of actions taken, and run for n = 5, 10, 20



# ### Task 5 — Describe your agent in four parts
# 
# In a markdown cell below, describe your agent using the four parts from Lecture 1: abilities, goals, prior knowledge, and experience. Be specific — name the actual variables in your code where you can.
# 
# > **Marks:** 2



# TODO: write your four-part description in a markdown cell below this one



# ## 6. Observations
# 
# Complete this table from your own results. Do not leave it blank — the observations carry marks and are what the viva is based on.
# 
# | Corridor size | Actions taken (with belief state) | Actions taken (without) | Every room cleaned? |
# |---|---|---|---|
# | 5 rooms  | 5 | 6 | 7 |
# | 10 rooms |  |  |  |
# | 20 rooms |  |  |  |



# ## 7. Discussion
# 
# Answer in your own words, in the cell below. Two or three sentences each is enough.
# 
# 1. What exactly does your agent's belief state contain, and what did you deliberately leave out of it?
# 2. Your agent senses only the current room. Give a situation where two different rooms produce identical percepts but require different actions.
# 3. How did the number of actions grow as the corridor got longer? Was the growth roughly proportional, or worse?



# *Your answers:*
# 
# 1. 
# 
# 2. 
# 
# 3. 



# ## 8. Submission checklist
# 
# - [ ] Notebook runs top to bottom from a clean kernel with no errors
# - [ ] Every `# TODO` cell is completed with your own code
# - [ ] The observations table is filled in with your actual results
# - [ ] Discussion answers are written in your own words
# - [ ] Your name and roll number are in the cell below
# - [ ] File named `P01_<your-roll-number>.ipynb`



NAME = ""
ROLL_NUMBER = ""
print(NAME, ROLL_NUMBER)

