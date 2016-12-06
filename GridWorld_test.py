from GridWorld import *
import numpy as np
import matplotlib.pyplot as plt

size = 5
g = DaPingTai(size, 0.3, 0.9)

s = g.startState
r = np.reshape(g.ground_r, (size, size))


m, ms, mg = g.generatemaze(g.ground_r)
g.find_path_bfs(m, ms, mg)
sx, sy = g.int_to_point(g.startState)
rx, ry = g.int_to_point(g.positiveState)
r[sx, sy] = 10
r[rx, ry] = 1

print(r)

#policy = [gw.optimal_policy_deterministic(s, ground_r) for s in range(gw.n_states)]

#print(ground_r)

#print(np.reshape(policy, (size, size)).T)
