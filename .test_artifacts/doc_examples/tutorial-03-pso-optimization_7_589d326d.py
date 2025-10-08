# Example from: docs\guides\tutorials\tutorial-03-pso-optimization.md
# Index: 7
# Runnable: True
# Hash: 589d326d

from src.optimizer.pso_optimizer import PSOTuner
from custom_cost import custom_cost_function

tuner = PSOTuner(
    controller_factory=controller_factory,
    config=config,
    cost_function=custom_cost_function  # Custom cost
)

best_gains, best_cost = tuner.optimize()