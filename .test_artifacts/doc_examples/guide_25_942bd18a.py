# Example from: docs\optimization_simulation\guide.md
# Index: 25
# Runnable: True
# Hash: 942bd18a

from src.plant.models.simplified import SimplifiedDIPDynamics

dynamics = SimplifiedDIPDynamics(
    config,
    enable_fast_mode=True,    # Use Numba JIT compilation
    enable_monitoring=False   # Disable diagnostics for speed
)