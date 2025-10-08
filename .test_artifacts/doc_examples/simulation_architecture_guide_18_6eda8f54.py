# Example from: docs\mathematical_foundations\simulation_architecture_guide.md
# Index: 18
# Runnable: False
# Hash: 6eda8f54

# GOOD: Pre-allocate result array
states = np.zeros((batch_size, horizon + 1, state_dim), dtype=float)
states[:, 0, :] = initial_state

for i in range(horizon):
    states[:, i+1, :] = dynamics_step(states[:, i, :], u[:, i], dt)

# BAD: Append to list
states = [initial_state]
for i in range(horizon):
    states.append(dynamics_step(states[-1], u[i], dt))
states = np.array(states)  # Expensive conversion at end