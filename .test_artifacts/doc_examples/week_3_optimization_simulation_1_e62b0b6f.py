# Example from: docs\plans\documentation\week_3_optimization_simulation.md
# Index: 1
# Runnable: True
# Hash: e62b0b6f

J(g) = w₁·ISE(g) + w₂·chattering(g) + w₃·control_effort(g)

where:
  ISE(g) = ∫₀ᵀ ||x(t;g)||² dt
  chattering(g) = ∫₀ᵀ |u̇(t;g)| dt
  control_effort(g) = ∫₀ᵀ u²(t;g) dt