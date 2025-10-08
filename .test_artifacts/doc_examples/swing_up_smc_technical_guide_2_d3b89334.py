# Example from: docs\controllers\swing_up_smc_technical_guide.md
# Index: 2
# Runnable: True
# Hash: d3b89334

# Bottom position (down-down)
state_bottom = [0, π, π, 0, 0, 0]
E_bottom = dynamics.total_energy(state_bottom)

# Upright position (target)
state_upright = [0, 0, 0, 0, 0, 0]
E_upright = dynamics.total_energy(state_upright)  # = -(m₁+m₂)g(L₁+L₂)