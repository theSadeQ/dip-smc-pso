# Example from: docs\reference\plant\core_numerical_stability.md
# Index: 7
# Runnable: True
# Hash: d3153084

from src.plant.core import MatrixInverter, AdaptiveRegularizer

# Default regularizer
inverter = MatrixInverter()

# Custom regularizer
custom_reg = AdaptiveRegularizer(regularization_alpha=1e-5)
custom_inverter = MatrixInverter(regularizer=custom_reg)