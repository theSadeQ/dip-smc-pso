# Example from: docs\numerical_stability_guide.md
# Index: 9
# Runnable: True
# Hash: 3aa6434b

from src.controllers.smc.core.equivalent_control import EquivalentControl

# Controllers automatically use AdaptiveRegularizer
eq_control = EquivalentControl(
    dynamics_model=dynamics,
    regularization_alpha=1e-4,
    min_regularization=1e-10,
    max_condition_number=1e14,
    use_fixed_regularization=False
)

# Equivalent control computation with robust matrix operations
u_eq = eq_control.compute(state, sliding_surface)