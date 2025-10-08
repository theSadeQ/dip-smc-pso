# Example from: docs\pso_integration_system_architecture.md
# Index: 8
# Runnable: True
# Hash: 5b0b5260

# Multi-level instability detection:
1. NaN/Inf trajectory values (immediate penalty)
2. Pendulum angle limits |θ| > π/2 (early termination)
3. State explosion |x| > 1e6 (numerical instability)
4. Control saturation violations (soft penalty)