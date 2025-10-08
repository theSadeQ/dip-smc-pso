# Example from: docs\reference\controllers\smc_core_equivalent_control.md
# Index: 4
# Runnable: True
# Hash: 76b4d150

from src.utils.control.saturation import saturate

# Compute equivalent control (model-based)
u_eq = eq_control.compute(state)

# Compute sliding surface
s = surface.compute(state)

# Compute switching control (robustness)
K_sw = 50.0  # Switching gain
epsilon = 0.01  # Boundary layer
u_sw = -K_sw * saturate(s, epsilon, method='tanh')

# Total control
u_total = u_eq + u_sw

# Apply actuator limits
u_max = 100.0
u = np.clip(u_total, -u_max, u_max)

print(f"u_eq={u_eq:.2f}, u_sw={u_sw:.2f}, u_total={u:.2f}")