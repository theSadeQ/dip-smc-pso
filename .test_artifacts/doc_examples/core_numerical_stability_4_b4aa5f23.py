# Example from: docs\reference\plant\core_numerical_stability.md
# Index: 4
# Runnable: True
# Hash: b4aa5f23

from src.plant.core import AdaptiveRegularizer

# Research-grade precision (default)
research_regularizer = AdaptiveRegularizer(
    regularization_alpha=1e-6,
    max_condition_number=1e14
)

# Real-time systems (more aggressive)
realtime_regularizer = AdaptiveRegularizer(
    regularization_alpha=1e-4,
    max_condition_number=1e12
)

# Fixed regularization (fastest)
fixed_regularizer = AdaptiveRegularizer(
    use_fixed_regularization=True,
    min_regularization=1e-8
)