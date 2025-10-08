# Example from: docs\guides\how-to\running-simulations.md
# Index: 6
# Runnable: True
# Hash: 37bb84a6

# In custom loop
if i % 10 == 0:  # Store every 10th sample
    time_log.append(i * dt)
    state_log.append(state.copy())
    control_log.append(u)