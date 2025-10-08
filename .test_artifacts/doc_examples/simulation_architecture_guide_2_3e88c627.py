# Example from: docs\mathematical_foundations\simulation_architecture_guide.md
# Index: 2
# Runnable: True
# Hash: 3e88c627

from src.simulation.engines.vector_sim import simulate
import numpy as np

# Single pendulum simulation
x0 = np.array([0.0, 0.1, -0.05, 0.0, 0.0, 0.0])  # [x, θ1, θ2, ẋ, θ̇1, θ̇2]
u = np.zeros(100)  # No control input
dt = 0.01  # 10 ms timestep

states = simulate(x0, u, dt)

print(f"State shape: {states.shape}")  # (101, 6) - includes initial state
print(f"Initial state: {states[0]}")   # Same as x0
print(f"Final state: {states[-1]}")