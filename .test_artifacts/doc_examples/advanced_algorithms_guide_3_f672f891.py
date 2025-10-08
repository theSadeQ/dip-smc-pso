# Example from: docs\mathematical_foundations\advanced_algorithms_guide.md
# Index: 3
# Runnable: False
# Hash: f672f891

# Configure physics uncertainty in config.yaml:
# physics_uncertainty:
#   n_evals: 5  # 5 perturbed models per evaluation
#   cart_mass: 0.10          # ±10%
#   pendulum1_mass: 0.15     # ±15%
#   pendulum2_mass: 0.15     # ±15%
#   pendulum1_length: 0.05   # ±5%
#   pendulum2_length: 0.05   # ±5%

tuner = PSOTuner(
    controller_factory=controller_factory,
    config=config,
    seed=42
)

# PSO will automatically evaluate robustness across perturbed models
result = tuner.optimise()

# Each fitness evaluation runs 5 simulations (1 nominal + 4 perturbed)
# Cost aggregation: 0.7 * mean + 0.3 * max