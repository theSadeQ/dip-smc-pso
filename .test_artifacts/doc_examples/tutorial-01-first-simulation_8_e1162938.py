# Example from: docs\guides\tutorials\tutorial-01-first-simulation.md
# Index: 8
# Runnable: True
# Hash: e1162938

# Random initial angles: ±0.2 rad
initial_conditions = np.random.uniform(
    low=[0, 0, -0.2, 0, -0.2, 0],
    high=[0, 0, 0.2, 0, 0.2, 0],
    size=(10, 6)
)