# Example from: docs\optimization_simulation\guide.md
# Index: 11
# Runnable: True
# Hash: 76ec42ae

from src.config import load_config

# Load and validate configuration
config = load_config("config.yaml")

# Access with full IDE autocomplete and type checking
cart_mass: float = config.physics.cart_mass
duration: float = config.simulation.duration
n_particles: int = config.pso.n_particles

# Pydantic prevents typos and type errors
try:
    invalid = config.simulation.durration  # AttributeError
except AttributeError:
    print("Typo caught at runtime!")

try:
    config.physics.cart_mass = "not a number"  # ValidationError
except Exception:
    print("Type error prevented!")