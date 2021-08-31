import random
import numpy as np
import matplotlib.pyplot as plt

# Read map from a file.txt
def load_map(map_path):
    with open(map_path) as f:
        city = f.readlines()
    for i in range(len(city) - 1):
        city[i] = city[i][0 : -1]
    return city

# Given a map find the starting position of the taxi
def get_starting_position(city):
    for i in range(len(city)):
        if city[i].find('T') != -1:
            return i, city[i].find('T')

# Given the current state check which action has the maximum expected reward
def best_action(x, y, picked, q_table):
    best = 0
    for i in range(1, 6):
        if q_table[x][y][picked][i] > q_table[x][y][picked][best]:
            best = i
    return best

"""
Possible actions:
    
0 : go up
1 : go right
2 : go down
3 : go left
4 : pick the passenger up
5 : leave the passenger down
"""

def make_step(x, y, action, city, picked):
    old_x, old_y = x, y
    if action == 0:
        x -= 1
    if action == 1:
        y += 1
    if action == 2:
        x += 1
    if action == 3:
        y -= 1
    if action <= 3:
        if x < 0 or x >= len(city) or y < 0 or y >= len(city[x]) or city[x][y] == '#':
            return old_x, old_y, -10, False, picked
        else:
            return x, y, -1, False, picked
    else:
        if action == 4:
            if picked == 1 or city[x][y] != 'A':
                return x, y, -10, False, picked
            else:
                return x, y, 20, False, 1
        else:
            if picked == 1 and city[x][y] == 'B':
                return x, y, 20, True, picked
            else:
                return x, y, -10, False, picked

# In each episode the agent find a path using and updating the q_table 
# Bellam's equation is used to update the q_table
def episode(start_x, start_y, q_table, alpha, gamma, epsilon, city):
    x, y, picked = start_x, start_y, 0 
    steps = 0
    total_reward = 0
    terminated = False
    moves = [[x, y, picked]]
    while terminated == False:
        if random.uniform(0, 1) < epsilon:
            action = random.randint(0, 5)
        else:
            action = best_action(x, y, picked, q_table)
        next_x, next_y, reward, done, next_picked = make_step(x, y, action, city, picked)
        old_value = q_table[x][y][picked][action]
        next_max = q_table[next_x][next_y][next_picked][best_action(next_x, next_y, next_picked, q_table)]
        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        q_table[x][y][picked][action] = new_value
            x, y, picked = next_x, next_y, next_picked
        moves.append([x, y, picked])
        terminated = done
        steps += 1
        total_reward += reward
    return steps, total_reward, moves

# To train the AI just run many episodes 
def train():
    map_path = 'maps/map1/'
    total_episodes = 150 
    city = load_map(map_path + 'map.txt')
    start_x, start_y = get_starting_position(city)
    alpha = 0.1     # Learning rate
    gamma = 0.8     # Discount factor
    epsilon = 0.1   # Probability of making a random move
    q_table = np.zeros((len(city), len(city[0]), 2, 6))
    steps, penalties, rewards = [], [], []
    moves = []      # Keeping track of all the moves
    for i in range(total_episodes):
        step, rew, move = episode(start_x, start_y, q_table, alpha, gamma, epsilon, city)
        steps.append(step)
        moves.append(move)
        rewards.append(rew)

    # Collecting moves' information
    f = open(map_path + 'moves.txt', 'w')
    f.write(str(moves))
    f.close()

    # Graph which analyze the number of steps
    plt.title('steps required')
    plt.xlabel('episodes')
    plt.ylabel('steps used')
    plt.plot(range(total_episodes), steps, label = 'steps')
    plt.ylim(1, max(steps))
    plt.xlim(1, total_episodes)
    plt.show()

    # Best route found
    f = open(map_path + 'best.txt', 'w')
    f.write(str(min(steps)) + ' ' + str(steps.index(min(steps))))
    f.close()


if __name__ == '__main__':
    train()
