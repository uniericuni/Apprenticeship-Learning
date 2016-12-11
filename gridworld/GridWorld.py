"""
Implements the gridworld MDP.
Matthew Alger, 2015
matthew.alger@anu.edu.au
"""

import numpy as np
import random
import numpy.random as rn
from collections import deque


class DaPingTai(object):
    """
    Gridworld MDP.
    """

    def __init__(self, grid_size, wind, discount):
        """
        grid_size: Grid size. int.
        wind: Chance of moving randomly. float.
        discount: MDP discount. float.
        -> Gridworld
        """

        self.actions = ((1, 0), (0, 1), (-1, 0), (0, -1))    #down,right, up, left
        self.n_actions = len(self.actions)
        self.n_states = grid_size ** 2
        self.grid_size = grid_size
        self.wind = wind
        self.discount = discount
        # Construct whole map as an n_states x 1 array
        self.ground_r = np.array([self.setNegativeReward(s) for s in range(self.n_states)])
        self.positiveState = self.setPostiveRewardState(self.ground_r)
        self.startState = self.setStartState(self.ground_r)
        self.currentState = self.startState
        self.negativeScore = 0



        # Preconstruct the transition probability array.
        """
        self.transition_probability = np.array(
            [[[self._transition_probability(i, j, k)
               for k in range(self.n_states)]
              for j in range(self.n_actions)]
             for i in range(self.n_states)])
        """

    def __str__(self):
        return "Gridworld({}, {}, {})".format(self.grid_size, self.wind,
                                              self.discount)

    def feature_vector(self, i, feature_map="ident"):
        """
        Get the feature vector associated with a state integer.
        i: State int.
        feature_map: Which feature map to use (default ident). String in {ident,
            coord, proxi}.
        -> Feature vector.
        """

        # Assume identity map.
        f = np.zeros(self.n_states)
        f[i] = 1
        return f

    def feature_matrix(self, feature_map="ident"):
        """
        Get the feature matrix for this gridworld.
        feature_map: Which feature map to use (default ident). String in {ident,
            coord, proxi}.
        -> NumPy array with shape (n_states, d_states).
        """

        features = []
        for n in range(self.n_states):
            f = self.feature_vector(n, feature_map)
            features.append(f)
        return np.array(features)

    def int_to_point(self, i):
        """
        Convert a state int into the corresponding coordinate.
        i: State int.
        -> (x, y) int tuple.
        """

        return (i // self.grid_size, i % self.grid_size)

    def point_to_int(self, p):
        """
        Convert a coordinate into the corresponding state int.
        p: (x, y) tuple.
        -> State int.
        """

        return p[0]*self.grid_size + p[1]

    def neighbouring(self, i, k):
        """
        Get whether two points neighbour each other. Also returns true if they
        are the same point.
        i: (x, y) int tuple.
        k: (x, y) int tuple.
        -> bool.
        """

        return abs(i[0] - k[0]) + abs(i[1] - k[1]) <= 1

    def getLegalAction(self, state):
        sx, sy = self.int_to_point(state)
        flag = np.zeros((4,))
        if sx == 0:
            flag[2] = 1      
        if sx == self.grid_size - 1:
            flag[0] = 1
        if sy == 0:
            flag[3] = 1
        if sy == self.grid_size - 1:
            flag[1] = 1
        return list(np.where(flag == 0)[0])







    def _transition_probability(self, i, j, k):
        """
        Get the probability of transitioning from state i to state k given
        action j.
        i: State int.
        j: Action int.
        k: State int.
        -> p(s_k | s_i, a_j)
        """

        xi, yi = self.int_to_point(i)
        xj, yj = self.actions[j]
        xk, yk = self.int_to_point(k)

        if not self.neighbouring((xi, yi), (xk, yk)):
            return 0.0

        # Is k the intended state to move to?
        if (xi + xj, yi + yj) == (xk, yk):
            return 1 - self.wind + self.wind/self.n_actions

        # If these are not the same point, then we can move there by wind.
        if (xi, yi) != (xk, yk):
            return self.wind/self.n_actions

        # If these are the same point, we can only move here by either moving
        # off the grid or being blown off the grid. Are we on a corner or not?
        if (xi, yi) in {(0, 0), (self.grid_size-1, self.grid_size-1),
                        (0, self.grid_size-1), (self.grid_size-1, 0)}:
            # Corner.
            # Can move off the edge in two directions.
            # Did we intend to move off the grid?
            if not (0 <= xi + xj < self.grid_size and
                    0 <= yi + yj < self.grid_size):
                # We intended to move off the grid, so we have the regular
                # success chance of staying here plus an extra chance of blowing
                # onto the *other* off-grid square.
                return 1 - self.wind + 2*self.wind/self.n_actions
            else:
                # We can blow off the grid in either direction only by wind.
                return 2*self.wind/self.n_actions
        else:
            # Not a corner. Is it an edge?
            if (xi not in {0, self.grid_size-1} and
                yi not in {0, self.grid_size-1}):
                # Not an edge.
                return 0.0

            # Edge.
            # Can only move off the edge in one direction.
            # Did we intend to move off the grid?
            if not (0 <= xi + xj < self.grid_size and
                    0 <= yi + yj < self.grid_size):
                # We intended to move off the grid, so we have the regular
                # success chance of staying here.
                return 1 - self.wind + self.wind/self.n_actions
            else:
                # We can blow off the grid only by wind.
                return self.wind/self.n_actions

    def setPostiveRewardState(self, ground_r):
        """
        Set positive reward state
        """
        ground_r_copy = np.copy(ground_r)
        points = np.array(range(self.n_states))

        return np.random.choice(points[ground_r_copy == 0])

    def getAction(self, action):
        return self.actions[action]

    def getPostiveRewardState(self):
        """
        Return postive rewards state
        """
        return self.positiveState

    def setNegativeReward(self, state_int):
        """
        Set Negative rewards
        """
        p = np.random.uniform()
        if p > 0.9:
            return -1
        else:
            return 0

    def setStartState(self, ground_r):
        """
        Set the starting state
        """
        ground_r_copy = np.copy(ground_r)
        goalState = self.getPostiveRewardState()
        ground_r_copy[goalState] = 1
        points = np.array(range(self.n_states))


        return np.random.choice(points[ground_r_copy == 0])
    def getStartState(self):
        """
        Return starting state
        """

        return self.startState

    def getCurrentState(self):

        return self.currentState

    def setCurrentState(self, currentState):

        self.currentState = currentState

    def convertToMatrix(self, ground_r):
        """
        Generate matrix version of the whole map. With up left being first state, right corner being last state 
        """
        matrix_ground_r = np.reshape(ground_r, (self.grid_size, self.grid_size))
        return matrix_ground_r

    def increaseNegativeScore(self, score):
        self.negativeScore = self.negativeScore + score

    def getNegativeScore(self):
        return self.negativeScore

    def setNegativeScore(self, num):
        self.negativeScore = num

    def average_reward(self, n_trajectories, trajectory_length, policy):
        """
        Calculate the average total reward obtained by following a given policy
        over n_paths paths.
        policy: Map from state integers to action integers.
        n_trajectories: Number of trajectories. int.
        trajectory_length: Length of an episode. int.
        -> Average reward, standard deviation.
        """

        trajectories = self.generate_trajectories(n_trajectories,
                                             trajectory_length, policy)
        rewards = [[r for _, _, r in trajectory] for trajectory in trajectories]
        rewards = np.array(rewards)

        # Add up all the rewards to find the total reward.
        total_reward = rewards.sum(axis=1)

        # Return the average reward and standard deviation.
        return total_reward.mean(), total_reward.std()

    def generatemaze(self, ground_r, startState):
        """
        Generate the maze for BFS
        """
        sx, sy = self.int_to_point(startState)

        goalState = self.getPostiveRewardState()
        gx, gy = self.int_to_point(goalState)

        matrix_ground_r = np.copy(self.convertToMatrix(ground_r))
        matrix_ground_r[sx, sy] = 0

        maze = np.zeros(((abs(gx - sx) + 3), (abs(gy - sy) + 3)))  - 1 # Generate walls around
        #print(sx, sy, gx, gy)
        #print(maze)
        extract_ground_r =  maze[1:-1, 1:-1]    
        if sx <= gx:
            if sy <= gy:
                extract_ground_r = matrix_ground_r[sx:gx+1, sy:gy+1]
                ms, mg = (1, 1), (len(maze) - 2, len(maze[0])-2)
            elif gy <= sy:
                extract_ground_r = matrix_ground_r[sx:gx+1, gy:sy+1]
                ms, mg = (1, len(maze[0])-2), (len(maze) - 2, 1)
        elif gx <= sx:
            if gy <= sy:
                extract_ground_r = matrix_ground_r[gx:sx+1, gy:sy+1]
                ms, mg = (len(maze) - 2, len(maze[0])-2), (1, 1)
            elif sy <= gy:
                extract_ground_r = matrix_ground_r[gx:sx+1, sy:gy+1]
                ms, mg = (len(maze) - 2, 1), (1, len(maze[0])-2)
        #print(extract_ground_r)
        maze[1:-1, 1:-1] = extract_ground_r

        

        return maze, ms, mg, sx, sy

    def maze2graph(self, maze):
        """
        Convert maze to graph for BFS
        """
        height = len(maze)
        width = len(maze[0]) if height else 0
        graph = {(i, j): [] for j in range(width) for i in range(height) if not maze[i][j]}
        for row, col in graph.keys():
            if row < height - 1 and not maze[row + 1][col]:
                graph[(row, col)].append(((1, 0), (row + 1, col)))
                graph[(row + 1, col)].append(((-1, 0), (row, col)))
            if col < width - 1 and not maze[row][col + 1]:
                graph[(row, col)].append(((0, 1), (row, col + 1)))
                graph[(row, col + 1)].append(((0, -1), (row, col)))
        return graph

    def find_path_bfs(self, maze, ms, mg):
        """
        Take the result of BFS as our optimal policy
        """
        start, goal = ms, mg
        #print(start, goal)
        queue = deque([([], start)])
        visited = set()
        graph = self.maze2graph(maze)
        while queue:
            path, current = queue.popleft()
            if current == goal:
                return path
            if current in visited:
                continue
            visited.add(current)
            for direction, neighbour in graph[current]:
                temp = path[:]
                temp.append(direction)              
                queue.append((temp, neighbour))
        return [(0, 0)]   # If no way, just stay


    def optimalPolicy(self, gamma):
        matrix_ground_r = self.convertToMatrix(self.ground_r)

        phi_sum = 0

        #print('g', matrix_ground_r)
        for state in range((self.n_states)):

            #print('State:', state)
            if self.ground_r[state] == -1:
                continue
            maze, ms, mg, sx, sy = self.generatemaze(self.ground_r, state) # Return start state of maze and real start state
            #print('Start:', (sx, sy))
            #print('Goal:', self.int_to_point(self.getPostiveRewardState()))
            phi = self.feature_vector(self.point_to_int((sx, sy)))
            path = self.find_path_bfs(maze, ms, mg)
            #print(path)

            for t, step in enumerate(path):
                sx = sx + step[0]
                sy = sy + step[1]          
                phi = phi + (gamma ** t) * self.feature_vector(self.point_to_int((sx, sy)))
            
            #print(np.reshape(phi, (4,4)))
            phi_sum = phi_sum + phi
        



        return phi_sum / self.n_states





    def generate_trajectories(self, n_trajectories, trajectory_length, policy,
                                    random_start=False):
        """
        Generate n_trajectories trajectories with length trajectory_length,
        following the given policy.
        n_trajectories: Number of trajectories. int.
        trajectory_length: Length of an episode. int.
        policy: Map from state integers to action integers.
        random_start: Whether to start randomly (default False). bool.
        -> [[(state int, action int, reward float)]]
        """

        trajectories = []
        for _ in range(n_trajectories):
            if random_start:
                sx, sy = rn.randint(self.grid_size), rn.randint(self.grid_size)
            else:
                sx, sy = 0, 0

            trajectory = []
            for _ in range(trajectory_length):
                if rn.random() < self.wind:
                    action = self.actions[rn.randint(0, 4)]
                else:
                    # Follow the given policy.
                    action = self.actions[policy(self.point_to_int((sx, sy)))]

                if (0 <= sx + action[0] < self.grid_size and
                        0 <= sy + action[1] < self.grid_size):
                    next_sx = sx + action[0]
                    next_sy = sy + action[1]
                else:
                    next_sx = sx
                    next_sy = sy

                state_int = self.point_to_int((sx, sy))
                action_int = self.actions.index(action)
                next_state_int = self.point_to_int((next_sx, next_sy))
                reward = self.reward(next_state_int)
                trajectory.append((state_int, action_int, reward))

                sx = next_sx
                sy = next_sy

            trajectories.append(trajectory)

        return np.array(trajectories)