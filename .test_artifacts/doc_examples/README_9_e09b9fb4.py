# Example from: docs\guides\api\README.md
# Index: 9
# Runnable: True
# Hash: e09b9fb4

from src.config.schemas import SimulationConfig

# Programmatic configuration
config = SimulationConfig(
    duration=5.0,
    dt=0.01,
    initial_conditions=[0, 0, 0.1, 0, 0.15, 0]
)