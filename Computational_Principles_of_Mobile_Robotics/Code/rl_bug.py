import numpy as np
import pprint as pp
import random
import csv

# Point Robot Simulated Environment
env = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,1,1,1,0,0,0,0],
    [0,0,0,0,0,1,1,1,1,1,0,0,0],
    [0,0,0,0,1,1,1,1,1,1,0,0,0],
    [0,0,0,0,1,1,1,0,1,1,1,0,0],
    [0,0,1,0,1,1,1,0,0,1,1,0,0],
    [0,0,1,1,0,1,1,0,1,0,1,0,0],
    [0,0,1,1,1,0,1,0,1,1,0,0,0],
    [0,0,1,1,1,0,0,0,1,1,0,0,0],
    [0,0,0,1,1,1,0,1,1,1,0,0,0],
    [0,0,0,0,1,1,1,1,1,1,0,0,0],
    [0,0,0,0,0,1,1,1,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0]
]

# Size of environment
MAX_ROW = len(env)
MAX_COL = len(env[0])

# Point Robot Moves N,S,E,W,NW,SW,NE,SE
MOVES = [(-1, 0), (1, 0), (0, 1), (0, -1), (-1, -1), (1, -1), (-1, 1), (1, 1)]

def collision(state) -> bool:
    """
    args: state value
    return: bool, collided with obstacle
    """

    r, c = state

    return env[r][c] == 1

def magnitude(vector) -> float:
    """
    args: array
    return: magnitude of array (not length)
    """
    # Total for sum
    total = 0 

    # Run summation of squared values
    for i in range(len(vector)):
        total += vector[i]**2

    return total **.5

def create_points(env) -> tuple:
    """
    args: Environment - Hexagon over grid, can be infinite
    
    States: Are one hot encoded tuples/arrays of coordinates, representing state multi-dimensional state.
    return: tuple, dictionary<states, values> and array of obstacles
    """

    # Value function
    v = {}

    # Obstacles reachable by agent
    walls = []

    # Build world
    for i in range(MAX_ROW):
        for j in range(MAX_COL):
            
            # Set value for visible states
            v[(i, j)] = 0

            # Obstacle blocking agent
            if env[i][j] == 1:
                walls.append((i, j))

    return v, walls

def obstacle_distance(state, walls, goal) -> tuple: 
    """
    args: State agent is in and obstacles nearby
    return: tuple, tuple of arrays - distance, angles, bearings
    """

    # Store length for looping
    length = len(walls)

    # Ignore warning
    np.seterr(invalid='ignore')

    # Distances to obstructions
    distances = [(((state[0] - walls[i][0])**2 + (state[1] - walls[i][1])**2)**.5 )/5*100  for i in range(length)]

    # Angles in radians to obstructions
    angles = [np.arccos(np.dot(state, walls[i])/(magnitude(state)*magnitude(walls[i]))) for i in range(length)]

    # Bearings in degrees to obstructions
    bearings = [np.arccos(np.dot(state, walls[i])/(magnitude(state)*magnitude(walls[i])))*180/np.pi for i in range(length)]

    # Distance from state to goal
    distance = ( (goal[0] - state[0])**2 + (goal[1] - state[1])**2 ) **.5

    # Angle from state in radians to goal
    angle = np.arccos(np.dot(state, goal)/(magnitude(state)*magnitude(goal))) 

    # Bearings from state in degrees to goal
    bearing = np.arccos(np.dot(state, goal)/(magnitude(state)*magnitude(goal)))*180/np.pi 

    return distances, angles, bearings, distance, angle, bearing

def simulate_vision(state, action, goal) -> tuple:
    """
    args: 
        state - current state of agent
        action - the action to be taken
        goal - the terminal state 
    
    returns:
        S', R
        next state and reward after agent visually scans environment
    """
    
    # Take action to next state
    next_state = (action[0] + state[0], action[1] + state[1])

    # Set boundary conditions
    out_of_bounds = (next_state[0] < 0 or next_state[0] >= MAX_ROW) or (next_state[1] < 0 or next_state[1] >= MAX_COL)

    # Collision detection
    collided = collision(next_state) if not out_of_bounds else False

    # Stay in current state if next state out of bounds
    if out_of_bounds: next_state = state

    # Reward signal is -1 until agent locates goal
    r = 0 if state == goal and not collided else -1

    return next_state, r

def argmax(Q):
    """
    Return index of max value with ties broken randomly
    """

    # Max value
    maximum = float('-inf')

    # Ties seen
    ties = []

    # Loop through Q values
    for i in range(len(Q)):

        # Greater than current maximum
        if Q[i] > maximum:

            # New current maximum
            maximum = Q[i]

            # No Ties seen for this value
            del ties[:]

        # Ties found
        if Q[i] == maximum:

            # Add index to ties
            ties.append(i)

    return random.choice(ties)

def e_greedy(Q, epsilon):
    """
    Return an action based on e-greedy policy
    """
    
    # Exploration
    if np.random.random() < epsilon:
        
        # Explorative action
        action = random.randint(0, len(MOVES)-1)

    # Exploitation
    else:

        # e-greedy action
        action = argmax(Q)
    
    return action

def create():
    """
    Create and return Q and arbitrary policy
    """
    
    # Policy and Q
    policy = {}; Q = {}

    # Create states for policy
    for i in range(MAX_ROW*MAX_COL):

        # Create row index
        row = i // MAX_COL

        # Create column index
        column = i % MAX_COL

        # Create policy
        policy[(row, column)] = MOVES
        
        # Create Q(s,a)
        Q[(row, column)] = [0] * len(MOVES)

    # Q and policy 
    return Q, policy

def Q_learning(episodes, start, goal, epsilon):
    """
    Return q* from Q-Learning Off-Policy TD Control (e-greedy)
    """
    
    ##########################################################
    # Q-Learning Off-Policy TD Control for estimating Q = q* #
    ##########################################################

    # Algorithm parameters: step size a -> (0, 1], small "a > 0
    alpha = 0.5

    # Initialize Q(s, a), for all s of S+, a of A(s), arbitrarily except that Q(terminal, ·)=0
    Q, policy = create()

    #Loop for each episode:
    for _ in range(episodes):

        # Initialize S
        S = start

        #Loop for each step of episode: until S is terminal
        while S != goal:
            
            # Choose A from S using policy derived from Q (e-greedy)
            A = e_greedy(Q[S], epsilon)

            # Take action A, observe R, S'
            S_prime, R = simulate_vision(S, MOVES[A], goal)

            # Q(S, A) <-- Q(S, A) + a[R + gamma*Q(S', A') - Q(S, A)]
            Q[S][A] = Q[S][A] + alpha*(R + max(Q[S_prime]) - Q[S][A])
            
            # S <-- S'
            S = S_prime
            
    # Output Q estimate of q*
    return Q, policy

def memory(Q, path):
    with open(path, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write multiple rows
        writer.writerows(Q.items())


if __name__ == "__main__":
    path = Q_learning(170, (8, 0), (1, 11), 0.1)
    pi = {state: argmax(val) for state, val in path[0].items()}
    
    memory(path[0], "q_values.csv")
    memory(pi, "policy.csv")
