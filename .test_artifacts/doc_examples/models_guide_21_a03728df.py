# Example from: docs\plant\models_guide.md
# Index: 21
# Runnable: True
# Hash: a03728df

dynamics = SimplifiedDIPDynamics(
    config,
    enable_fast_mode=True,    # Use Numba JIT compilation
    enable_monitoring=False   # Disable monitoring for maximum speed
)