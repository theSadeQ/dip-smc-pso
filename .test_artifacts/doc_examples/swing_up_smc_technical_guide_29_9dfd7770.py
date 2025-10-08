# Example from: docs\controllers\swing_up_smc_technical_guide.md
# Index: 29
# Runnable: False
# Hash: 9dfd7770

# 1. Use smoother stabilizer
stabilizer = SuperTwistingSMC(...)  # Continuous control

# 2. Tighten handoff criteria
swing_up.switch_angle_tol = 0.25  # From 0.35 (closer to upright)

# 3. Verify stabilizer initialization
if hasattr(stabilizer, "initialize_state"):
    state_vars = stabilizer.initialize_state()
else:
    print("WARNING: Stabilizer missing initialize_state()")