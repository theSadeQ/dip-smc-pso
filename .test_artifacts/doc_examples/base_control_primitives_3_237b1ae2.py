# Example from: docs\reference\controllers\base_control_primitives.md
# Index: 3
# Runnable: True
# Hash: 237b1ae2

from src.controllers.base.control_primitives import anti_windup_back_calculation

# PID-like controller with integral term
integral = 5.0  # Accumulated integral error
u_raw = 150.0   # Requested control
u_max = 100.0

# Saturated control
u_sat = saturate(u_raw, u_max)  # 100.0 N

# Back-calculation anti-windup
T_i = 1.0  # Integration time constant
integral_correction = (u_sat - u_raw) / T_i  # Negative (reduces integral)

integral_new = integral + integral_correction * dt
print(f"Integral before: {integral:.3f}")
print(f"Integral after:  {integral_new:.3f}")  # Reduced