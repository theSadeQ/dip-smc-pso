# Example from: docs\controllers\factory_system_guide.md
# Index: 36
# Runnable: True
# Hash: ad110194

# Solution: Check gain bounds and constraints
lower, upper = get_gain_bounds_for_pso(SMCType.SUPER_TWISTING)
# Ensure K1 bounds > K2 bounds for STA-SMC
# lower[0] > lower[1], upper[0] > upper[1]