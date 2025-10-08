# Example from: docs\controllers\control_primitives_reference.md
# Index: 25
# Runnable: True
# Hash: 311a23a5

from src.utils.numerical_stability import safe_log

# PSO cost function with log penalty
cost = ise + 1000 * safe_log(1 + instability_penalty)