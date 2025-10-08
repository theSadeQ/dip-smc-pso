# Example from: docs\reference\controllers\smc_algorithms_adaptive_controller.md
# Index: 9
# Runnable: True
# Hash: 8b41f166

from src.controllers.smc.algorithms.adaptive.adaptation_law import AdaptationLaw

# Experiment with different adaptation strategies
adaptation = AdaptationLaw(
    gamma=5.0,        # Fast adaptation
    sigma=0.1,        # Low leakage
    K_min=1.0,        # Minimum gain bound
    K_max=200.0       # Maximum gain bound
)

# Test adaptation response
for uncertainty in [5.0, 10.0, 20.0]:
    adapted_gain = adaptation.update(surface=0.1, uncertainty=uncertainty, dt=0.01)
    print(f"Uncertainty={uncertainty}: K={adapted_gain:.2f}")