# Example from: docs\controllers\swing_up_smc_technical_guide.md
# Index: 27
# Runnable: True
# Hash: 4b52a435

# 1. Increase energy gain
swing_up.k_swing = 70.0  # From 50.0

# 2. Increase force limit
swing_up.max_force = 30.0  # From 20.0

# 3. Relax angle tolerance
swing_up.switch_angle_tol = 0.45  # From 0.35 rad

# 4. Check energy calculation
E_current = dynamics.total_energy(state)
print(f"E_current: {E_current}, E_bottom: {swing_up.E_bottom}")