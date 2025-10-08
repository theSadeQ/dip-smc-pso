# Example from: docs\optimization_simulation\guide.md
# Index: 1
# Runnable: True
# Hash: 269ec14a

from src.config import load_config

config = load_config("config.yaml")

# Configure physics uncertainty
config.physics_uncertainty.n_evals = 5  # Number of perturbed evaluations
config.physics_uncertainty.cart_mass = 0.1  # ±10% variation
config.physics_uncertainty.pendulum1_mass = 0.1
config.physics_uncertainty.pendulum2_mass = 0.1